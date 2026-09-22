"""Minimal Jev demo via the Vercel AI Gateway.

Jev is TypeSafe AI's "System One" model: instead of chatting, it evaluates a
`state` against typed `questions` and returns structured answers with
confidence. Here we ask it a `choice` question: which item is a fruit?

Run:  python jev_demo.py
Key:  read from ai-gateway.txt (or the AI_GATEWAY_API_KEY env var).
"""
import json
import os

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENDPOINT = "https://ai-gateway.vercel.sh/typesafe/v1/systemone"


def load_key():
    key = os.environ.get("AI_GATEWAY_API_KEY")
    if key:
        return key.strip()
    path = os.path.join(BASE_DIR, "ai-gateway.txt")
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def ask_jev():
    payload = {
        "model": "typesafe-ai/jev",
        # The shared context Jev evaluates. We describe the two candidates.
        "state": "We are shown two items. Item 1 is 'apple'. Item 2 is 'truck'.",
        "questions": {
            # choice → Jev picks the option whose criteria best fit the state
            "fruit": {
                "type": "choice",
                "instructions": "Which item is a fruit?",
                "criteria": {
                    "apple": "the item labelled 'apple'",
                    "truck": "the item labelled 'truck'",
                },
            },
        },
    }
    resp = requests.post(
        ENDPOINT,
        headers={
            "Authorization": "Bearer " + load_key(),
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    data = ask_jev()
    answer = data.get("answers", {}).get("fruit", {})
    print("Question : what is a fruit?  1: apple   2: truck")
    print("Raw answer:", json.dumps(answer))
    # choice answers look like {"type": "choice", "choice": "apple", ...}
    picked = answer.get("choice") or answer.get("value")
    if picked:
        print("Jev says :", picked, "is the fruit.")
    usage = data.get("usage", {})
    if usage:
        print("Tokens   :", usage)


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as e:
        print("HTTP error:", e.response.status_code, e.response.text)
    except FileNotFoundError:
        print("No key found. Put your key in ai-gateway.txt or set AI_GATEWAY_API_KEY.")
