import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Return the content of a file as a string.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to the file being read, relative to the working directory.",
                },
            "required": ["file_path"]
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    work_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(work_dir_abs, file_path))
    valid_target_file = os.path.commonpath([work_dir_abs, target_file]) == work_dir_abs

    try:
        if not valid_target_file:
            raise ValueError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file):
            raise ValueError(f'Error: File not found or is not a regular file: "{file_path}"')
        with open(target_file, 'r') as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[... File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except (ValueError, OSError) as e:
        return f"{e}"
