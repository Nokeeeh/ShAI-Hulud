import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

def main():

    parser = argparse.ArgumentParser(description="ShAI-Hulud, the wormiest Python assistant...")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "user", "content": args.user_prompt}
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if response.usage == None:
        raise RuntimeError("failed API request")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
