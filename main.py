import os
import sys
from dotenv import load_dotenv
#from google.genai import types
import google.generativeai as genai
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if len(sys.argv) < 2:
    print("Usage: python main.py '<your prompt here>'")
    sys.exit(1)

verbose = False
args = sys.argv[1:]

# Look for --verbose
if '--verbose' in args:
    verbose = True
    args.remove('--verbose')

# Combine remaining args into a prompt (in case it's multi-word without quotes)
prompt = " ".join(args)

#system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
model_name = "gemini-2.0-flash-001"
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

system_prompt = """
You are a helpful AI coding agent.

Your job is to interpret user requests and choose from the following function calls:

- get_files_info: Lists files and directories. Requires: directory (string)
- get_file_content: Reads file contents. Requires: file_path (string)
- run_python_file: Executes a Python script. Requires: file_path (string). This must be a relative path ending in '.py'.
- write_file: Writes to a file. Requires: file_path (string), content (string)

Paths must always be relative to the working directory. Always provide all required arguments in function calls.
"""

messages = [
    {"role": "user", "parts": [prompt]}
]


available_functions = [genai.types.Tool(function_declarations=[
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
])]

client = genai.configure(api_key=api_key)
#client.models.generate_content("gemini-2.0-flash-001","Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")

#response = client.models.generate_content(
#    model='gemini-2.0-flash-001',
#    contents=[prompt]
#)

#response = client.models.generate_content(
#    model="gemini-2.0-flash-001",
#    contents=messages,
#)

#response = client.models.generate_content(
#    model=model_name,
#    contents=messages,
#    config=types.GenerateContentConfig(system_instruction=system_prompt),
#)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-001",
    tools=available_functions,
    system_instruction=system_prompt  # ✅ just a string
)


response = model.generate_content([
    {"role": "user", "parts": [prompt]}
])


if not response.candidates:
    print("No candidates returned.")
    sys.exit(1)

content = response.candidates[0].content

if not content.parts:
    print("No parts returned in response.")
    sys.exit(1)

first_part = content.parts[0]

if hasattr(first_part, "function_call"):
    fn_call = first_part.function_call
    # ✅ Safely handle missing args
    if fn_call.args:
        args_dict = dict(fn_call.args)
        for k, v in args_dict.items():
            print(v)  # ✅ print values only (e.g. 'main.py', 'hello')
    else:
        print("No arguments provided.")
    print(fn_call.name)
else:
    print("Text response:")
    print(first_part.text)

if verbose:
    print("\n--- Verbose Output ---")
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")