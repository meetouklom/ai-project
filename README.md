เ# Local AI Studio

A small browser-based chat interface for Ollama, with local document and image attachments, plus a separate Python script for comparing two models on a fixed summarization example.

## How it works

```text
Browser (static HTML/CSS/JS)
  ├─ reads supported attachments in the browser
  └─ sends the current request directly to http://localhost:11434/api/chat
       └─ Ollama runs the selected model on this machine
```

There is no Python web server, API proxy, database, account system, or cloud AI service in this project. The browser page and the Ollama API are separate local services. The web page sends only the current message and attachments; earlier messages shown in the chat are not included as context in later requests.

## Project files

| File | Purpose |
| --- | --- |
| `index.html` | Chat interface and model selector |
| `style.css` | Responsive layout, light/dark themes, attachment styling |
| `script.js` | Language/theme preferences, file reading, and direct Ollama API requests |
| `app.py` | Separate one-shot benchmark for `hermes3` and `qwen2.5:3b` |
| `docker-compose.yml` | Runs only Ollama and stores its models in a named volume |
| `Dockerfile` | Optional standalone Nginx image that serves the static website; it does not run Ollama or a proxy |

## Requirements

- Ollama installed on the host, or Docker Desktop with Docker Compose
- Python 3, only if using its built-in static file server or running `app.py`
- `hermes3` and/or `qwen2.5:3b` for text chat
- `llava` for image attachments
- An internet connection the first time PDF/DOCX reader libraries are needed

## Run with Ollama on Windows

1. Download the models you want to use:

   ```powershell
   ollama pull hermes3
   ollama pull qwen2.5:3b
   ollama pull llava
   ```

   `llava` is only needed for images.

2. Allow the local website origins in Ollama. Quit the Ollama tray app first if it is already running, then start Ollama from PowerShell:

   ```powershell
   $env:OLLAMA_ORIGINS = "http://localhost:8000,http://127.0.0.1:8000,http://localhost:8080,http://127.0.0.1:8080"
   ollama serve
   ```

   Leave this terminal running. This setting allows the browser page to call Ollama directly; it does not create a proxy.

3. In another PowerShell window, start a local static server from the project folder:

   ```powershell
   cd "C:\Users\User\OneDrive\Desktop\ai-project-main"
   python -m http.server --bind 127.0.0.1 8000
   ```

4. Open [http://127.0.0.1:8000](http://127.0.0.1:8000). Choose an installed model, type a message, attach files if needed, then press **Send** or Enter.

Opening `index.html` as a `file://` URL is not recommended. A local HTTP origin is needed for the browser-to-Ollama CORS configuration.

## Run Ollama with Docker Compose

From the project folder:

```powershell
docker compose up -d
docker compose exec ollama ollama pull hermes3
docker compose exec ollama ollama pull qwen2.5:3b
docker compose exec ollama ollama pull llava
```

Pull `llava` only if you need image understanding. Compose runs **only the Ollama service**, publishes its API at `localhost:11434`, and stores models in the `ollama_data` volume. It does not run the website.

Start the static website separately using the Python command in the previous section, then open `http://127.0.0.1:8000`. The Compose service allows the listed local website origins through `OLLAMA_ORIGINS`. If you change that setting, recreate Ollama:

```powershell
docker compose up -d --force-recreate ollama
```

Stop the Ollama container with `docker compose down`. Its downloaded models remain in the named volume.

## Optional: serve the website with the Dockerfile

The Dockerfile builds a standalone Nginx image for the static files. It does not start Ollama, configure its CORS policy, or proxy API calls.

```powershell
docker build -t local-ai-web .
docker run --rm -p 8080:80 local-ai-web
```

Open [http://localhost:8080](http://localhost:8080). Make sure the Ollama instance also allows the `http://localhost:8080` origin.

## Attaching files

Click the **＋** button or drag files onto the message box. Up to five files can be attached at once, with a 10 MB per-file limit. Each extracted text document is limited to 100,000 characters.

| File type | What the browser does |
| --- | --- |
| TXT, Markdown, CSV, JSON, LOG, XML, HTML | Reads the file as text |
| PDF | Extracts selectable text using PDF.js |
| DOCX | Extracts text using Mammoth |
| PNG, JPG/JPEG, WEBP, GIF | Resizes to at most 2048 pixels on the longest side, converts to JPEG, and sends it to Ollama |

PDF.js, its PDF worker, and Mammoth are loaded from cdnjs only when a PDF or DOCX is selected. Therefore those file types need internet access the first time they are opened (and after browser cache is cleared). The document contents are extracted in the browser and are not uploaded to the CDN.

Text and image content is sent directly from the browser to the local Ollama API. Image attachments require the `llava` model to be installed and selected in the interface. Scanned/image-only PDFs have no selectable text and are not OCR-processed by this application.

## Chat behavior and model instructions

The web chat sends one Ollama request containing the current message and any attachments. It does **not** send a system prompt, fine-tune a model, or enforce a summarization-only role. The two summary buttons insert example instructions into the message box; they are suggestions, not restrictions on the model.

`app.py` is separate from the web chat. Its `test_prompt` contains a summarization instruction and a fixed sample article; that prompt is sent as a user message to each of the two benchmark models. It applies only to that benchmark request and does not change the model or the website's chat behavior.

## Run the benchmark

With Ollama running and both text models installed, run:

```powershell
python app.py
```

The script sends the same fixed test prompt once to `hermes3` and once to `qwen2.5:3b`, prints each response and elapsed request time, then reports which was faster in that run. The timer measures the full local HTTP request round trip, including model inference. This is a simple comparison, not a controlled benchmark; first-load time and machine load can affect results.

## Troubleshooting

### The page says Ollama could not be reached

- Confirm Ollama is running and the selected model is installed (`ollama list`).
- Open `http://localhost:11434/api/tags` to check that the API responds.
- Check that `OLLAMA_ORIGINS` includes the exact origin used in the browser, including its port (`http://localhost:8000` is different from `http://127.0.0.1:8000`).
- Restart Ollama after changing `OLLAMA_ORIGINS`.

### An image cannot be summarized

Select **LLaVA · Vision** in the model list and install the model with `ollama pull llava` (or `docker compose exec ollama ollama pull llava` when using Compose).

### A PDF or DOCX cannot be read

Connect to the internet so the browser can load PDF.js or Mammoth from cdnjs. PDFs containing scanned pages may require OCR, which this app does not provide.

### `python app.py` returns a connection error

Start Ollama first, check `http://localhost:11434/api/tags`, and verify that both benchmark models have been downloaded.

## Privacy and limitations

- The browser calls the Ollama API at `localhost:11434` directly; Ollama must allow the website's origin through CORS.
- The project does not send prompts or attachment contents to a hosted AI API. PDF/DOCX parser scripts are fetched from cdnjs, but document contents are not sent there.
- The page's “Direct Ollama API” badge is descriptive, not a live health check.
- Chat history remains visible in the current page, but only the latest request is sent to the model.
- The benchmark's summarization prompt does not fine-tune or permanently configure either model.
- No license file is included in this repository.
