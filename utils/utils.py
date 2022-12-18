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

class Point2D(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(Point2D[{0}:{1}])".format(self.x, self.y)

    def __str__(self):
        return "[{0}:{1}]".format(self.x, self.y)

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Point2D):
            return self.x == other.x and self.y == other.y
        return False
