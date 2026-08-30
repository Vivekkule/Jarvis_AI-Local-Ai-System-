import requests
from tools.browser import browse_url, search_web
from tools.code_runner import run_python_code
from tools.files import read_file, write_file, list_folder
from memory import remember, recall

OLLAMA_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = """You are Jarvis, a personal AI assistant.

IMPORTANT: You have a real web search tool available. When the user asks about:
- Current news, recent events, latest information
- Anything that changes over time (prices, weather, scores)
- Topics you are unsure about

You MUST search the web first. To trigger a search, include this EXACTLY in your reply:
[SEARCH: your search query here]

Example: if asked "what is the latest news in AI", reply with:
[SEARCH: latest AI news 2025]
Then I will give you the results and you summarize them.

For coding tasks, write clean code with markdown code blocks.
Think step by step. Be concise but thorough."""

def handle_tool_calls(reply: str) -> str:
    lines = reply.split("\n")
    results = []
    for line in lines:
        if "[TOOL: search_web]" in line:
            query = line.split("]", 1)[-1].strip()
            results.append(f"Search result:\n{search_web(query)}")
        elif "[TOOL: browse_url]" in line:
            url = line.split("]", 1)[-1].strip()
            results.append(f"Page content:\n{browse_url(url)}")
        elif "[TOOL: run_code]" in line:
            code = line.split("]", 1)[-1].strip()
            results.append(f"Code output:\n{run_python_code(code)}")
        elif "[TOOL: read_file]" in line:
            path = line.split("]", 1)[-1].strip()
            results.append(f"File content:\n{read_file(path)}")
        elif "[TOOL: write_file]" in line:
            parts = line.split("]", 1)[-1].strip().split("|", 1)
            if len(parts) == 2:
                results.append(write_file(parts[0].strip(), parts[1].strip()))
        elif "[TOOL: list_folder]" in line:
            path = line.split("]", 1)[-1].strip()
            results.append(f"Files:\n{list_folder(path)}")
    return "\n".join(results)

def ask_jarvis(user_input: str, history: list) -> str:
    # Add relevant memories to context
    memories = recall(user_input, n=2)
    if memories:
        mem_text = "Remembered context: " + " | ".join(memories)
        history.append({"role": "system", "content": mem_text})
    
    history.append({"role": "user", "content": user_input})
    
    response = requests.post(OLLAMA_URL, json={
        "model": "llama3.1",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history
        ],
        "stream": False,
        "options": {"num_gpu": 35, "num_ctx": 4096}
    })
    
    reply = response.json()["message"]["content"]
    
    # Handle any tool calls in the reply
    tool_results = handle_tool_calls(reply)
    if tool_results:
        history.append({"role": "assistant", "content": reply})
        history.append({"role": "user",
                        "content": f"Tool results:\n{tool_results}\nPlease give your final answer."})
        response2 = requests.post(OLLAMA_URL, json={
            "model": "llama3.1",
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *history],
            "stream": False,
            "options": {"num_gpu": 35, "num_ctx": 4096}
        })
        reply = response2.json()["message"]["content"]
    
    history.append({"role": "assistant", "content": reply})
    remember(f"User asked: {user_input}. Jarvis replied: {reply[:200]}")
    return reply

if __name__ == "__main__":
    history = []
    print("\n  Jarvis online with tools. Type 'exit' to quit.\n")
    while True:
        user = input("You: ").strip()
        if not user: continue
        if user.lower() in ["exit","quit","bye"]:
            print("Jarvis: Goodbye."); break
        print("Jarvis: thinking...")
        reply = ask_jarvis(user, history)
        print(f"\nJarvis: {reply}\n")