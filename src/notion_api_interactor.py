import re
import uuid
from typing import List, Optional

import requests
from requests import RequestException


def make_md_from_block(block, image_map: dict) -> str:
    b_type = block["type"]
    block_content = block.get(b_type, {})

    # Pictures processing
    if b_type == "image":
        image = block["image"]
        url = ""
        if image["type"] == "external":
            url = image["external"]["url"]
        elif image["type"] == "file":
            url = image["file"]["url"]

        if not url:
            return ""

        img_id = f"img_{uuid.uuid4().hex[:8]}"
        image_map[img_id] = url

        caption_list = image.get("caption", [])
        caption = "".join(t["plain_text"] for t in caption_list)

        if not caption:
            caption = "Image"

        return f"\n![{caption}]({img_id})\n\n"

    # Text processing
    rich_text = block_content.get("rich_text", [])
    full_text = "".join(item["plain_text"] for item in rich_text)

    match b_type:
        case "paragraph":
            return full_text + "\n\n"
        case "heading_1":
            return f"# {full_text}\n\n"
        case "heading_2":
            return f"## {full_text}\n\n"
        case "heading_3":
            return f"### {full_text}\n\n"
        case "bulleted_list_item":
            return f"- {full_text}\n"
        case "numbered_list_item":
            return f"1. {full_text}\n"
        case "code":
            lang = block_content.get("language", "")
            return f"```{lang}\n{full_text}\n```\n\n"
        case "quote":
            return f"> {full_text}\n\n"
        case "callout":
            # Callout часто содержит эмодзи
            icon = block_content.get("icon", {}).get("emoji", "")
            return f"> {icon} {full_text}\n\n"

    return ""


# Notion API allows to get only 100 children/pages in a time, so we need to
# send a new request with updated cursor
def fetch_all_paginated_results(
    url: str, headers: dict, method: str = "GET", params: Optional[dict] = None
):
    """Fetch all paginated results from Notion API."""

    all_results = []
    has_more = True
    next_cursor = None

    current_params = params.copy() if params else {}

    while has_more:
        if next_cursor:
            current_params["start_cursor"] = next_cursor

        try:
            if method.upper() == "POST":
                response = requests.post(url, headers=headers, json=current_params)
            else:
                response = requests.get(url, headers=headers, params=current_params)

            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            all_results.extend(results)

            has_more = data.get("has_more", False)
            next_cursor = data.get("next_cursor")

        except RequestException as e:
            print(f" Error during request to {url}: {e}")
            break

    return all_results


def extract_and_resolve_images(text: str, image_map: dict) -> List[str]:
    """
    Searches for image IDs in the LLM response text and returns a list of URLs.
    Supports the following formats: (img_...), [img_...], or just img_... inside the Markdown link.
    """
    resolved_urls = []
    matches = re.findall(r"(img_[a-f0-9]{8})", text)

    unique_keys = []
    for m in matches:
        if m not in unique_keys:
            unique_keys.append(m)

    for img_key in unique_keys:
        if img_key in image_map:
            resolved_urls.append(image_map[img_key])

    return resolved_urls
