import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write the provided content into a specified file in a specified directory relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to the file being edited, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "String detailing the exact content that will be written into the file."
                },
            "required": ["file_path", "content"]
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    work_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(work_dir_abs, file_path))
    valid_target_file = os.path.commonpath([work_dir_abs, target_file]) == work_dir_abs

    try:
        if not valid_target_file:
            raise ValueError(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target_file):
            raise ValueError(f'Error: Cannot write to "{file_path}" as it is a directory')
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, 'w') as f:
            f.write(content)
        return (f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    except Exception as e:
        return str(e)
