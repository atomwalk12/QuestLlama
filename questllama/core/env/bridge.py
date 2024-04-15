import requests
from questllama.core.env import load_control_primitives
import json


def run():
    while True:
        input("\n Start?")
        server = "http://127.0.0.1:3000"
        reset_options = {
            "port": 40189,
            "reset": "hard",
            "inventory": {},
            "equipment": [],
            "spread": False,
            "waitTicks": 20,
            "position": None,
        }
        request_timeout = 600

        data = {
            "code": load_control_primitives("examples/code.js"),
            "programs": load_control_primitives("examples/programs.js"),
        }

        requests.post(f"{server}/start", json=reset_options)
        print(data["code"])
        res = requests.post(f"{server}/step", json=data, timeout=request_timeout)
        pretty_printed_string = json.dumps(json.loads(res.text), indent=4)
        print(pretty_printed_string)


if __name__ == "__main__":
    run()
