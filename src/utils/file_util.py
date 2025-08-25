import os

def get_file_name_and_extension(filename):
    # for a filename, returns to the name and the extension
    return os.path.splitext(filename)