import os

def get_file_content(working_directory, file_path):
    try:
        # Construct the absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))

        # Enforce directory boundary
        if not abs_target_file.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if it's a regular file
        if not os.path.isfile(abs_target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read content
        with open(abs_target_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if len(content) > 10000:
            truncated_msg = f'\n[...File "{file_path}" truncated at 10000 characters]'
            return content[:10000] + truncated_msg

        return content

    except Exception as e:
        return f"Error: {str(e)}"