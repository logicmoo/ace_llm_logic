
import subprocess
import argparse
import openai
import os

def llm_rewrite_to_ace_english(text):
    prompt = f"""Convert the following sentence into active voice, present tense, declarative form, so it can be parsed by ACE controlled English.

Sentence: "{text}"
Rewritten:"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response['choices'][0]['message']['content'].strip()

def parse_with_ace(sentence, ace_path="./ace/bin/ace", grammar_path="./ace/grammars/erg.dat", mock=False):
    if mock:
        return "exists x (report(x) ∧ write(alice, x)).\nexists y (data(y) ∧ review(alice, y) ∧ before(write(alice, x), review(alice, y)))."
    if not os.path.isfile(ace_path):
        return "ERROR: ACE binary not found and mock mode is disabled."
    try:
        result = subprocess.run(
            [ace_path, "-g", grammar_path, "-1", "-T"],
            input=sentence.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.stdout.decode("utf-8")
    except Exception as e:
        return f"ACE parser error: {e}"

def llm_adjust_logic(original, logic):
    prompt = f"""The following original sentence has been rewritten to ACE-compatible English and parsed into logical form. Please revise the logic to reflect the original sentence's tense, aspect, and voice (e.g., past tense, passive voice), while preserving the structure and entities.

Original sentence:
"{original}"

Original ACE-based logic:
{logic}

Revised logic:"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response['choices'][0]['message']['content'].strip()

def process_sentence(sentence, mock=False):
    ace_friendly = llm_rewrite_to_ace_english(sentence)
    ace_logic = parse_with_ace(ace_friendly, mock=mock)
    adjusted_logic = llm_adjust_logic(sentence, ace_logic)
    return adjusted_logic

def main():
    parser = argparse.ArgumentParser(description="Convert English to adjusted logic using ACE and OpenAI")
    parser.add_argument('--file', type=str, help='Input file with English text')
    parser.add_argument('--mock', action='store_true', help='Use mock logic output instead of calling ACE')
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

    openai.api_key = os.getenv("OPENAI_API_KEY")
    result = process_sentence(text.strip(), mock=args.mock)
    print("\n--- Final Adjusted Logic ---")
    print(result)

if __name__ == "__main__":
    main()
