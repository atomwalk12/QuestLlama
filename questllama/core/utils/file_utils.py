import pkg_resources

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
    """ Load a prompt from a given file. """
    package_path = pkg_resources.resource_filename("questllama", "")
    return load_text(f"{package_path}/core/prompts/{file}")


def get_prompts_path(prompts_location):
    return pkg_resources.resource_filename("questllama", prompts_location)
