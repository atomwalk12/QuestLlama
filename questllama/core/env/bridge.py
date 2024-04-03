import requests
from questllama.core.env import load_control_primitives
import json

def pretty_print(data):
    pretty_printed_string = json.dumps(json.loads(data), indent=4)
    print(pretty_printed_string)



def run():
    while True:
        input("\n Start?")
        server = "http://127.0.0.1:3000"
        reset_options = {
            "port": 43571,
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
        pretty_print(res.text)


if __name__ == "__main__":
    run()


