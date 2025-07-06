import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types



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
system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
model_name = "gemini-2.0-flash-001"

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]


client = genai.Client(api_key=api_key)
#client.models.generate_content("gemini-2.0-flash-001","Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")

#response = client.models.generate_content(
#    model='gemini-2.0-flash-001',
#    contents=[prompt]
#)

#response = client.models.generate_content(
#    model="gemini-2.0-flash-001",
#    contents=messages,
#)

response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)




print(response.text)
if verbose:
    print("\n--- Verbose Output ---")
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")