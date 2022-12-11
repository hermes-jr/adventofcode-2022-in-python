import logging
import sys

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def dlog(obj: str, *args):
    logging.debug(obj, *args)


def read_file(filepath) -> list[str]:
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            data.append(line.strip())
    return data
