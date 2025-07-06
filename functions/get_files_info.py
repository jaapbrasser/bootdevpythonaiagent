# functions/get_files_info.py
import os
import google.generativeai as genai
from google.generativeai import types



def get_files_info(working_directory, directory=None):
    try:
        # Build the full path
        target_directory = os.path.join(working_directory, directory or ".")

        # Resolve to absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(target_directory)

        # Enforce directory boundaries
        if not abs_target_dir.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Verify it's a directory
        if not os.path.isdir(abs_target_dir):
            return f'Error: "{directory}" is not a directory'

        # List directory contents
        items = []
        for entry in os.listdir(abs_target_dir):
            entry_path = os.path.join(abs_target_dir, entry)
            try:
                size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                items.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                items.append(f"Error: Failed to get info for {entry} - {str(e)}")

        return "\n".join(items)

    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
            }
        },
        "required": ["directory"]
    }
)

