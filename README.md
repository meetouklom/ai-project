# Local AI Studio

![Ollama](https://img.shields.io/badge/LLM-Ollama-black?logo=ollama)
![Docker Compose](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JavaScript-E34F26?logo=html5&logoColor=white)
![Inference](https://img.shields.io/badge/Inference-Local%20Ollama-2E8B57)

A lightweight browser chat interface for **Ollama running on your machine**. Send text, attach documents or images, and ask for a concise summary with either a simple explanation or an ER diagram in one model response. A separate Python script measures one fixed summarization request to Hermes 3.

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
- [Response-Time Sample](#response-time-sample)
- [Privacy & Limitations](#privacy--limitations)
- [Troubleshooting](#troubleshooting)

## Overview & Key Highlights

- **Local model inference:** The browser sends requests to the Ollama API at `http://localhost:11434/api/chat`.
- **Single-model summaries:** Hermes 3 summarizes and explains text or creates a Mermaid ER diagram in one request.
- **Optional image model:** LLaVA can handle image attachments.
- **File attachments:** Attach up to five supported files, with a 10 MB limit per file.
- **Light and dark themes:** The selected theme and interface language are saved in browser local storage.
- **Thai and English interface:** Switch the UI language from the sidebar.
- **Response timing:** The chat displays the elapsed time for each completed Ollama request.
- **Separate timing sample:** `app.py` sends one fixed summarization prompt to `hermes3`.

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
|             | POST /api/chat (one direct request)                              |
|             | Current message + extracted document text + images               |
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
|  | hermes3 / llava (optional, for images)       |                            |
|  +-----------------------------------------------+                            |
|                                                                               |
|  app.py (separate timing sample) ── POST /api/chat ──> Ollama API            |
|                                                                               |
+-------------------------------------------------------------------------------+

PDF.js / Mammoth are downloaded from cdnjs when needed to read PDF/DOCX files.
Only the parser libraries are downloaded; document contents stay in the browser
until they are sent directly to the local Ollama API.
```

### Request flow

1. The browser loads the static website from Python's built-in HTTP server or Nginx.
2. For each request, the browser sends the source to the selected model through Ollama. The static web server does not handle AI requests.
3. Hermes 3 summarizes the source and produces the selected format in one response. LLaVA can be selected instead when processing images.
4. `app.py` is an independent command-line timing sample; it also calls Ollama directly.

## Repository Structure

| File | Purpose |
| --- | --- |
| `index.html` | Chat layout, model selector, attachment controls, and settings |
| `style.css` | Responsive layout, themes, and component styling |
| `script.js` | Language/theme preferences, file extraction, and direct Ollama API requests |
| `app.py` | One-request response-time sample for `hermes3` |
| `docker-compose.yml` | Ollama container, API port, allowed browser origins, and model volume |
| `Dockerfile` | Optional Nginx image for serving the static website only |

## Models

| Model | Ollama name | Use |
| --- | --- | --- |
| Hermes 3 | `hermes3` | Text and document summaries, simple explanations, or ER diagrams |
| LLaVA | `llava` | Optional image understanding; select it when attaching images |

Install Hermes 3 for text and document summarization. LLaVA is optional and needed only for images.

## Quick Start

Choose one Ollama setup below. In both cases, the website must also be served from a local HTTP origin. Opening `index.html` with a `file://` URL is not recommended because browser security and Ollama CORS settings may block API requests.

### Option 1: Ollama on Windows

#### 1. Download the models

Open PowerShell in a terminal where Ollama is installed:

```powershell
ollama pull hermes3
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

- **Choose a model:** Hermes 3 handles text and documents. Choose LLaVA when sending images.
- **Choose a response format:** Select **Explain in simple language** or **Create an ER diagram**. The selected model creates the summary and requested format in one response.
- **Send a message:** Type into the input field and press **Send** or Enter.
- **Use a summary example:** Click a summary prompt to place its text into the input field. These examples do not restrict the model.
- **Attach files:** Click **＋** or drag files onto the message input. Remove an attachment using its **×** button.
- **Change language or theme:** Use the controls in the sidebar. Preferences are saved in the current browser.
- **Check response time:** Each response includes the elapsed time for its single Ollama request.

An ER diagram is generated as Mermaid `erDiagram` text with an explanation. If the source does not support identifiable entities and relationships, the model is instructed to say so rather than inventing a diagram.

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

## Response-Time Sample

Run the separate response-time sample with Python 3 while Ollama is running and `hermes3` is installed:

```powershell
python app.py
```

`app.py` sends one fixed Thai summarization prompt to `hermes3` and prints the response and elapsed HTTP round-trip time, including model inference. It is a single timing sample, not a controlled performance test.

The summarization instruction in `test_prompt` applies only to that timing-sample request. It does not fine-tune Hermes 3, persist as a model setting, or change the website's chat behavior.

## Privacy & Limitations

- The browser sends the current message and attachments directly to the local Ollama API. This project does not call a hosted AI service.
- Previous chat messages remain visible in the page, but are **not** sent as conversation history with later requests.
- Each web request goes to one selected model. Hermes 3 handles text and documents; image attachments require selecting the installed `llava` model.
- The summary buttons insert example user text; the system prompt guides the model but is not a hard technical restriction or a guarantee that every model will follow it.
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

Start Ollama, check [http://localhost:11434/api/tags](http://localhost:11434/api/tags), and verify that `hermes3` is installed.
