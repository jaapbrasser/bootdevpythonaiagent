# functions/write_file.py
import os

def write_file(working_directory, file_path, content):
    try:
        # Resolve full absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if the target path is within the working directory
        if not abs_target_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure parent directories exist
        os.makedirs(os.path.dirname(abs_target_path), exist_ok=True)

        # Write (overwrite) file content
        with open(abs_target_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"
