# Local AI Chat & Benchmark Lab

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/LLM-Ollama-black)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Mode](https://img.shields.io/badge/Mode-Local%20%26%20Offline-2E8B57)

A lightweight local AI chat application and model benchmark. A browser-based interface sends prompts to a small Python web server, which serves the site and forwards chat requests to an Ollama instance running on your machine or in Docker.

Once Ollama and the required models are installed, chat inference runs locally. No third-party cloud AI API is used.

## Table of Contents

- [Overview & Key Highlights](#overview--key-highlights)
- [System Architecture](#system-architecture)
- [Repository Structure](#repository-structure)
- [Models & Benchmark](#models--benchmark)
- [Quick Start](#quick-start)
  - [Option 1: Windows Ollama + Python Web Server](#option-1-windows-ollama--python-web-server)
  - [Option 2: Docker Compose](#option-2-docker-compose)
- [Running the Benchmark Script](#running-the-benchmark-script)
- [Offline Usage](#offline-usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Privacy & Limitations](#privacy--limitations)
- [License](#license)

## Overview & Key Highlights

- **Local inference:** Chat requests are sent to Ollama, not to a hosted AI API.
- **Simple web stack:** Static HTML, CSS, and JavaScript served by a Python standard-library HTTP server.
- **Same-origin API proxy:** The browser calls the local web server, which forwards requests to Ollama. This avoids browser cross-origin restrictions when accessing the chat page.
- **Two deployment options:** Connect to Ollama installed on Windows, or run the web app and Ollama as Docker Compose services.
- **Model selection:** Choose `hermes3` or `qwen2.5:3b` in the interface.
- **Response timing:** Each completed answer displays its elapsed response time.
- **Persistent Docker models:** The Compose configuration stores Ollama model data in a named Docker volume.

## System Architecture

### Windows Ollama

```text
+----------------------- Host machine ------------------------+
|                                                              |
|  Browser                                                     |
|    | http://localhost:8000                                   |
|    v                                                         |
|  Python web server (server.py)                               |
|    | serves HTML/CSS/JS                                      |
|    | proxies POST /api/chat                                  |
|    v                                                         |
|  Ollama on Windows (http://localhost:11434)                  |
|    |                                                         |
|    +--> hermes3                                              |
|    +--> qwen2.5:3b                                           |
|                                                              |
+--------------------------------------------------------------+
```

### Docker Compose

```text
+------------------------ Host machine ------------------------+
|                                                               |
|  Browser                                                      |
|    | http://localhost:8000                                    |
|    v                                                          |
|  web container (Python / server.py)                           |
|    | http://ollama:11434                                      |
|    v                                                          |
|  ollama container                                             |
|    |                                                          |
|    +--> Local models in the ollama_data Docker volume         |
|                                                               |
+---------------------------------------------------------------+
```

## Repository Structure

```text
.
├── app.py                 # Command-line model response-time benchmark
├── docker-compose.yml     # Web and Ollama services
├── Dockerfile             # Container image for the web server
├── index.html             # Chat interface and model selector
├── script.js              # Browser chat requests and response rendering
├── server.py              # Static web server and Ollama API proxy
└── style.css              # Chat interface styles
```

## Models & Benchmark

The web interface offers these Ollama model names:

| Model | Ollama name | Description |
| --- | --- | --- |
| Hermes 3 | `hermes3` | Local chat model |
| Qwen 2.5 3B | `qwen2.5:3b` | Smaller local chat model |

The separate `app.py` script sends the same short Thai prompt to `hermes3` and `qwen2.5:3b`, prints each response and elapsed time, then reports which request was faster in that run. This is a simple, single-run timing comparison; it is not a standardized quality or performance evaluation.

## Quick Start

Choose **one** deployment option. Both options serve the site at `http://localhost:8000`.

### Option 1: Windows Ollama + Python Web Server

#### Requirements

- Windows
- Python 3
- Ollama for Windows
- The Ollama models you intend to use

#### 1. Install and prepare Ollama

Start the Ollama application, or start its server from PowerShell:

```powershell
ollama serve
```

Keep that terminal open if you started Ollama this way. Check the local Ollama API:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

Download the models used by this project while connected to the internet:

```powershell
ollama pull hermes3
ollama pull qwen2.5:3b
```

You only need to download a model once. Ollama keeps downloaded models on the machine.

#### 2. Start the web server

Open another PowerShell window and change to the project directory. Update the path if you put the project somewhere else:

```powershell
cd "C:\Users\User\OneDrive\Desktop\ai-project-main"
python server.py
```

The server prints the web address and the Ollama URL it will use.

#### 3. Open the chat

Visit [http://localhost:8000](http://localhost:8000), select an installed model, type a prompt, and press **Send** or Enter.

To stop the web server, focus its PowerShell window and press `Ctrl+C`. To stop Ollama, close its application or stop the terminal running `ollama serve`.

### Option 2: Docker Compose

#### Requirements

- Docker Desktop, running
- Docker Compose
- Enough disk space for the Docker images and downloaded models

#### 1. Start both services

From PowerShell in the project directory:

```powershell
cd "C:\Users\User\OneDrive\Desktop\ai-project-main"
docker compose up -d --build
```

This builds the web image and starts the `web` and `ollama` services.

#### 2. Download models into the Ollama container

On the first run, download the models into the Compose-managed Ollama service:

```powershell
docker compose exec ollama ollama pull hermes3
docker compose exec ollama ollama pull qwen2.5:3b
```

Model files are stored in the `ollama_data` named volume and remain available when the containers are stopped and restarted.

#### 3. Open the chat and manage services

Visit [http://localhost:8000](http://localhost:8000). Check service status or stop the stack with:

```powershell
docker compose ps
docker compose down
```

`docker compose down` stops and removes the containers but keeps the named model volume. Start them again with:

```powershell
docker compose up -d
```

> Do not run the Windows Ollama server and the Compose Ollama service at the same time if both need host port `11434`. Pick one deployment option to avoid a port conflict.

## Running the Benchmark Script

The benchmark script uses the Ollama API at `http://localhost:11434`. With Windows Ollama running and both models downloaded, run:

```powershell
python app.py
```

If using Docker Compose, run the script from a Python installation on the host while the Ollama container is running and its port `11434` is published:

```powershell
python app.py
```

The script prints both model responses, elapsed time, and a speed comparison for that run. Results can vary with hardware, model load state, and other system activity.

## Offline Usage

The application can be used without an internet connection **after** the required software, Docker images (if using Docker), and Ollama models have been downloaded.

For offline chat:

1. Start Ollama (or the Compose services).
2. Start the web server (or use the Compose web service).
3. Open `http://localhost:8000`.

The browser, web server, and model inference communicate with local services. Initial installation and downloading models or container images require internet access.

## Configuration

`server.py` reads the following environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama base URL used by the web server |
| `HOST` | `127.0.0.1` | Address on which the web server listens |
| `PORT` | `8000` | Web server port |

Example PowerShell configuration:

```powershell
$env:OLLAMA_URL = "http://localhost:11434"
$env:HOST = "127.0.0.1"
$env:PORT = "8000"
python server.py
```

The Compose configuration sets `OLLAMA_URL` to `http://ollama:11434` so the web container can reach Ollama by its Compose service name.

## Troubleshooting

### The chat does not work when opening `index.html`

Do not open the HTML file directly with a `file://` URL. Start the Python server or Docker Compose and open `http://localhost:8000` instead.

### The web server cannot use port 8000

Another process may already be using that port. Stop the other server, or choose a different port:

```powershell
$env:PORT = "8001"
python server.py
```

Then open `http://localhost:8001`.

### The web app cannot connect to Ollama

- Confirm that Ollama is running.
- For Windows Ollama, check `http://localhost:11434/api/tags` in PowerShell.
- For Docker Compose, check `docker compose ps` and inspect logs with `docker compose logs ollama`.
- Confirm `OLLAMA_URL` points to the correct address. Inside Compose, use `http://ollama:11434` for the Ollama service.

### Ollama reports that a model is missing

List the models available to Windows Ollama:

```powershell
ollama list
```

For Compose Ollama:

```powershell
docker compose exec ollama ollama list
```

Download a missing model using `ollama pull <model-name>` for Windows Ollama, or `docker compose exec ollama ollama pull <model-name>` for Compose. Model downloads require internet access.

### The first answer is slow

The first request can take longer while Ollama loads a model into memory. Response time also depends on the model, available system memory, and CPU/GPU performance.

## Privacy & Limitations

- Prompts are sent to the Ollama instance configured for this app; this project does not call a third-party cloud AI API.
- The current chat page sends only the latest prompt with each request. Previous messages shown in the browser are not included as conversation context.
- The “พร้อมใช้งาน” status badge is currently a static display, not a live Ollama health check. If Ollama is unavailable, an error appears after sending a message.
- `app.py` is a separate command-line benchmark, not a benchmark page in the web interface.
- For security, the default Python server binds to `127.0.0.1`. The Docker configuration binds inside the container and publishes the web service on host port `8000`.

## License

No license file is currently included. Unless a license is added, the repository does not grant the standard permissions associated with an open-source license.

