import sys
from string import Template
import argparse
from pathlib import Path
import random
import string

template_client = """
from ploomber.clients import S3Client


def get():
    return S3Client(bucket_name='{}', parent='outputs')
"""

template_policy = Template("""\
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "s3:*",
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::$bucket_name",
                "arn:aws:s3:::$bucket_name/*"
            ]
        }
    ]
}
""")

template_cfg = Template("""\
aws-env:
  backend: aws-batch
  container_properties: {memory: 16384, vcpus: 8}
  exclude: [output]
  job_queue: $queue
  region_name: $region
  repository: $repository
""")

class CLI:

    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('command')
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            sys.exit(f'Unrecognized command {args.command!r}')
        else:
            cmd = getattr(self, args.command)

            try:
                cmd()
            except Exception as e:
                sys.exit(e)

            sys.exit(0)

    def bucket(self):
        chars = string.ascii_lowercase + string.digits
        suffix = ''.join(random.choice(chars) for i in range(6))
        print(f'ploomber-bucket-{suffix}')
    
    def client(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--directory", type=str)
        parser.add_argument("--bucket-name", type=str)
        args = parser.parse_args(sys.argv[2:])

        path = Path(args.directory, "clients.py")
        path.write_text(template_client.format(args.bucket_name))
        print(f"Clients file stored at: {path!s}")

    def policy(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--bucket-name", type=str)
        args = parser.parse_args(sys.argv[2:])

        path = Path("s3-policy.json")
        path.write_text(template_policy.substitute(bucket_name=args.bucket_name))
        print(f"Policy file stored at: {path!s}")

    def config(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--directory", type=str)
        parser.add_argument("--queue", type=str)
        parser.add_argument("--region", type=str)
        parser.add_argument("--repository", type=str)
        args = parser.parse_args(sys.argv[2:])

        path = Path(args.directory, "soopervisor.yaml")
        path.write_text(template_cfg.substitute(queue=args.queue,
                                                region=args.region,
                                                repository=args.repository))
        print(f"Config file stored at: {path!s}")
        
if __name__ == '__main__':
    CLI()