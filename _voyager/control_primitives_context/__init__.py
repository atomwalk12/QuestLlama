import pkg_resources
import os
import _voyager.utils as U
import shared.config as C


def load_control_primitives_context(primitive_names=None):
    if C.USE_QUESTLLAMA:
        package_path = pkg_resources.resource_filename("questllama", "core")
    else:
        package_path = pkg_resources.resource_filename("voyager", "")
    if primitive_names is None:
        primitive_names = [
            primitive[:-3]
            for primitive in os.listdir(f"{package_path}/control_primitives_context")
            if primitive.endswith(".js")
        ]
    primitives = [
        U.load_text(f"{package_path}/control_primitives_context/{primitive_name}.js")
        for primitive_name in primitive_names
    ]
    return primitives
