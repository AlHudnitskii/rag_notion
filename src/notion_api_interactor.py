from typing import Optional

import requests
from requests import RequestException


def make_md_from_block(block):
    """Convert a Notion block to Markdown."""
    b_type = block["type"]
    full_text = ""

    try:
        rich_text = block[b_type]["rich_text"]
        if rich_text:
            full_text = "".join([item["plain_text"] for item in rich_text])
        else:
            return "No text provided"
    except KeyError:
        pass  # image found

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
            return f"```\n{full_text}\n```\n\n"
        case "image":
            return "[IMAGE]"

    return full_text + "\n"


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
