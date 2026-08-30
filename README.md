# JARVIS — Personal AI Assistant

> A fully local, free alternative to ChatGPT. An autonomous AI assistant with real-time web search, code execution, long-term memory, and a Jarvis-style UI — running entirely on your own GPU using open-source models. No API keys. No cost. No limits.

---

## Demo

![JARVIS UI](C:\Users\vivek\jarvis-ai\image.png)

> Dark-themed Jarvis-style web interface with real-time chat, voice input, model switching, and live web search.

---

## Features

- **Real-time Web Search** — automatically searches the internet for every query and returns live results
- **Local LLM Engine** — runs open-source models (Llama 3.1, DeepSeek Coder V2, Mistral, Phi3) via Ollama on your own GPU
- **Code Execution** — writes and runs Python code in a sandboxed environment, returns output
- **File Management** — reads, writes, and organizes files on your laptop
- **Long-term Memory** — stores context across sessions using ChromaDB vector database and Sentence Transformers
- **Voice Input** — speak your questions using browser-based speech recognition
- **Beautiful Web UI** — Jarvis-inspired dark interface with animated elements, model switcher, quick action buttons, and session stats
- **Multi-model Routing** — switch between models mid-conversation for different task types
- **Zero API Cost** — 100% free, runs offline after initial model download

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Models | Llama 3.1 8B/13B, DeepSeek Coder V2, Mistral, Phi3 |
| Model Runtime | Ollama (CUDA accelerated) |
| Backend | Python, Flask, Flask-CORS |
| Web Search | DuckDuckGo scraping (no API key) |
| Browser Automation | Playwright, urllib |
| Memory / Vector DB | ChromaDB, Sentence Transformers |
| Frontend | HTML, CSS, JavaScript (vanilla) |
| Code Execution | Python subprocess sandbox |
| Voice | Web Speech API |

---

## System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB+ |
| GPU VRAM | 4 GB | 6 GB+ |
| Storage | 10 GB free | 20 GB+ free |
| OS | Windows 10/11 | Windows 11 |
| Python | 3.11+ | 3.11+ |
| Node.js | 18+ | 20+ |

> This project was built and tested on: **Ryzen 5 5500H · RTX 3050 4GB · 64GB RAM**

---

## Project Structure

```
jarvis-ai/
├── server.py              # Flask backend — API routes, search engine, Ollama bridge
├── index.html             # Frontend — Jarvis-style web UI
├── main.py                # Core agent loop — chat, memory, tool routing
├── memory.py              # Long-term memory — ChromaDB + Sentence Transformers
├── jarvis.py              # Voice mode launcher
├── tools/
│   ├── __init__.py
│   ├── browser.py         # Web search + URL scraping
│   ├── code_runner.py     # Python code execution sandbox
│   └── files.py           # File read/write/list operations
├── jarvis_memory_db/      # Auto-created — ChromaDB persistent storage
└── venv/                  # Python virtual environment
```

---

## Installation

