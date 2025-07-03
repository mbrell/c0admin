import base64
import os
from google import genai
from google.genai import types
import threading
import itertools
import sys
import time
import requests
import webbrowser
import pyperclip
from colorama import init, Fore, Style

def ensure_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    env_path = ".env"
    if not api_key:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.strip().split("=", 1)[1]
                        break
        if not api_key:
            api_key = input("Enter your GEMINI_API_KEY: ").strip()
            with open(env_path, "a") as f:
                f.write(f"GEMINI_API_KEY={api_key}\n")
    os.environ["GEMINI_API_KEY"] = api_key
    return api_key

def delete_api_key():
    env_path = ".env"
    if os.path.exists(env_path):
        os.remove(env_path)
    os.environ.pop("GEMINI_API_KEY", None)
    print("API key deleted.")

def spinner(stop_event):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        sys.stdout.write('\rLoading... ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 20 + '\r')

def print_ascii():
    print(Fore.CYAN + r"""
  ▄▖   ▌   ▘  
▛▘▛▌▀▌▛▌▛▛▌▌▛▌
▙▖█▌█▌▙▌▌▌▌▌▌▌                              
    """ + Style.RESET_ALL)

def log_history(answer):
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(f"{answer}\n")

def generate():
    print_ascii()
    api_key = ensure_api_key()
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY environment variable.")
    client = genai.Client(
        api_key=api_key,
    )

    while True:
        question = input("> ")
        if question.strip() == "/del":
            delete_api_key()
            return
        elif question.strip() == "/exit":
            print("Exiting...")
            return
        elif question.strip() == "/history":
            if not os.path.exists("history.txt"):
                print("No history found.")
                continue
            os.system("cat history.txt")
            continue
        elif question.strip() == "/help":
            webbrowser.open("https://github.com/mbrell/c0admin")
            print("Opening help documentation..")  
            continue

        SYSTEM_INSTRUCTION_URL_MBRELL = "https://raw.githubusercontent.com/mbrell/c0admin/refs/heads/main/system-instructions.txt"
        try:
            resp = requests.get(SYSTEM_INSTRUCTION_URL_MBRELL, timeout=5)
            resp.raise_for_status()
            system_instruction_text = resp.text
        except Exception as e:
            raise ValueError(f"Failed to fetch system instruction: {e} [ERROR_CODE:42]")

        model = "gemini-2.0-flash-lite"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=question),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=[
                types.Part.from_text(text=system_instruction_text),
            ],
        )

        stop_event = threading.Event()
        t = threading.Thread(target=spinner, args=(stop_event,))
        t.start()

        answer_text = ""
        try:
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                stop_event.set()
                t.join()
                print(chunk.text, end="")
                answer_text += chunk.text
                pyperclip.copy(answer_text)
        except Exception as e:
            if "API key not valid" in str(e):
                print("\nAPI key not valid. Please check your GEMINI_API_KEY or type /del to reset.")
            else:
                print("An error occurred:", str(e))
        finally:
            log_history(answer_text)
            stop_event.set()
            t.join()

if __name__ == "__main__":
    generate()