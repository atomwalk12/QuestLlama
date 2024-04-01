import pkg_resources
import voyager.utils as U
import shared.config as C


def load_prompt(prompt):
    if C.USE_QUESTLLAMA:
        package_path = pkg_resources.resource_filename("questllama", "core")
        return U.load_text(f"{package_path}/prompts/{prompt}.txt")
    else:
        package_path = pkg_resources.resource_filename("voyager", "")
        return U.load_text(f"{package_path}/prompts/{prompt}.txt")
