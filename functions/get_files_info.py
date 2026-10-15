import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:

    work_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(work_dir_abs, directory))
    valid_target_dir = os.path.commonpath([work_dir_abs, target_dir]) == work_dir_abs
    directory_contents = os.listdir(target_dir)
    list_result = []

    try:
        if not valid_target_dir:
            raise ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(target_dir):
            raise ValueError(f'Error: "{directory}" is not a directory')

        for item in directory_contents:
            try:
                item_path = os.path.join(target_dir, item)
                list_result.append(f'- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}')
            except OSError as e:
                return f'Error: {e}'
        return '\n'.join(list_result)

    except (ValueError, OSError) as e:
        return f"{e}"
