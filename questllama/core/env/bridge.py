from pandas import reset_option
import requests

from questllama.core.env import load_control_primitives


def run():
    server = "0.0.0.0:3000"
    reset_options = ""
    request_timeout = 30

    data = {
        "code": load_control_primitives("examples/code.js"),
        "programs": load_control_primitives("examples/programs.js"),
    }

    requests.post(
        f"{server}/start",
        json=reset_options,
        timeout=request_timeout,
    )
    res = requests.post(f"{server}/step", json=data, timeout=request_timeout)


if __name__ == "__main__":
    run()
