import os
import pkg_resources

from questllama.core.utils.file_utils import load_text


def load_control_primitives(file):
    package_path = pkg_resources.resource_filename(
        "questllama", "core/env"
    )

    return load_text(f"{package_path}/{file}")

