from voyager import utils as U
import pkg_resources


def writeToFile(lines, filename='prompts.txt'):
    """
    Write lines to a file. Used to debug LM Studio prompts.
    """
    with open(filename, 'w') as f:
        for line in lines:
            f.write(f"type: {line.type}\n")
            f.write(f"content: {line.content}\n")


def load_text(file):
    """ Load text from a file. """
    package_path = pkg_resources.resource_filename("questllama", "")
    return U.load_text(f"{package_path}/debug/{file}")
