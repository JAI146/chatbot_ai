#!/usr/bin/env python3
"""
SpongeBob CLI Chatbot (multi-turn) for ai.sooners.us using gemma3:4b.

Features
- Uses OpenAI-compatible Chat Completions API: /api/chat/completions
- Loads API creds & config from ~/.soonerai.env
- Maintains and sends full chat history (with truncation)
- Clean Ctrl+C handling, simple errors, and optional transcript save

Usage
    pip install -r requirements.txt
    python spongebob_cli.py
"""

import os
import sys
import json
import time
import signal
import argparse
from typing import List, Dict, Any

import requests
from dotenv import load_dotenv

# ---------- Config & Env ----------

ENV_PATH = os.path.join(os.path.expanduser("~"), ".soonerai.env")
load_dotenv(ENV_PATH)

API_KEY = os.getenv("SOONERAI_API_KEY")
BASE_URL = (os.getenv("SOONERAI_BASE_URL", "https://ai.sooners.us") or "").rstrip("/")
MODEL = os.getenv("SOONERAI_MODEL", "gemma3:4b")

if not API_KEY:
    raise RuntimeError(
        "Missing SOONERAI_API_KEY in ~/.soonerai.env. "
        "Create it in the ai.sooners.us dashboard and try again."
    )

API_URL = f"{BASE_URL}/api/chat/completions"


# ---------- Defaults ----------

DEFAULT_SYSTEM_PROMPT = (
    "You are SpongeBob SquarePants. Talk cheerfully, use underwater/ocean humor, "
    "wholesome optimism, and occasional nautical nonsense. Keep replies concise, "
    "friendly, and squeaky-clean. Stay in character."
)

# Hard cap to avoid giant prompts. 1 system + up to N pairs (user+assistant)
MAX_TURN_PAIRS = 6

# ---------- Helpers ----------

def truncate_history(messages: List[Dict[str, str]], max_pairs: int) -> List[Dict[str, str]]:
    """
    Keep the system message and the last `max_pairs` user/assistant pairs.
    Assumes messages[0] is the system message.
    """
    if not messages:
        return messages
    system = messages[0:1]
    rest = messages[1:]
    # Each pair is 2 messages (user + assistant). We’ll just keep the last 2*max_pairs.
    keep = rest[-2 * max_pairs :]
    return system + keep


def call_chat_api(model: str, messages: List[Dict[str, str]], temperature: float = 0.6, timeout: int = 60) -> str:
    """
    Calls the OpenAI-compatible Chat Completions API and returns assistant text.
    """
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    try:
        resp = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=timeout,
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error: {e}")

    if resp.status_code != 200:
        # Try to surface meaningful JSON error if present
        try:
            details = resp.json()
            msg = details.get("error", {}).get("message") or details
        except Exception:
            msg = resp.text
        raise RuntimeError(f"API error {resp.status_code}: {msg}")

    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError(f"Unexpected API response shape: {json.dumps(data, indent=2)})")


def save_transcript(path: str, messages: List[Dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for m in messages:
            role = m.get("role", "?").upper()
            content = m.get("content", "")
            f.write(f"{role}: {content}\n\n")


def handle_sigint(_signum, _frame):
    print("\n👋 Bye! (Caught Ctrl+C)")
    sys.exit(0)


# ---------- Main CLI ----------

def main():
    parser = argparse.ArgumentParser(description="SpongeBob CLI on ai.sooners.us (gemma3:4b)")
    parser.add_argument("--system", default=DEFAULT_SYSTEM_PROMPT, help="Override the system prompt")
    parser.add_argument("--temp", type=float, default=0.6, help="Sampling temperature (default 0.6)")
    parser.add_argument("--max-pairs", type=int, default=MAX_TURN_PAIRS, help="Max user/assistant pairs to keep")
    parser.add_argument("--save", default="", help="Optional transcript file path to save on exit (e.g., logs/chat.txt)")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, handle_sigint)

    messages: List[Dict[str, str]] = [{"role": "system", "content": args.system}]

    print("🌊 Ahoy! I’m SpongeBob (gemma3:4b on ai.sooners.us). Type 'exit' to quit.\n")

    # Simple REPL
    while True:
        try:
            user = input("You: ").strip()
        except EOFError:
            print("\n👋 Bye!")
            break

        if not user:
            continue
        if user.lower() in {"exit", "quit", ":q"}:
            print("👋 Bye!")
            break

        messages.append({"role": "user", "content": user})
        messages = truncate_history(messages, args.max_pairs)

        try:
            reply = call_chat_api(MODEL, messages, temperature=args.temp)
        except RuntimeError as e:
            print(f"Error: {e}")
            # Leave the last user message in history so you can retry.
            continue

        messages.append({"role": "assistant", "content": reply})
        print(f"SpongeBob: {reply}\n")

    if args.save:
        save_transcript(args.save, messages)
        print(f"📝 Transcript saved to: {args.save}")


if __name__ == "__main__":
    main()
