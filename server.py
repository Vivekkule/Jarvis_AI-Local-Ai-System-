from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests, os, sys, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, static_folder=".")
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = """You are Jarvis, a personal AI assistant with real-time internet access.

You will ALWAYS receive fresh web search results before answering.
Your job is to:
1. Read the search results carefully
2. Extract the most relevant and accurate information
3. Give a clear, direct, conversational answer in plain text
4. Never say "I don't have access to the internet" — you always do
5. Never say "as of my knowledge cutoff" — you have live results
6. If search results are not relevant, answer from your own knowledge
7. Keep answers concise but complete
8. For code tasks, use proper code blocks
9. Always mention the source or context of information when useful"""

def build_query(text: str) -> str:
    """Clean up user message into a good search query."""
    remove = [
        "can you", "could you", "please", "jarvis", "hey", "hi",
        "tell me", "show me", "find me", "give me", "i want to know",
        "do you know", "what do you think about", "help me with"
    ]
    q = text.strip()
    low = q.lower()
    for r in remove:
        low = low.replace(r, "")
    # keep original casing but use cleaned version
    return low.strip() or text.strip()

def do_search(query: str) -> str:
    """Always search and return results as text."""
    try:
        from tools.browser import search_and_browse
        results = search_and_browse(query)
        if results and len(results) > 50:
            return results
        # fallback
        from tools.browser import search_web
        return search_web(query)
    except Exception as e:
        try:
            from tools.browser import search_web
            return search_web(query)
        except Exception as e2:
            return f"Search unavailable: {e2}"

@app.route("/api/chat", methods=["POST"])
def chat():
    data     = request.get_json()
    messages = data.get("messages", [])
    model    = data.get("model", "llama3.1")

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    user_text = messages[-1]["content"]

    # Always search for every message
    query = build_query(user_text)
    print(f"\n  [SEARCHING]: {query}")
    search_results = do_search(query)
    print(f"  [GOT RESULTS]: {len(search_results)} chars")

    # Inject search results into context
    enriched_input = f"""Here are live web search results for the query "{query}":

{search_results}

---
Now answer this question using the search results above:
{user_text}

Give a clear, direct answer in plain conversational text."""

    # Build message list with enriched input
    final_messages = list(messages[:-1])  # all previous messages
    final_messages.append({"role": "user", "content": enriched_input})

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                *final_messages
            ],
            "stream": False,
            "options": {
                "num_gpu": 35,
                "num_ctx": 8192,
                "temperature": 0.7
            }
        }, timeout=300)

        if response.status_code != 200:
            return jsonify({"error": f"Ollama error {response.status_code}"}), 500

        reply = response.json()["message"]["content"]
        print(f"  [REPLY]: {reply[:100]}...")
        return jsonify({"reply": reply, "searched": query})

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to Ollama. Run: ollama serve"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Try phi3:mini for faster responses"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/status", methods=["GET"])
def status():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        if r.ok:
            models = [m["name"] for m in r.json().get("models", [])]
            return jsonify({"status": "online", "models": models})
        return jsonify({"status": "offline", "models": []})
    except:
        return jsonify({"status": "offline", "models": []})


@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json()
    try:
        from tools.browser import search_and_browse
        return jsonify({"result": search_and_browse(data.get("query", ""))})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/run-code", methods=["POST"])
def run_code():
    data = request.get_json()
    try:
        from tools.code_runner import run_python_code
        return jsonify({"result": run_python_code(data.get("code", ""))})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  JARVIS WEB SERVER — ALWAYS ONLINE MODE")
    print("="*50)
    print("  Every message searches the web automatically")
    print("  Open browser: http://localhost:5000")
    print("="*50 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=False)