### Step 1 — Install Ollama
Download from [https://ollama.com](https://ollama.com) and install it.

### Step 2 — Pull AI Models
```bash
# Main brain (required)
ollama pull llama3.1

# Coding specialist (recommended)
ollama pull deepseek-coder-v2

# Fast lightweight model (recommended)
ollama pull phi3:mini
```

### Step 3 — Clone the Repository
```bash
git clone https://github.com/yourusername/jarvis-ai.git
cd jarvis-ai
```

### Step 4 — Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 5 — Install Dependencies
```bash
pip install flask flask-cors requests
pip install chromadb sentence-transformers
pip install playwright SpeechRecognition pyttsx3
python -m playwright install chromium
```

---

## Running JARVIS

You need **two terminals** open at the same time.

**Terminal 1 — Start Ollama:**
```bash
ollama serve
```

**Terminal 2 — Start JARVIS:**
```bash
cd jarvis-ai
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux
python server.py
```

**Then open your browser:**
```
http://localhost:5000
```

---

## One-Click Launch (Windows)

Create a file called `start_jarvis.bat` in your project folder:

```bat
@echo off
echo Starting JARVIS AI...
start "Ollama" cmd /k "ollama serve"
timeout /t 3
call venv\Scripts\activate
echo Opening browser...
start http://localhost:5000
python server.py
```

Double-click `start_jarvis.bat` to launch everything at once.

---

## How It Works

```
User types a message
        │
        ▼
Flask server receives request
        │
        ▼
Web search runs automatically (DuckDuckGo)
        │
        ▼
Search results injected into AI context
        │
        ▼
Ollama runs local LLM (Llama 3.1 / DeepSeek)
        │
        ▼
AI reads search results + answers question
        │
        ▼
Response shown in browser UI
        │
        ▼
Conversation saved to ChromaDB memory
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serves the web UI |
| `/api/chat` | POST | Main chat endpoint — searches web + queries LLM |
| `/api/status` | GET | Check if Ollama is running + list available models |
| `/api/search` | POST | Direct web search |
| `/api/run-code` | POST | Execute Python code and return output |

---

## Usage Examples

**General Questions**
```
What is the latest news in India today?
Who won the IPL match today?
Current Bitcoin price
```

**Coding Help**
```
Write a Python script to rename all files in a folder
Debug this error: [paste your error]
Build a REST API with Flask and SQLite
```

**Research**
```
Explain how transformers work in deep learning
Summarize the latest developments in AI
Compare React vs Vue for a beginner
```

**Task Planning**
```
Plan a full-stack web project for my portfolio
Create a study schedule for DSA in 30 days
```

---

## Models Guide

| Model | Best For | Speed | Size |
|---|---|---|---|
| `phi3:mini` | Quick answers, simple tasks | ⚡⚡⚡ Fast | 2.3 GB |
| `llama3.1` | General purpose, good quality | ⚡⚡ Medium | 4.9 GB |
| `llama3.1:13b` | Complex reasoning (needs 16GB+ RAM) | ⚡ Slow | 8.0 GB |
| `deepseek-coder-v2` | Coding tasks, debugging | ⚡⚡ Medium | 9.0 GB |
| `mistral` | Fast reasoning, research | ⚡⚡ Medium | 4.1 GB |

---

## Troubleshooting

**Ollama error / cannot connect**
```bash
# Make sure ollama is running
ollama serve
```

**Request timed out**
- Switch to `phi3:mini` in the model dropdown for faster responses
- Increase timeout in `server.py`: change `timeout=300` to `timeout=600`

**No search results**
```bash
# Test search directly
python -c "from tools.browser import search_web; print(search_web('test'))"
```

**ModuleNotFoundError: tools.browser**
```bash
# Create missing __init__.py
New-Item tools\__init__.py -ItemType File
```

**Model not appearing in dropdown**
```bash
ollama list   # see installed models
ollama pull llama3.1   # pull if missing
```

---

## Future Improvements

- [ ] Streaming responses (word by word output)
- [ ] Image generation support (Stable Diffusion)
- [ ] File upload and PDF reading
- [ ] Multiple chat sessions / history
- [ ] Plugin system for custom tools
- [ ] Mobile-responsive UI
- [ ] Wake word detection ("Hey Jarvis")
- [ ] Email and calendar integration

---

## Skills Demonstrated

- `Python` `Flask` `REST API design`
- `Large Language Models (LLM)` `Prompt Engineering`
- `RAG (Retrieval Augmented Generation)`
- `Vector Databases` `ChromaDB` `Semantic Search`
- `Web Scraping` `Playwright` `urllib`
- `CUDA / GPU Acceleration`
- `Agent Systems` `Tool Use` `Autonomous AI`
- `HTML` `CSS` `JavaScript`
- `System Design` `Local AI Deployment`

---

## Author

**Vivek**
Computer Engineering Graduate — Data Science Specialization
Pillai College of Engineering, New Panvel

---

## License

MIT License — free to use, modify, and distribute.

---

> Built entirely without paid APIs. Runs free forever on your own hardware.
