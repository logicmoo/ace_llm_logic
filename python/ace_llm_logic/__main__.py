
import subprocess
import argparse
import time
import os
import socket
from typing import Tuple, Optional
import openai
import requests
from urllib.parse import urlencode, quote_plus


def start_ape_http_server(ape_script: str = os.path.join("APE", "ape.sh")) -> Tuple[subprocess.Popen, int]:
    """Start APE in HTTP mode on a random free port."""
    ape_script = os.path.abspath(ape_script)
    sock = socket.socket()
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    proc = subprocess.Popen(
        [ape_script, "-httpserver", "-port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(ape_script),
    )
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


def _strip_code_fences(text: str) -> str:
    """Return text with surrounding triple backtick fences removed."""
    if text.startswith("```") and text.rstrip().endswith("```"):
        lines = text.strip().splitlines()
        if len(lines) >= 2:
            return "\n".join(lines[1:-1]).strip()
    fence_start = text.find("```")
    fence_end = text.rfind("```")
    if fence_start != -1 and fence_end != -1 and fence_end > fence_start:
        return text[fence_start + 3:fence_end].strip()
    return text.strip()

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
    return _strip_code_fences(response.choices[0].message.content)

def parse_with_ace(sentence: str, endpoint: str, mock: bool = False) -> str:
    """Send the sentence to an APE HTTP server and return the FOL result."""
    if mock:
        return (
            "exists x (report(x) ∧ write(alice, x)).\n"
            "exists y (data(y) ∧ review(alice, y) ∧ before(write(alice, x), review(alice, y)))."
        )
    try:
        # APE's HTTP interface expects spaces encoded as '+' rather than '%20'
        query = urlencode({"text": sentence, "solo": "fol"}, quote_via=quote_plus)
        url = f"http://{endpoint}/?{query}"
        response = requests.get(url, timeout=30)
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
    return _strip_code_fences(response.choices[0].message.content)

def process_sentence(sentence: str, endpoint: str, mock: bool = False) -> str:
    ace_friendly = llm_rewrite_to_ace_english(sentence)
    if mock:
        # Skip OpenAI logic adjustments in mock mode for deterministic tests
        ace_logic = parse_with_ace(ace_friendly, endpoint="localhost:0", mock=True)
        return ace_logic

    ace_logic = parse_with_ace(ace_friendly, endpoint=endpoint)
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

    endpoint = args.use_http_ape
    proc = None
    if not args.mock and endpoint is None:
        proc, port = start_ape_http_server()
        time.sleep(1)
        endpoint = f"localhost:{port}"

    result = process_sentence(text.strip(), endpoint=endpoint, mock=args.mock)

    if proc:
        stop_ape_http_server(proc)

    print("\n--- Final Adjusted Logic ---")
    print(result)

if __name__ == "__main__":
    main()
