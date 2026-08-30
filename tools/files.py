import os

def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(path: str, content: str) -> str:
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Saved to {path}"
    except Exception as e:
        return f"Error writing file: {e}"

def list_folder(folder: str = ".") -> str:
    try:
        items = os.listdir(folder)
        return "\n".join(items)
    except Exception as e:
        return f"Error: {e}"

def append_file(path: str, content: str) -> str:
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n" + content)
        return f"Appended to {path}"
    except Exception as e:
        return f"Error: {e}"