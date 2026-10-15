import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

def main():

    parser = argparse.ArgumentParser(description="ShAI-Hulud, the wormiest Python assistant...")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    verbose = args.verbose

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt}
    ]

    loop = 1

    for l in range(20):

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in response.choices[0].message.tool_calls:
                result_message = call_function(tool_call, verbose)
                messages.append(result_message)
                if not result_message["content"]:
                    raise Exception("No content")
                if args.verbose:
                    print(f"-> {result_message['content']}")

        if not message.tool_calls:
            print(message.content)
            break

        if response.usage == None:
            raise RuntimeError("failed API request")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")

        loop += 1
        if loop == 20:
            print("Maximum number of iterations has been reached without finding a proper answer. Exiting...")
            sys.exit(1)


if __name__ == "__main__":
    main()
