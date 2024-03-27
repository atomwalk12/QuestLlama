from voyager import utils as U
import pkg_resources


def load_text(file):
    """ Load text from a file. """
    package_path = pkg_resources.resource_filename("questllama", "")
    return U.load_text(f"{package_path}/debug/{file}")
