import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a Python file located in a specified directory, with optional arguments, returning the output as a string.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "A list of optional arguments for the Python file being ran."
                },
            "required": ["file_path"]
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    work_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(work_dir_abs, file_path))
    valid_target_file = os.path.commonpath([work_dir_abs, target_file]) == work_dir_abs

    try:
        if not valid_target_file:
            raise ValueError(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file):
            raise ValueError(f'Error: "{file_path}" does not exist or is not a regular file')
        if not target_file.endswith('.py'):
            raise ValueError(f'Error: "{file_path}" is not a Python file')
        command = ["python", target_file]
        if args:
            command.extend(args)
        completed_process = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_string = ""
        if completed_process.returncode != 0:
            output_string += "Process exited with code X"
        if not completed_process.stdout and not completed_process.stderr:
            output_string += "No output produced"
        output_string += f"STDOUT: {completed_process.stdout}\n"
        output_string += f"STDERR: {completed_process.stderr}\n"
        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"
