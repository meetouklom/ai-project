# Local AI Studio

![Ollama](https://img.shields.io/badge/LLM-Ollama-black?logo=ollama)
![Docker Compose](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JavaScript-E34F26?logo=html5&logoColor=white)
![Inference](https://img.shields.io/badge/Inference-Local%20Ollama-2E8B57)

A lightweight browser chat interface for **Ollama running on your machine**. Send text, attach documents or images, and see the model response time. A separate Python script compares the response times of two text models using one fixed summarization prompt.

The chat page is a static HTML/CSS/JavaScript app. It sends requests **directly from the browser to Ollama**; this project does not include a backend, API proxy, database, or hosted AI service. Docker Compose runs Ollama only—the website is served separately.

## Table of Contents

- [Overview & Key Highlights](#overview--key-highlights)
- [System Architecture](#system-architecture)
- [Repository Structure](#repository-structure)
- [Models](#models)
- [Quick Start](#quick-start)
  - [Option 1: Ollama on Windows](#option-1-ollama-on-windows)
  - [Option 2: Ollama with Docker Compose](#option-2-ollama-with-docker-compose)
  - [Optional: Serve the Website with Nginx](#optional-serve-the-website-with-nginx)
- [Using the Website](#using-the-website)
- [Supported Attachments](#supported-attachments)
- [Benchmark Script](#benchmark-script)
- [Privacy & Limitations](#privacy--limitations)
- [Troubleshooting](#troubleshooting)

## Overview & Key Highlights

- **Local model inference:** The browser sends requests to the Ollama API at `http://localhost:11434/api/chat`.
- **Three selectable models:** `hermes3`, `qwen2.5:3b`, and `llava` (vision).
- **File attachments:** Attach up to five supported files, with a 10 MB limit per file.
- **Light and dark themes:** The selected theme and interface language are saved in browser local storage.
- **Thai and English interface:** Switch the UI language from the sidebar.
- **Response timing:** The chat displays the elapsed time for each completed Ollama request.
- **Separate benchmark:** `app.py` tests `hermes3` and `qwen2.5:3b` with the same fixed summarization prompt.

## System Architecture

```text
+------------------------------- YOUR COMPUTER --------------------------------+
|                                                                               |
|  +----------------------+       Loads website       +----------------------+  |
|  | Browser              | <------------------------ | Static Web Server    |  |
|  | Chat UI and files    |                           | Python http.server   |  |
|  +----------+-----------+                           | or Nginx             |  |
|             |                                       | Serves web files only|  |
|             |                                       +----------------------+  |
|             |                                                                 |
|             | POST /api/chat (direct request)                                 |
|             | Current message + extracted document text + images              |
|             v                                                                 |
|  +-------------------------------+                                            |
|  | Ollama API :11434             |                                            |
|  | Windows app or Docker service |                                            |
|  +---------------+---------------+                                            |
|                  |                                                            |
|                  | Runs the selected model                                    |
|                  v                                                            |
|  +-----------------------------------------------+                            |
|  | Models installed in Ollama                   |                            |
|  | hermes3 / qwen2.5:3b / llava (for images)    |                            |
|  +-----------------------------------------------+                            |
|                                                                               |
|  app.py (separate benchmark) ── POST /api/chat ──> Ollama API                |
|                                                                               |
+-------------------------------------------------------------------------------+

PDF.js / Mammoth are downloaded from cdnjs when needed to read PDF/DOCX files.
Only the parser libraries are downloaded; document contents stay in the browser
until they are sent directly to the local Ollama API.
```

### Request flow

1. The browser loads the static website from Python's built-in HTTP server or Nginx.
2. When you send a message, the browser calls Ollama directly. The static web server does not handle AI requests.
3. Ollama runs the selected model and returns its response to the browser.
4. `app.py` is an independent command-line benchmark; it also calls Ollama directly.

## Repository Structure

| File | Purpose |
| --- | --- |
| `index.html` | Chat layout, model selector, attachment controls, and settings |
| `style.css` | Responsive layout, themes, and component styling |
| `script.js` | Language/theme preferences, file extraction, and direct Ollama API requests |
| `app.py` | One-shot response-time comparison for `hermes3` and `qwen2.5:3b` |
| `docker-compose.yml` | Ollama container, API port, allowed browser origins, and model volume |
| `Dockerfile` | Optional Nginx image for serving the static website only |

## Models

| Model | Ollama name | Use |
| --- | --- | --- |
| Hermes 3 | `hermes3` | Text chat |
| Qwen 2.5 3B | `qwen2.5:3b` | Text chat |
| LLaVA | `llava` | Image understanding; select it before sending image attachments |

Download only the models you plan to use. LLaVA is needed only for images.

## Quick Start

Choose one Ollama setup below. In both cases, the website must also be served from a local HTTP origin. Opening `index.html` with a `file://` URL is not recommended because browser security and Ollama CORS settings may block API requests.

### Option 1: Ollama on Windows

#### 1. Download the models

Open PowerShell in a terminal where Ollama is installed:

```powershell
ollama pull hermes3
ollama pull qwen2.5:3b
ollama pull llava
```

Skip `ollama pull llava` if you do not need image understanding.

#### 2. Start Ollama with browser access enabled

If Ollama is already running from the system tray, quit it first. Then set the allowed website origins and start the server:

```powershell
$env:OLLAMA_ORIGINS = "http://localhost:8000,http://127.0.0.1:8000,http://localhost:8080,http://127.0.0.1:8080"
ollama serve
```

Keep this terminal open. `OLLAMA_ORIGINS` lets the local browser page call the Ollama API; it does not start a proxy.

#### 3. Serve the website

Open another PowerShell window:

```powershell
cd "C:\Users\User\OneDrive\Desktop\ai-project-main"
python -m http.server --bind 127.0.0.1 8000
```

This serves the static website only.

#### 4. Open the chat

Visit [http://localhost:8000](http://localhost:8000), choose an installed model, then type a message or attach files.

### Option 2: Ollama with Docker Compose

Docker Compose runs **only Ollama**, publishes its API on port `11434`, and stores downloaded models in the `ollama_data` volume.

```powershell
cd "C:\Users\User\OneDrive\Desktop\ai-project-main"
docker compose up -d
docker compose exec ollama ollama pull hermes3
docker compose exec ollama ollama pull qwen2.5:3b
docker compose exec ollama ollama pull llava
```

Skip the LLaVA pull if you do not need image understanding. Then start the website separately using step 3 in [Option 1](#option-1-ollama-on-windows), and open [http://localhost:8000](http://localhost:8000).

Check or stop the Ollama service:

```powershell
docker compose ps
docker compose down
```

Stopping Compose does not delete the `ollama_data` volume. Start the service again with `docker compose up -d`.

### Optional: Serve the Website with Nginx

The Dockerfile builds an Nginx image for the static website. It does **not** run Ollama, configure Ollama, or proxy API requests.

```powershell
docker build -t local-ai-web .
docker run --rm -p 8080:80 local-ai-web
```

Open [http://localhost:8080](http://localhost:8080). Make sure Ollama allows the exact website origin `http://localhost:8080`.

## Using the Website

- **Choose a model:** Select an installed model in the sidebar.
- **Send a message:** Type into the input field and press **Send** or Enter.
- **Use a summary example:** Click a summary prompt to place its text into the input field. These examples do not restrict the model.
- **Attach files:** Click **＋** or drag files onto the message input. Remove an attachment using its **×** button.
- **Change language or theme:** Use the controls in the sidebar. Preferences are saved in the current browser.
- **Check response time:** The completed model response includes the elapsed request time.

## Supported Attachments

The app accepts up to **five files**, each up to **10 MB**. Extracted text is limited to **100,000 characters per file**.

| File types | What happens |
| --- | --- |
| `.txt`, `.md`, `.csv`, `.json`, `.log`, `.xml`, `.html`, `.htm` | Read as text in the browser and included in the Ollama request |
| `.pdf` | PDF.js extracts selectable text in the browser |
| `.docx` | Mammoth extracts text in the browser |
| `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif` | Resized to a maximum 2,048 pixels on the longest side, converted to JPEG, then sent to Ollama |

PDF.js, its PDF worker, and Mammoth are loaded from cdnjs when needed. PDF/DOCX attachments therefore require internet access if the libraries are not already cached. The file contents are extracted in the browser and are **not** uploaded to cdnjs.

Scanned or image-only PDFs are not OCR-processed and may produce no extracted text. Image attachments require the `llava` model to be installed and selected in the model selector.

## Benchmark Script

Run the separate benchmark with Python 3 while Ollama is running and both text models are installed:

```powershell
python app.py
```

`app.py` sends the same fixed Thai summarization prompt once to `hermes3` and once to `qwen2.5:3b`. It prints both responses, the elapsed time for each request, and which request was faster in that run. The timer measures the full HTTP round trip, including model inference. It is a simple comparison, not a controlled performance test.

The summarization instruction in `test_prompt` applies only to those benchmark requests. It does not fine-tune either model, persist as a model setting, or change the website's chat behavior.

## Privacy & Limitations

- The browser sends the current message and attachments directly to the local Ollama API. This project does not call a hosted AI service.
- Previous chat messages remain visible in the page, but are **not** sent as conversation history with later requests.
- The web chat does not send a system prompt or enforce a summarization-only role. The summary buttons only insert example user text.
- PDF/DOCX parsing libraries are fetched from cdnjs; the document contents are not.
- The status badge describes the direct Ollama connection mode; it is not a live health check.
- Ollama must allow the exact origin used to open the website through its `OLLAMA_ORIGINS` setting.
- The repository does not include a license file.

## Troubleshooting

### The page cannot connect to Ollama

1. Make sure Ollama is running and the selected model is installed.
2. Check the local API at [http://localhost:11434/api/tags](http://localhost:11434/api/tags).
3. Make sure `OLLAMA_ORIGINS` includes the website's exact origin, including hostname and port. For example, `http://localhost:8000` and `http://127.0.0.1:8000` are different origins.
4. Restart Ollama after changing `OLLAMA_ORIGINS`.

### Ollama reports that a model is missing

- Windows Ollama: run `ollama list`.
- Compose Ollama: run `docker compose exec ollama ollama list`.
- Download a model with `ollama pull <model-name>` or `docker compose exec ollama ollama pull <model-name>`.

### An image cannot be summarized

Select **LLaVA · Vision** and install the model with `ollama pull llava` (Windows) or `docker compose exec ollama ollama pull llava` (Compose).

### A PDF or DOCX cannot be read

Connect to the internet so the browser can load PDF.js or Mammoth. Check the file size and extracted text limits. Scanned PDFs may not contain selectable text.

### `python app.py` shows a connection error

Start Ollama, check [http://localhost:11434/api/tags](http://localhost:11434/api/tags), and verify that both `hermes3` and `qwen2.5:3b` are installed.
