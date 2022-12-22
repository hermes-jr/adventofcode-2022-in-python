import copy
import os

import pytest

import level19
import utils
from level19 import Inventory

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_inventory_hash():
    visited = set()
    i1 = Inventory()
    i1.geodes = 2
    visited.add(i1)
    i2 = Inventory()
    i2.geodes = 2
    assert hash(i1) == hash(i2)


def test_inventory_equality():
    visited = set()
    i1 = Inventory()
    i1.geodes = 2
    visited.add(i1)

    i2 = Inventory()
    i2.geodes = 2

    i3 = Inventory()
    i3.geodes = 1

    i4 = copy.deepcopy(i1)

    assert visited.__contains__(i2)  # `(i2 in visited) is True` maybe?
    assert not visited.__contains__(i3)
    assert visited.__contains__(i4)


@pytest.mark.skip(reason='Works, but slows things down')
def test_blueprint_evaluation():
    blueprints = level19.parse_input(in_data)
    assert level19.analyze_blueprint(blueprints[0], 24) * 1 == 9
    assert level19.analyze_blueprint(blueprints[1], 24) * 2 == 24
    assert level19.analyze_blueprint(blueprints[1], 32) == 62


def test_part1():
    assert level19.p1(level19.parse_input(in_data)) == 33


def test_part2():
    blueprints = level19.parse_input(in_data)
    assert level19.p2(blueprints) == 56 * 62
