# functions/run_python.py
import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))

        # Guard: directory boundary check
        if not abs_target_file.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Guard: file existence
        if not os.path.isfile(abs_target_file):
            return f'Error: File "{file_path}" not found.'

        # Guard: .py extension
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Run the Python file in subprocess
        result = subprocess.run(
            ["python", abs_target_file],
            capture_output=True,
            text=True,
            cwd=abs_working_dir,
            timeout=30
        )

        output_parts = []

        if result.stdout.strip():
            output_parts.append("STDOUT:\n" + result.stdout.strip())

        if result.stderr.strip():
            output_parts.append("STDERR:\n" + result.stderr.strip())

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
