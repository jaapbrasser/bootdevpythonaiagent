import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from functions.agent_executor import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if len(sys.argv) < 2:
    print("Usage: python main.py '<your prompt here>'")
    sys.exit(1)

verbose = False
args = sys.argv[1:]
if '--verbose' in args:
    verbose = True
    args.remove('--verbose')

prompt = " ".join(args)

system_prompt = """
You are a helpful AI coding agent.

Your job is to interpret user requests and choose from the following function calls:

- get_files_info: Lists files and directories. Requires: directory (string)
- get_file_content: Reads file contents. Requires: file_path (string)
- run_python_file: Executes a Python script. Requires: file_path (string). This must be a relative path ending in '.py'.
- write_file: Writes to a file. Requires: file_path (string), content (string)

Paths must always be relative to the working directory. Always provide all required arguments in function calls.
"""
client = genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-001",
    tools=[genai.types.Tool(function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ])],
    system_instruction=system_prompt
)

# Conversation loop setup
messages = [{"role": "user", "parts": [prompt]}]



max_iterations = 20
for i in range(max_iterations):
    if verbose:
        print(f"\n--- Iteration {i + 1} ---")

    response = model.generate_content(messages)
    
    if not response.candidates:
        print("No candidates returned.")
        break

    function_called = False
    for candidate in response.candidates:
        content = candidate.content
        messages.append(content)

        for part in content.parts:
            if hasattr(part, "function_call"):
                fn_call = part.function_call
                if not fn_call.name:
                    print("⚠️  function_call_part.name is empty or None")
                    continue

                function_call_result = call_function(fn_call, verbose=verbose)
                messages.append(function_call_result)
                function_called = True
                break  # One tool call per iteration

        if not function_called:
            # No tool call, assume final LLM message
            if verbose:
                print("Final response:")
            for part in content.parts:
                if hasattr(part, "text"):
                    print(part.text)
            break

    if not function_called:
        break
