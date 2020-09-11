import os


def find_file_above(file_name: str, path: str = None):
    path = (
        path or os.getcwd()
    )  # Dir from where search starts can be replaced with any path

    while True:
        file_list = os.listdir(path)
        parent_dir = os.path.dirname(path)
        if file_name in file_list:
            return f"{path}/{file_name}"
        else:
            if path == parent_dir:
                return None
            else:
                path = parent_dir
