# 3. Docker: Commands & Docker Compose

Категория: Docker & Kubernetes
Статус: Проверено

[](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAB1klEQVR4AWIYBaMA0G4ZQEQQRGE4QkUqSUTsm+3kZveuTjuzdUGXihIQJ5ACiUqVKoQCIkgJKRQlVFIUIBJAKhEBCAAFpKKu3ibds+3OFXDYYdzxvvn32/cGmxWrutoq4yBHDLAGTGbXuuu8SkQ4Ez0cxNgXo9U3AyTyvbLC0ACY1e3k4ZlBrludlm4VKwUMJo8w/IPskxjESjCgDfcNraW3fOBgTyeTyVwnI8LqagyQp96seDaYWDaMRKGPgNhzHzJA3OHvu3cg4ZjcN0G2I/+UicV95dmNUKi+CO37OJNrCKV+HWTiHutL+LAJA8QccueubrzRzmB9Hf9P4bkZ5A9pHTO21OMAueF6w12veZuaGPwtKi+c++RmuS5bsf76zaUiWgNX3AdrOD0G+eh0RyFLZ55yLqsfi/VFMt5ZhYAYIqE76m7ZA6T1tyo2oslGMtLjP3ZAzCkFdNlCBA5UbE1VYzl5scscRatGfwR0e1wVGgXZRO7Ktoo1zXgpGe21UoC0avIfAlv/ELgKBAKBQCAQCAR8wTDYvWlQ9Gf4dogR2RUVm8BvCuRevvkzXzAU6sjD4HnO7IV4ZbzAFyQdQ9FVrlkVmdiwLrs4yM2obkVzsmUFK1ifInKCpHb+66kAAAAASUVORK5CYII=)

