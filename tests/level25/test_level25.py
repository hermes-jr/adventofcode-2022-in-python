import os

import pytest

import utils
from level25 import level25

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


@pytest.mark.parametrize("snafu, decimal",
                         [('1=-0-2', 1747), ('12111', 906), ('2=0=', 198), ('21', 11), ('2=01', 201), ('111', 31),
                          ('20012', 1257), ('112', 32), ('1=-1=', 353), ('1-12', 107), ('12', 7), ('1=', 3),
                          ('122', 37)])
def test_snafu_to_decimal(snafu, decimal):
    assert level25.s_to_d(snafu) == decimal


@pytest.mark.parametrize("snafu, decimal",
                         [('1=-0-2', 1747), ('12111', 906), ('2=0=', 198), ('21', 11), ('2=01', 201), ('111', 31),
                          ('20012', 1257), ('112', 32), ('1=-1=', 353), ('1-12', 107), ('12', 7), ('1=', 3),
                          ('122', 37)])
def test_decimal_to_snafu(snafu, decimal):
    assert level25.d_to_s(decimal) == snafu


def test_part1():
    assert level25.p1(in_data) == '2=-1=0'
