import pkg_resources
import os
import collections


def load_text(path, by_lines=False):
    """
    Load text from a file at the given path. The function can either read the entire
    content of the file or break it down into lines depending on the 'by_lines' parameter.
    """

    with open(path, "r") as fp:
        if by_lines:
            return fp.readlines()
        else:
            return fp.read()


def load_prompt(file):
    """Load a prompt from a given file."""
    package_path = pkg_resources.resource_filename("questllama", "core")
    return load_text(f"{package_path}/prompts/{file}.txt")


def debug_load_prompt(prompt):
    """Load a prompt from a given file."""
    package_path = pkg_resources.resource_filename("questllama", "core")
    return  load_text(f"{package_path}/prompts/debugging/{prompt}")


def get_abs_path(resource_name):
    """
    Get the absolute path of a resource file based on its name.
    """
    return pkg_resources.resource_filename("questllama", resource_name)


def read_skill_library(path):
    """
    Read all JavaScript files in the 'skill_library' directory and its subdirectories.
    """
    skill_directory = get_abs_path(path)

    return read_files(skill_directory, extension=".js")


def read_files(directory_path, extension=".js"):
    """
    Read all files in a directory and its subdirectories with the specified extension.
    """

    all_files = []

    for file in os.listdir(directory_path):
        # Construct absolute path of current file/directory being examined
        file_path = os.path.join(directory_path, file)

        # If file is a directory, recursively read its contents
        if os.path.isdir(file_path):
            all_files += read_files(file_path, extension)

        else:
            # If it's not a directory and has the correct extension, add to list of files to be returned
            if file.endswith(extension):
                with open(file_path, "r") as f:
                    all_files.append((file, f.read()))

    return all_files


# FIXME refactor these functions
def f_mkdir(*fpaths):
    """
    Recursively creates all the subdirs
    If exist, do nothing.
    """
    fpath = f_join(*fpaths)
    os.makedirs(fpath, exist_ok=True)
    return fpath


def f_expand(fpath):
    return os.path.expandvars(os.path.expanduser(fpath))


def is_sequence(obj):
    """
    Returns:
      True if the sequence is a collections.Sequence and not a string.
    """
    return isinstance(obj, collections.abc.Sequence) and not isinstance(obj, str)


def pack_varargs(args):
    """
    Pack *args or a single list arg as list

    def f(*args):
        arg_list = pack_varargs(args)
        # arg_list is now packed as a list
    """
    assert isinstance(args, tuple), "please input the tuple `args` as in *args"
    if len(args) == 1 and is_sequence(args[0]):
        return args[0]
    else:
        return args


def f_join(*fpaths):
    """
    join file paths and expand special symbols like `~` for home dir
    """
    fpaths = pack_varargs(fpaths)
    fpath = f_expand(os.path.join(*fpaths))
    if isinstance(fpath, str):
        fpath = fpath.strip()
    return fpath
