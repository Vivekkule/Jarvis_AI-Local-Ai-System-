import subprocess, tempfile, os, sys

def run_python_code(code: str) -> str:
    with tempfile.NamedTemporaryFile(
        suffix=".py", delete=False,
        mode="w", encoding="utf-8"
    ) as f:
        f.write(code)
        temp_path = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.expanduser("~")
        )
        output = result.stdout or result.stderr or "(no output)"
        return output[:3000]
    except subprocess.TimeoutExpired:
        return "Error: Code timed out after 30 seconds"
    except Exception as e:
        return f"Error: {e}"
    finally:
        os.unlink(temp_path)

if __name__ == "__main__":
    result = run_python_code("print(2 + 2)\nprint('Hello from Jarvis!')")
    print(result)