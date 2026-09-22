import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    work_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(work_dir_abs, directory))
    valid_target_dir = os.path.commonpath([work_dir_abs, target_dir]) == work_dir_abs

    try:
        if not valid_target_dir:
            raise ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(target_dir):
            raise ValueError(f'Error: "{directory}" is not a directory')
        return f'Success: "{directory}" is within the working directory'
    except (ValueError, OSError) as e:
        return f"{e}"
