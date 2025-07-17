
import subprocess
import argparse
import time
import os
import socket
from typing import Tuple, Optional
import openai
import requests


def start_ape_http_server(ape_script: str = os.path.join("APE", "ape.sh")) -> Tuple[subprocess.Popen, int]:
    """Start APE in HTTP mode on a random free port."""
    sock = socket.socket()
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    proc = subprocess.Popen([
        ape_script,
        "-httpserver",
        "-port",
        str(port),
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc, port


def stop_ape_http_server(proc: subprocess.Popen) -> None:
    """Terminate the spawned APE process."""
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


_client: Optional[openai.OpenAI] = None


def get_openai_client() -> openai.OpenAI:
    """Return a cached OpenAI client instance."""
    global _client
    if _client is None:
        _client = openai.OpenAI()
    return _client

def llm_rewrite_to_ace_english(text):
    prompt = f"""Convert the following sentence into active voice, present tense, declarative form, so it can be parsed by ACE controlled English.

Sentence: "{text}"
Rewritten:"""
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def parse_with_ace(sentence: str, endpoint: str, mock: bool = False) -> str:
    """Send the sentence to an APE HTTP server and return the FOL result."""
    if mock:
        return (
            "exists x (report(x) ∧ write(alice, x)).\n"
            "exists y (data(y) ∧ review(alice, y) ∧ before(write(alice, x), review(alice, y)))."
        )
    try:
        response = requests.get(
            f"http://{endpoint}/",
            params={"text": sentence, "solo": "fol"},
            timeout=30,
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"ACE parser error: {e}"

def llm_adjust_logic(original, logic):
    prompt = f"""The following original sentence has been rewritten to ACE-compatible English and parsed into logical form. Please revise the logic to reflect the original sentence's tense, aspect, and voice (e.g., past tense, passive voice), while preserving the structure and entities.

Original sentence:
"{original}"

Original ACE-based logic:
{logic}

Revised logic:"""
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def process_sentence(sentence: str, mock: bool = False, use_http_ape: Optional[str] = None) -> str:
    ace_friendly = llm_rewrite_to_ace_english(sentence)
    if mock:
        ace_logic = parse_with_ace(ace_friendly, endpoint="localhost:0", mock=True)
    else:
        if use_http_ape:
            ace_logic = parse_with_ace(ace_friendly, endpoint=use_http_ape)
        else:
            proc, port = start_ape_http_server()
            # Give the server a moment to start
            time.sleep(1)
            try:
                ace_logic = parse_with_ace(ace_friendly, endpoint=f"localhost:{port}")
            finally:
                stop_ape_http_server(proc)
    adjusted_logic = llm_adjust_logic(sentence, ace_logic)
    return adjusted_logic

def main():
    parser = argparse.ArgumentParser(description="Convert English to adjusted logic using ACE and OpenAI")
    parser.add_argument('--file', type=str, help='Input file with English text')
    parser.add_argument('--mock', action='store_true', help='Use mock logic output instead of calling ACE')
    parser.add_argument('--use-http-ape', type=str, help='Connect to existing APE HTTP server host:port')
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
    else:
        print("Enter your sentence (Ctrl+D to end):")
        text = ""
        try:
            while True:
                line = input()
                text += line + " "
        except EOFError:
            pass

    result = process_sentence(text.strip(), mock=args.mock, use_http_ape=args.use_http_ape)
    print("\n--- Final Adjusted Logic ---")
    print(result)

if __name__ == "__main__":
    main()