[](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAMFBMVEVHcExfn7xfn7xfn7xfn7z+//+Puc5ZnLre6vCkxda60+Dv9fjO3+h7rsZqpcBQmLfQ5/9SAAAABHRSTlMAy3M67HfsvAAAASBJREFUOI2FUwmSgzAMozTx7eT/v11Rrg1lFzEDAYtYlp1pAuZXucFrnla876Ir3g/xlfFfvBTkHz9wy+F9nkZ9TEmMR7Zd6ZGBl6sXzeRMXVhbjn2Rat3cTUIp2hE/CZ2iiloFw0prVwKTmYdUS8GNKL926BbkUT+Qqv2qgUl9i7tXFaM2EFCdh9cNGiDwQGhBkrITxKLpSChd/IhXrO0oY0thofXEYgTnqCFQ4y7CA4Vq8lAFhO9h1BGmpjT40CBBYRJMcCEyRZJxh0QjJAJ2ehLdGIWsAiuUCI34NRNHs2Dd4rZQb0vvvwmMfmn2rnp2ciQULYaZIS63BPzfliYzlb8IhT7mtSthH1r+GugPXtexv2J+PjjPR+/x8D4c/x+lPxUzghXNtgAAAABJRU5ErkJggg==)

[](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAArElEQVR4AWOgKriTFsoIxHFAzEeuAV1A/B+IHwOxH6mamYH4M9gABF4DxJKkGBIMxI/QDHkPxIkg7xFrCA/UK7/RDNoBxPKkuEYHiA+hGfIJiDNBriElVhpBmtFwDrEGKAHxPmTN0IB2IKSRDYirgfgbmuY9QKxISLMzEN9A0/gBiFNBXiKUDpZh8e8WIJYh1s/3kTS+AOIIUlNjKBD/BOK5QCxIbn4QYKAnAADIN8Egyaf95gAAAABJRU5ErkJggg==)

Команды Docker — это основной способ управления контейнерами, образами, сетями и томами, включающий команды для управления жизненным циклом (`run`, `start`, `stop`, `kill`, `rm`), управления образами (`pull`, `build`, `rmi`), инспектирования (`ps`, `logs`, `inspect`), а также Dockerfile директивы (`FROM`, `RUN`, `CMD`, `COPY`) для создания образов, и Docker Compose для управления мультиконтейнерными приложениями (`up`, `down`). Они позволяют упаковывать, запускать и масштабировать приложения в изолированных средах (контейнерах). 

### Список команд в docker CLI

1. Docker Hub Account
- `docker login` – Login to your account. You must login before you can push images. Logging in also helps you avoid hitting public pull rate limits.
- `docker logout` – Logs you out of your account.
- `docker search nginx` – Searches Docker Hub for images matching the supplied search term (`nginx`, in this example).
1. General commands
- `docker version` – Displays detailed information about your Docker CLI and daemon versions.
- `docker system info` – Lists data about your Docker environment, including active plugins and the number of containers and images on your system.
- `docker help` – View the help index, a reference of all the supported commands.
- `docker <command> --help` – View the help information about a particular command, including detailed information on the supported option flags.
1. Biuld Images
- `docker build .` – Build the Dockerfile in your working directory into a new image.
- `docker build -t example-image:latest .` – Build the Dockerfile in your working directory and tag the resulting image as `example-image:latest`.
- `docker build -f docker/app-dockerfile` – Build the Dockerfile at the `docker/app-dockerfile` path.
- `docker build --build-arg foo=bar .` – Build an image and set the `foo` [build argument](https://docs.docker.com/engine/reference/commandline/build/#build-arg) to the value bar.
- `docker build --pull .` – Instructs Docker to pull updated versions of the images referenced in FROM instructions in your Dockerfile, before building your new image.
- `docker build --quiet .` – Build an image without emitting any output during the build. The image ID will still be emitted to the terminal when the build completes.
1. Run containers
- `docker run example-image:latest` – Run a new container using the `example-image:latest` image. The output from the container’s foreground process will be shown in your terminal.
- `docker run --rm example-image:latest` – The `--rm` flag instructs Docker to automatically remove the container when it exits instead of allowing it to remain as a stopped container.
- `docker run -d example-image:latest` – Detaches your terminal from the running container, leaving the container in the background.
- `docker run -it example-image:latest` – Attaches your terminal’s input stream and a TTY to the container. Use this command to run interactive commands inside the container.
- `docker run --name my-container example-image:latest` – Names the new container `my-container`.
- `docker run --hostname my-container example-image:latest` – Set the container’s hostname to a specific value (it defaults to the container’s name).
- `docker run --env foo=bar example-image:latest` – Set the value of the `foo` environment variable inside the container to `bar`.
- `docker run --env-file config.env example-image:latest` – Populate environment variables inside the container from the file `config.env`. The file should contain key-value pairs in the format `foo=bar`.
- `docker run -p 8080:80 example-image:latest` – Bind port 8080 on your Docker host to
- `docker run -v data:/data example-image:latest` – Mount the [named Docker volume](https://spacelift.io/blog/docker-volumes) called `data` to `/data` inside the container.
- `docker run --network my-network example-image:latest` – Connect the new container to the Docker network called `my-network`.
- `docker run --restart unless-stopped example-image:latest` – Set the container to start automatically when the Docker daemon starts, unless the container has been manually stopped. Other [restart policies](https://docs.docker.com/config/containers/start-containers-automatically) are also supported.
- `docker run --privileged example-image:latest` – Run the container with [privileged access](https://docs.docker.com/engine/reference/run/#security-configuration) to the host system. This should usually be disabled to maintain security.
1. Manage containers
- `docker ps` – List all the containers currently running on your host.
- `docker ps -a` – List *every* container on your host, including stopped ones.
- `docker attach <container>` – Attach your terminal to the foreground process of the container with the ID or name `<container>`.
- `docker commit <container> new-image:latest` – Save the current state of `<container>` to a new image called `new-image:latest`.
- `docker inspect <container>` – Obtain all the information Docker holds about a container, in JSON format.
- `docker kill <container>` – Send a `SIGTERM` (reuest to correct stoping), after that `SIGKILL`signal to the foreground process running in a container, to force it to stop.
- `docker rename <container> my-container` – Rename a specified container to `my-container`.
- `docker pause <container>` and `docker unpause <container>` – Pause and unpause the processes running within a specific container.
- `docker stop <container>` – Stop a running container.
- `docker start <container>` – Start a previously stopped container.
- `docker rm <container>` – Delete a container by its ID or name. Use the `-f` (force) flag to delete a container that’s currently running.
1. Copy to and From Containers
- `docker cp example.txt my-container:/data` – Copy example.txt from your host to `/data` inside the `my-container` container.
- `docker cp my-container:/data/example.txt /demo/example.txt` – Copy `/data/example.txt` out of the `my-container` container, to `/demo/example.txt` on your host.
1. Execute Commands in Containers

`docker exec my-container demo-command` – Run `demo-command` inside `my-container`; the process’ output will be shown in your terminal

`docker exec -it my-container demo-command` – Run a command interactively by attaching your terminal’s input stream and a pseudo-TTY.

1. Access Container Logs
- `docker logs <container>` – This command streams the existing log output from a container into your terminal window, then exits.
- `docker logs <container> --follow` – This variation emits all existing logs, then continues to stream new logs into your terminal as they’re stored.
- `docker logs <container> -n 10` – Get the last 10 logs from a container.
- `docker stats <container>` – Stream a container’s resource utilization information into your terminal. The output includes CPU, memory, and I/O usage, as well as the number of processes running within the container.
1. Manage Images
- `docker images` – List all stored images.
- `docker rmi <image>` – Delete an image by its ID or tag. Deletion of images which have multiple tags must be forced using the -f flag.
- `docker tag <image> example-image:latest` – Add a new tag (`example-image:latest`) to an existing image (`<image>`).
- `docker push example.com/user/image:latest` – Push an image from your Docker host to a remote registry. The image is identified by its tag, which must reference the registry you’re pushing to.
- `docker pull example.com/user/image:latest` – Manually pull an image from a remote registry to make it available on your host.
- `docker save <IMAGE_NAME>:<TAG> > image.tar`- Save Docker image into .tar-file
- `docker load < image.tar` (or `docker load --input image.tar`). - Load docker images from .tar-file into local Docker library.
1. Manage Networks & Volumes
- `docker create network my-network` – Create a new network called `my-network`; it will default to using the `bridge` driver.
- `docker create network my-network -d host` – Use the `-d` flag to select an alternative driver, such as `host`.
- `docker network connect <network> <container>` – Connect a container to an existing network.
- `docker network disconnect <network> <container>` – Remove a container from a network it’s currently connected to.
- `docker network ls` – List all the Docker networks available on your host, including built-in networks such as `bridge` and `host`.
- `docker network rm <network>` – Delete a network by its ID or name. This is only possible when there are no containers currently connected to the network.
- `docker volume create my-volume` – Create a new named volume called `my-volume`.
- `docker volume ls` – List the volumes present on your host.
- `docker volume rm` – Delete a volume, which will destroy the data within it. The volume must not be used by any container.
1. Scan for Vulnerabilities
- `docker scan example-image:latest` – Scan for vulnerabilities in the image tagged `example-image:latest`. The results will be shown in your terminal.
- `docker scan example-image:latest --file Dockerfile` – The `--file` argument supplies the path to the Dockerfile that was used to build the image. When the Dockerfile is available, more detailed vulnerability information is produced.
- `docker scan example-image:latest --severity high` – Only report vulnerabilities that are `high` severity or higher. The `--severity` flag also supports `low` and `medium` values.
1. Clean Up Unused Resources
- `docker system prune` – Removes unused data, including dangling image layers (images with no tags).
- `docker system prune -a` – Extends the prune process by deleting all unused images, instead of only dangling ones.
- `docker system prune --volumes` – Includes volume data in the prune process. This will delete any volumes that aren’t used by a container.
- `docker image prune` – Removes dangling images, without affecting any other types of data.
- `docker image prune -a` – Removes all unused images.
- `docker network prune` – Removes unused networks.
- `docker volume prune` – Removes unused volumes.
- `docker system df` – Reports your Docker installation’s total disk usage.

The `prune` commands will prompt you to confirm your intentions before any resources are deleted. You can disable the prompt by setting the `-f` (force) flag.

### Dockerfile commands

| `ADD` | Add local or remote files and directories. |
| --- | --- |
| `ARG` | Use build-time variables. |
| `CMD` | Specify default commands. |
| `COPY` | Copy files and directories. |
| `ENTRYPOINT` | Specify default executable. |
| `ENV` | Set environment variables. |
| `EXPOSE` | Describe which ports your application is listening on. |
| `FROM` | Create a new build stage from a base image. |
| `HEALTHCHECK` | Check a container's health on startup. |
| `LABEL` | Add metadata to an image. |
| `MAINTAINER` | Specify the author of an image. |
| `ONBUILD` | Specify instructions for when the image is used in a build. |
| `RUN` | Execute build commands. |
| `SHELL` | Set the default shell of an image. |
| `STOPSIGNAL` | Specify the system call signal for exiting a container. |
| `USER` | Set user and group ID. |
| `VOLUME` | Create volume mounts. |
| `WORKDIR` | Change working directory. |

### Работа EXPOSE

`EXPOSE` в Docker — это инструкция в `Dockerfile`, которая документирует, какие порты внутри контейнера будут прослушивать сетевые соединения (например, 80 для веб-сервера). Сама по себе она не открывает порты наружу, а служит лишь информацией для пользователя образа, облегчая связь между контейнерами в одной сети или для последующего использования с ключом `-p` или `-P` при запуске `docker run` для публикации портов на хост-машину. 

### Разница между EXPOSE и PORTS

`EXPOSE` в Docker сообщает, какие порты контейнер *использует* для внутренней связи (между контейнерами) и документирует их, но не делает их доступными извне; а [**PORTS](https://www.google.com/search?client=opera&q=PORTS&sourceid=opera&ie=UTF-8&oe=UTF-8&ved=2ahUKEwi4xYDS0MKRAxUHHxAIHdrVMpQQgK4QegQIARAC) (или [-p](https://www.google.com/search?client=opera&q=-p&sourceid=opera&ie=UTF-8&oe=UTF-8&ved=2ahUKEwi4xYDS0MKRAxUHHxAIHdrVMpQQgK4QegQIARAD)/[publish](https://www.google.com/search?client=opera&q=publish&sourceid=opera&ie=UTF-8&oe=UTF-8&ved=2ahUKEwi4xYDS0MKRAxUHHxAIHdrVMpQQgK4QegQIARAE)) — это механизм, который реально открывает порт контейнера на хост-машине, делая его доступным для внешнего мира**. `EXPOSE` — это «информация», а `PORTS` — «действие», создающее мост между хостом и контейнером.

**EXPOSE**

- **Назначение:** Объявляет, что приложение внутри контейнера слушает определенный порт (например, веб-сервер на порту 80).
- **Видимость:** Порты, объявленные через `EXPOSE`, доступны только для других контейнеров в той же Docker-сети.
- **Функция:** Документация и подсказка для Docker и других сервисов, не открывает порт наружу.
- **Пример:** `EXPOSE 80`

**PORTS (или `-p` в `docker run`, `ports` в `docker-compose`)**

- **Назначение:** Создает сопоставление (mapping) между портом на хост-машине и портом внутри контейнера.
- **Видимость:** Делает порт контейнера доступным извне хост-системы.
- **Функция:** Реальное открытие порта для взаимодействия с внешним миром, например, для доступа через браузер.
- **Пример:** `docker run -p 8080:80 my-image` (порт 8080 хоста -> порт 80 контейнера).

### **Как ARG и FROM работают вместе?**

![image.png](image%20622.png)

### **Разница между CMD и RUN**

`RUN` выполняется во время сборки образа (создает новый слой), а `CMD` задает команду по умолчанию, которая запускается при старте контейнера из этого образа, и может быть переопределена при запуске через `docker run`, в отличие от `ENTRYPOINT`, который сложнее переопределить.

[**RUN**](https://www.google.com/search?client=opera&q=RUN&sourceid=opera&ie=UTF-8&oe=UTF-8&mstk=AUtExfC8aAEFGLmoP9db6FffDUhn11x5FzRcrd_SEPn6I8qduuXpbObOjRkyAjOz8Bq4bL2MZ0wF50TL4un2M7xYD_q63b7MpEgf-K1CZhLpIPq2Pa04ttsMgh8IudVZm7y6ROcTPyG8YsjRkrgzpQL_vpG7D00dk0ZQusJDmSWRNVxFtV4&csui=3&ved=2ahUKEwi1s9X41ryRAxX2EhAIHaVgK4UQgK4QegQIAhAA)

- **Когда**: Во время сборки Docker-образа (инструкция в `Dockerfile`).
- **Что делает**: Выполняет команды, устанавливает пакеты, компилирует код, создает новый слой в образе.
- **Пример**: `RUN apt-get update && apt-get install -y nginx`.

[**CMD**](https://www.google.com/search?client=opera&q=CMD&sourceid=opera&ie=UTF-8&oe=UTF-8&mstk=AUtExfC8aAEFGLmoP9db6FffDUhn11x5FzRcrd_SEPn6I8qduuXpbObOjRkyAjOz8Bq4bL2MZ0wF50TL4un2M7xYD_q63b7MpEgf-K1CZhLpIPq2Pa04ttsMgh8IudVZm7y6ROcTPyG8YsjRkrgzpQL_vpG7D00dk0ZQusJDmSWRNVxFtV4&csui=3&ved=2ahUKEwi1s9X41ryRAxX2EhAIHaVgK4UQgK4QegQIBBAA)

- **Когда**: При запуске контейнера из образа (команда по умолчанию).
- **Что делает**: Определяет основную команду, которая будет выполнена, если при запуске контейнера не указана другая команда.
- **Переопределение**: Легко переопределяется аргументами, переданными в `docker run`.
- **Пример**: `CMD ["nginx", "-g", "daemon off;"]`.

**Ключевое отличие**

`RUN` — для **построения** образа, `CMD` — для **запуска** контейнера из образа.

`RUN` — это как установка ПО в операционной системе, а `CMD` — это то, что запускается автоматически при «включении» контейнера.

### **Разница между CMD и ENTRYPOINT**

1. При запуске Dockerfile нет ни одной из этих команд - сообщение об ошибке.

![image.png](image%20623.png)

1. Если определена одна из инструкций - `CMD` и `ENTRYPOINT` будут иметь одинаковый эффект. Разница будет только в метаданных контейнеров.

![image.png](image%20624.png)

1. Для CMD и ENTRYPOINT существуют режимы shell и exec.

![image.png](image%20625.png)

Однако режим exec является рекомендуемым. Это связано с тем, что контейнеры задуманы так, чтобы содержать один процесс. Например, отправленные в контейнер сигналы перенаправляются процессу, запущенному внутри контейнера с идентификатором PID, равным 1.

1. Аргументы CMD могут присоединиться к концу инструкции ENTRYPOINT иногда:

![image.png](image%20626.png)

- Если вы используете режим *shell* для `ENTRYPOINT`, `CMD` игнорируется.
- При использовании режима *exec* для `ENTRYPOINT` аргументы `CMD` добавляются в конце.
- При использовании режима *exec* для инструкции `ENTRYPOINT` необходимо использовать режим *exec* и для инструкции `CMD`. Если этого не сделать, Docker попытается добавить `sh -c` в уже добавленные аргументы, что может привести к некоторым непредсказуемым результатам.
1. Инструкции `ENTRYPOINT` и `CMD` могут быть переопределены с помощью флагов командной строки.

Флаг `--entrypoint` может быть использован, чтобы переопределить инструкцию `ENTRYPOINT`:

![image.png](image%20627.png)

Все, что следует после названия образа в команде `docker run`, переопределяет инструкцию `CMD`:

![image.png](image%20628.png)

### Так когда что использовать?

- Используйте `ENTRYPOINT`, если вы не хотите, чтобы разработчики изменяли исполняемый файл, который запускается при запуске контейнера. Вы можете представлять, что ваш контейнер – *исполняемая оболочка*. Хорошей стратегией будет определить *стабильную* комбинацию параметров и исполняемого файла как `ENTRYPOINT`. Для нее вы можете (не обязательно) указать аргументы `CMD` по умолчанию, доступные другим разработчикам для переопределения.
- Используйте только `CMD` (без определения `ENTRYPOINT`), если требуется, чтобы разработчики могли легко переопределять исполняемый файл. Если точка входа определена, исполняемый файл все равно можно переопределить, используя флаг `--entrypoint`. Но для разработчиков будет гораздо удобнее добавлять желаемую команду в конце строки `docker run`.

### **Разница между COPY и ADD**

Основная разница: `COPY` копирует локальные файлы и папки в образ Docker, будучи более прозрачным и рекомендуемым способом, в то время как `ADD` делает то же самое, но также умеет скачивать файлы по URL и автоматически распаковывать локальные `tar`-архивы, что делает его менее предсказуемым и обычно не рекомендуется к использованию. 

Docker рекомендует использовать `COPY` для простоты, а `ADD` — только в случае необходимости авто-распаковки или загрузки по URL, но с осторожностью. 

### Docker Compose

Docker Compose — это инструмент для определения и запуска многоконтейнерных Docker-приложений; он позволяет описать все сервисы (контейнеры, сети, тома) вашего приложения в одном YAML-файле (обычно docker-compose.yml ) и управлять ими с помощью одной команды, например, docker compose up.

Он значительно упрощает разработку и тестирование, автоматизируя запуск и взаимодействие нескольких сервисов (например, веб-сервера, базы данных и кеша).

Ключевые особенности:

- Конфигурация в YAML: Все настройки (образы, порты, переменные окружения, зависимости) прописываются в файле `docker-compose.yml`.
- Управление стеком: Позволяет запускать, останавливать и перестраивать все сервисы приложения одновременно, учитывая их зависимости.
- Изолированные сети: Автоматически создает отдельную сеть для каждого проекта, позволяя контейнерам обращаться друг к другу по именам сервисов.
- Упрощение развертывания: Идеально подходит для создания воспроизводимых сред разработки и тестирования, минимизируя «работает у меня» проблемы.

### Команды Docker Compose

**Основные команды**

- [docker compose up](https://www.google.com/search?q=docker+compose+up&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIAxAB&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp): Запускает приложение, создает контейнеры, сети и тома.
    - [docker compose up -d](https://www.google.com/search?q=docker+compose+up+-d&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIAxAD&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp): Запускает в фоновом режиме (detached).
    - [docker compose up --build](https://www.google.com/search?q=docker+compose+up+--build&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIAxAF&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp): Пересобирает образы перед запуском.
- [docker compose down](https://www.google.com/search?q=docker+compose+down&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIAxAH&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp): Останавливает и удаляет контейнеры, сети и тома, созданные командой `up`.
    - [docker compose down -v](https://www.google.com/search?q=docker+compose+down+-v&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIAxAJ&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp): Удаляет тома (volumes) вместе с контейнерами.
- [docker compose stop](https://www.google.com/search?q=docker+compose+stop&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIAxAL&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp): Останавливает работающие контейнеры без их удаления.
- [docker compose start](https://www.google.com/search?q=docker+compose+start&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIAxAN&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp): Запускает ранее остановленные контейнеры.
- [docker compose restart](https://www.google.com/search?q=docker+compose+restart&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIAxAP&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp): Перезапускает контейнеры.
- [docker compose ps](https://www.google.com/search?q=docker+compose+ps&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIAxAR&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp): Отображает состояние контейнеров (аналогично `docker ps`).
- [docker compose logs](https://www.google.com/search?q=docker+compose+logs&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIAxAT&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp): Выводит журналы (логи) сервисов.
- [docker compose build](https://www.google.com/search?q=docker+compose+build&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIAxAV&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp): Собирает или пересобирает образы из Dockerfile.
- [docker compose pull](https://www.google.com/search?q=docker+compose+pull&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIAxAX&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp): Загружает последние версии образов.

**Команды для выполнения команд**

- [docker compose exec <имя_сервиса> <команда>](https://www.google.com/search?q=docker+compose+exec+%3C%D0%B8%D0%BC%D1%8F_%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%B0%3E+%3C%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%B0&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIBRAB&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp&mstk=AUtExfB7-AeAF8rDuuuc0q59QQXcte0QpJxVXpJGGXjBqLYu-T46R82zdCmr7yIMGkbpjsi3l6Rv9Ot02Y9cGImaddqt9F0r4X9RW7TVIioYimSpboVQtiFHqOpDQMNrIEuoXtwN4SRmMpDm9PSn8iKWSX_zLOq6mqjfzAtnorJVv1eI0ZbwhAJ-GtRHocHa0FYyqZg5-QZYv0H4YvBPCQoiGpVuNnH_6xPtIYnqnm8gzFMF2TG4fdGHCxm5mhrDinQP_G3Rn_-uWOrqz-a2zaqK6Lm6Whr8L__RJX6PgXlzSDQFSQ&csui=3): Выполняет команду в запущенном контейнере.
    - *Пример:* `docker compose exec web bash` (откроет shell в контейнере `web`).
- [docker compose run <имя_сервиса> <команда](https://www.google.com/search?q=docker+compose+run+%3C%D0%B8%D0%BC%D1%8F_%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%B0%3E+%3C%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%B0&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIBRAE&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp&mstk=AUtExfB7-AeAF8rDuuuc0q59QQXcte0QpJxVXpJGGXjBqLYu-T46R82zdCmr7yIMGkbpjsi3l6Rv9Ot02Y9cGImaddqt9F0r4X9RW7TVIioYimSpboVQtiFHqOpDQMNrIEuoXtwN4SRmMpDm9PSn8iKWSX_zLOq6mqjfzAtnorJVv1eI0ZbwhAJ-GtRHocHa0FYyqZg5-QZYv0H4YvBPCQoiGpVuNnH_6xPtIYnqnm8gzFMF2TG4fdGHCxm5mhrDinQP_G3Rn_-uWOrqz-a2zaqK6Lm6Whr8L__RJX6PgXlzSDQFSQ&csui=3): Запускает одноразовую команду в новом контейнере сервиса.

**Дополнительные команды**

- [docker compose config](https://www.google.com/search?q=docker+compose+config&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIBxAB&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp&mstk=AUtExfB7-AeAF8rDuuuc0q59QQXcte0QpJxVXpJGGXjBqLYu-T46R82zdCmr7yIMGkbpjsi3l6Rv9Ot02Y9cGImaddqt9F0r4X9RW7TVIioYimSpboVQtiFHqOpDQMNrIEuoXtwN4SRmMpDm9PSn8iKWSX_zLOq6mqjfzAtnorJVv1eI0ZbwhAJ-GtRHocHa0FYyqZg5-QZYv0H4YvBPCQoiGpVuNnH_6xPtIYnqnm8gzFMF2TG4fdGHCxm5mhrDinQP_G3Rn_-uWOrqz-a2zaqK6Lm6Whr8L__RJX6PgXlzSDQFSQ&csui=3): Проверяет и отображает скомпилированную конфигурацию Compose.
- [docker compose rm](https://www.google.com/search?q=docker+compose+rm&client=opera&hs=jJy&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifMc-R2uVCYlmUl-cRtQR_ClGCktZQ%3A1765905670753&ei=BpVBaZ3ZLer_wPAP7c2noAU&ved=2ahUKEwjP9eD-z8KRAxWxJRAIHerKA1cQgK4QegQIBxAD&uact=5&oq=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B+docker+compose&gs_lp=Egxnd3Mtd2l6LXNlcnAiHdCa0L7QvNCw0L3QtNGLIGRvY2tlciBjb21wb3NlMgUQABiABDIGEAAYBRgeMgYQABgIGB4yBhAAGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI1B5QjgFYix1wBHgBkAEAmAF6oAGuB6oBBDExLjG4AQPIAQD4AQGYAgygAoYFwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAgYQABgHGB7CAggQABgHGAoYHsICBBAjGCfCAgoQABiABBhDGIoFwgIIEAAYBRgHGB7CAggQABgHGAgYHsICBxAAGIAEGA2YAwCIBgGQBgmSBwIxMqAHqGOyBwE4uAf2BMIHBTAuNS43yAcngAgA&sclient=gws-wiz-serp&mstk=AUtExfB7-AeAF8rDuuuc0q59QQXcte0QpJxVXpJGGXjBqLYu-T46R82zdCmr7yIMGkbpjsi3l6Rv9Ot02Y9cGImaddqt9F0r4X9RW7TVIioYimSpboVQtiFHqOpDQMNrIEuoXtwN4SRmMpDm9PSn8iKWSX_zLOq6mqjfzAtnorJVv1eI0ZbwhAJ-GtRHocHa0FYyqZg5-QZYv0H4YvBPCQoiGpVuNnH_6xPtIYnqnm8gzFMF2TG4fdGHCxm5mhrDinQP_G3Rn_-uWOrqz-a2zaqK6Lm6Whr8L__RJX6PgXlzSDQFSQ&csui=3): Удаляет остановленные контейнеры.

Способ достижения того, чтобы контейнер запускался после того, как запуститься другой контейнер - использование depends_on в docker-compose.yml-файле.

### Директивы docker-compose.yml

- **`version`**: Указывает версию синтаксиса `docker-compose.yml` (например, '3.8').
- **`services`**: Главный раздел, где описываются ваши микросервисы (контейнеры).
    - **`image`**: Имя образа для сборки (например, `nginx`, `mysql:latest`).
    - **`build`**: Путь к папке с Dockerfile для сборки образа.
    - **`ports`**: Проброс портов из контейнера на хост-машину (например, `"8080:80"`).
    - **`environment`**: Переменные окружения (ключ-значение).
    - **`volumes`**: Монтирование файлов/папок или именованных томов в контейнер.
    - **`depends_on`**: Указывает порядок запуска сервисов (зависимость одного от другого).
    - **`container_name`**: Желаемое имя для контейнера.
- **`volumes`**: Глобальное определение именованных томов для постоянного хранения данных.
- **`networks`**: Глобальное определение пользовательских сетей для связи сервисов.
- [**extends**](https://www.google.com/search?q=extends&client=opera&hs=HGJ&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifP7U-kYnX3J94kRcAFmXC1AWelLIQ%3A1765906734287&ei=LplBaeGjEeKpwPAPncn_-Ak&ved=2ahUKEwiciPGv08KRAxVaKRAIHZo1Fb0QgK4QegQIAxAM&uact=5&oq=%D0%92%D1%81%D0%B5+%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82%D0%B8%D0%B2%D1%8B+%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B8+docker-compose.yml&gs_lp=Egxnd3Mtd2l6LXNlcnAiOdCS0YHQtSDQtNC40YDQtdC60YLQuNCy0Ysg0LLQvdGD0YLRgNC4IGRvY2tlci1jb21wb3NlLnltbDIIEAAYgAQYogQyCBAAGIAEGKIEMgUQABjvBTIIEAAYgAQYogQyCBAAGIAEGKIESO4vULMHWNIucAh4AJABAJgBhwGgAfAPqgEEOC4xMrgBA8gBAPgBAZgCGaAChQ7CAgsQABiABBiwAxiiBMICDBAhGKABGMMEGAoYKsICChAhGKABGMMEGArCAggQIRigARjDBJgDAIgGAZAGBZIHBTEzLjEyoAfPT7IHBDUuMTK4B-0NwgcEMC4yNcgHKoAIAA&sclient=gws-wiz-serp): Позволяет расширять конфигурацию из другого файла.
- [**profiles**](https://www.google.com/search?q=profiles&client=opera&hs=HGJ&sca_esv=cf3d8fcadb69d60c&sxsrf=AE3TifP7U-kYnX3J94kRcAFmXC1AWelLIQ%3A1765906734287&ei=LplBaeGjEeKpwPAPncn_-Ak&ved=2ahUKEwiciPGv08KRAxVaKRAIHZo1Fb0QgK4QegQIAxAO&uact=5&oq=%D0%92%D1%81%D0%B5+%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82%D0%B8%D0%B2%D1%8B+%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B8+docker-compose.yml&gs_lp=Egxnd3Mtd2l6LXNlcnAiOdCS0YHQtSDQtNC40YDQtdC60YLQuNCy0Ysg0LLQvdGD0YLRgNC4IGRvY2tlci1jb21wb3NlLnltbDIIEAAYgAQYogQyCBAAGIAEGKIEMgUQABjvBTIIEAAYgAQYogQyCBAAGIAEGKIESO4vULMHWNIucAh4AJABAJgBhwGgAfAPqgEEOC4xMrgBA8gBAPgBAZgCGaAChQ7CAgsQABiABBiwAxiiBMICDBAhGKABGMMEGAoYKsICChAhGKABGMMEGArCAggQIRigARjDBJgDAIgGAZAGBZIHBTEzLjEyoAfPT7IHBDUuMTK4B-0NwgcEMC4yNcgHKoAIAA&sclient=gws-wiz-serp): Фильтрация сервисов для запуска (например, только `development` или `production`).