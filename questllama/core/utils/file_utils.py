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
    package_path = pkg_resources.resource_filename("questllama", "")
    return load_text(f"{package_path}/core/prompts/{file}")


def get_prompts_path(prompts_location):
    return pkg_resources.resource_filename("questllama", prompts_location)


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
