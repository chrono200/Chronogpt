#!/usr/bin/env python3
import os
import sys
import time
import random
from datetime import datetime
from openai import OpenAI, APIStatusError, APIConnectionError

HOME = os.path.expanduser("~")
CONFIG = os.path.join(HOME, ".config", "chronogpt")
KEYFILE = os.path.join(CONFIG, "api_key")
MODELFILE = os.path.join(CONFIG, "model")

G = "\033[38;5;82m"
C = "\033[38;5;51m"
R = "\033[38;5;196m"
D = "\033[38;5;244m"
W = "\033[38;5;255m"
B = "\033[1m"
RESET = "\033[0m"

def say(color, text=""):
    print(f"{color}{text}{RESET}")

def type_text(text, color=G, delay=0.012):
    sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(RESET + "\n")

def load_model():
    try:
        with open(MODELFILE) as f:
            return f.read().strip() or "openrouter/free"
    except FileNotFoundError:
        return "openrouter/free"

def get_key():
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if key:
        return key
    try:
        with open(KEYFILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        pass

    import getpass
    key = getpass.getpass("Paste OpenRouter API key (hidden): ").strip()
    if not key:
        raise SystemExit("No API key supplied.")

    os.makedirs(CONFIG, exist_ok=True)
    fd = os.open(KEYFILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(key + "\n")
    return key

def banner(model):
    os.system("clear")
    say(G, r"""
   _______ __  ____  ______  _   __  ____  ______
  / ____// / / / __ \/ ____/ / | / / / __ \/ __  /
 / /    / /_/ / /_/ / /     /  |/ / / /_/ / /_/ /
/ /___ / __  / _, _/ /___  / /|  / / ____/ ____/
\____//_/ /_/_/ |_|\____/ /_/ |_/ /_/   /_/
""")
    say(D, "  ─────────────────────────────────────────────")
    say(C, "  [ SYSTEM ]", end="") if False else None
    say(C, "  ◆ CHRONO TERMINAL  //  AI RELAY")
    say(G, "  ◆ STATUS: ONLINE       ◆ MODE: INTERACTIVE")
    say(D, "  ─────────────────────────────────────────────")
    say(G, f"  MODEL   : {model}")
    say(G, "  PROVIDER: OPENROUTER")
    say(D, "  SESSION : VOLATILE MEMORY / NO CHAT LOG")
    say(D, "  Type /help for commands.")
    say(D, "  ─────────────────────────────────────────────\n")

def main():
    args = sys.argv[1:]

    if args and args[0] == "--key-reset":
        try:
            os.remove(KEYFILE)
            say(G, "[OK] Saved API key removed.")
        except FileNotFoundError:
            say(D, "[INFO] No saved key found.")
        return

    if args and args[0] == "--set-model":
        if len(args) < 2:
            say(R, "Usage: chronogpt --set-model MODEL_ID")
            return
        os.makedirs(CONFIG, exist_ok=True)
        with open(MODELFILE, "w") as f:
            f.write(args[1].strip())
        os.chmod(MODELFILE, 0o600)
        say(G, f"[OK] Model set to {args[1]}")
        return

    try:
        client = OpenAI(
            api_key=get_key(),
            base_url="https://openrouter.ai/api/v1",
            timeout=90,
            max_retries=1,
        )
    except Exception as e:
        say(R, f"[BOOT ERROR] {e}")
        return

    if args and args[0] == "--models":
        try:
            for item in client.models.list().data:
                print(item.id)
        except Exception as e:
            say(R, f"Could not list models: {e}")
        return

    model = load_model()
    banner(model)

    history = []
    while True:
        try:
            prompt = input(f"{C}┌─[{G}you{C}@chrono{C}]{RESET}\n{C}└─➤ {W}").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not prompt:
            continue
        if prompt == "/exit":
            type_text("[ SESSION CLOSED ] See you on the other side.", R, 0.01)
            break
        if prompt == "/clear":
            history.clear()
            say(G, "[OK] Conversation memory cleared.")
            continue
        if prompt == "/model":
            say(C, f"[MODEL] {model}")
            continue
        if prompt == "/help":
            say(G, "/clear  Clear session memory")
            say(G, "/model  Show active model")
            say(G, "/exit   Close ChronoGPT")
            say(G, "/help   Show commands")
            continue

        stamp = datetime.now().strftime("%H:%M:%S")
        say(C, f"\n  ◈ YOU // {stamp}")
        say(W, "  " + prompt)
        history.append({"role": "user", "content": prompt})

        say(D, "\n  ◆ Establishing relay...",)
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content":
                     "You are ChronoGPT, a helpful AI and coding assistant. "
                     "Use clear, direct answers. Help with lawful, authorized "
                     "cybersecurity learning. Be honest about uncertainty."},
                    *history,
                ],
                max_tokens=2048,
                stream=True,
            )

            say(G, f"\n  ◈ CHRONOGPT // {datetime.now().strftime('%H:%M:%S')}")
            sys.stdout.write(W)
            answer_parts = []
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta.content
                if delta:
                    sys.stdout.write(delta)
                    sys.stdout.flush()
                    answer_parts.append(delta)
            sys.stdout.write(RESET + "\n\n")
            answer = "".join(answer_parts).strip()
            history.append({"role": "assistant", "content": answer})

        except APIStatusError as e:
            history.pop()
            say(R, f"\n  [RELAY ERROR {e.status_code}] {e.message}")
            if e.status_code == 401:
                say(R, "  Check your OpenRouter API key.")
            elif e.status_code == 402:
                say(R, "  Insufficient credits for this request.")
            elif e.status_code == 429:
                say(R, "  Rate limit hit. Retry later or change model.")
        except APIConnectionError:
            history.pop()
            say(R, "\n  [NETWORK ERROR] Check your internet connection.")
        except Exception as e:
            history.pop()
            say(R, f"\n  [ERROR] {e}")

    say(D, "\n  ChronoGPT offline.\n")

if __name__ == "__main__":
    main()
