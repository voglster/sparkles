import os


def find_file_above(file_to_find: str, path: str = None):
    starting_directory = path or os.getcwd()

    tree = FileTree(starting_directory)

    while not tree.is_at_filesystem_root:
        if file_to_find in tree.current_files:
            return f"{tree.current_directory}/{file_to_find}"
        tree.move_up_one_level()


class FileTree:
    def __init__(self, starting_directory):
        self.current_directory = starting_directory

    @property
    def current_files(self):
        return os.listdir(self.current_directory)

    @property
    def parent_dir(self):
        return os.path.dirname(self.current_directory)

    @property
    def is_at_filesystem_root(self):
        return self.current_directory == self.parent_dir

    def move_up_one_level(self):
        self.current_directory = self.parent_dir
