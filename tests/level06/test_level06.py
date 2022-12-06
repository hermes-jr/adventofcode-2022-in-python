import level06


def test_part1():
    assert level06.detect_first_block('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4) == 7
    assert level06.detect_first_block('bvwbjplbgvbhsrlpgdmjqwftvncz', 4) == 5
    assert level06.detect_first_block('nppdvjthqldpwncqszvftbrmjlhg', 4) == 6
    assert level06.detect_first_block('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4) == 10
    assert level06.detect_first_block('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4) == 11


def test_part2():
    assert level06.detect_first_block('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14) == 19
    assert level06.detect_first_block('bvwbjplbgvbhsrlpgdmjqwftvncz', 14) == 23
    assert level06.detect_first_block('nppdvjthqldpwncqszvftbrmjlhg', 14) == 23
    assert level06.detect_first_block('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14) == 29
    assert level06.detect_first_block('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14) == 26
