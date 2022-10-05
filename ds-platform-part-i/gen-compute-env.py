import argparse
import json
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("subnet", type=str)
    parser.add_argument("sg", type=str)
    args = parser.parse_args()

    ce = json.loads(Path('compute-env.json').read_text())

    ce["computeResources"]["subnets"] = [args.subnet]
    ce["computeResources"]["securityGroupIds"] = [args.sg]

    path = "my-compute-env.json"
    Path(path).write_text(json.dumps(ce))
    print(f"Config file stored at: {path}")