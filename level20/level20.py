from utils import read_file, Point2D

Chain = dict[Point2D, list[Point2D, Point2D]]


def p1(parsed: Chain, encrypted: list[int]) -> int:
    mixed = mix(parsed, encrypted)
    if __debug__:
        print(mixed)
    return sum_key_elements(parsed)


def p2(parsed: Chain, encrypted: list[int]) -> int:
    for mixing_round in range(10):
        if __debug__:
            print('started round', mixing_round)
        parsed = mix(parsed, encrypted)

    return sum_key_elements(parsed)


def find_zero(chain):
    for k in chain:
        if k.y == 0:
            return k


def dump_chain(chain):
    zero = head = find_zero(chain)
    while True:
        print(head.y, end=',')
        head = chain[head][1]
        if chain[head][1] == zero:
            break
    print('')


def mix(chain: Chain, encrypted: list[int]) -> Chain:
    if __debug__:
        print('Mixing: ', end='')
        dump_chain(chain)
    wrap = len(encrypted) - 1
    for idx, distance in enumerate(encrypted):
        current = Point2D(idx, distance)
        steps = abs(distance) % wrap
        for _ in range(steps):
            old_left = chain[current][0]
            old_right = chain[current][1]
            if distance >= 0:
                new_right = chain[old_right][1]
                # if __debug__:
                #     print('{} moves between {} and {}'.format(current.y, old_right.y, new_right.y))
                chain[current] = [old_right, new_right]
                chain[old_right] = [old_left, current]
                chain[new_right][0] = current
                chain[old_left][1] = old_right
            else:
                new_left = chain[old_left][0]
                # if __debug__:
                #     print('{} moves between {} and {}'.format(current.y, new_left.y, old_left.y))
                chain[current] = [new_left, old_left]
                chain[old_left] = [current, old_right]
                chain[old_right][0] = old_left
                chain[new_left][1] = current
    if __debug__:
        dump_chain(chain)
    return chain


def sum_key_elements(chain: Chain):
    head = find_zero(chain)
    result = 0
    for i in range(1, 3001):
        head = chain[head][1]
        if i in {1000, 2000, 3000}:
            result += head.y
            if __debug__:
                print('key element {} found: {}'.format(i, head.y))
    if __debug__:
        print('key elements sum:', result)
    return result


def parse_input(input_lines: list[str], key=1) -> tuple[Chain, list[int]]:
    parsed: Chain = {}
    lines = list([x * key for x in map(int, input_lines)])
    size = len(lines)
    for idx, val in enumerate(lines):
        left_idx = (idx - 1) % size
        right_idx = (idx + 1) % size
        parsed[Point2D(idx, val)] = [Point2D(left_idx, lines[left_idx]), Point2D(right_idx, lines[right_idx])]

    if __debug__:
        print(input_lines)
        print(parsed)
    return parsed, lines


if __name__ == "__main__":
    data_input = read_file("in.txt")
    result1 = p1(*parse_input(data_input))
    print("result1: {}".format(result1))
    result2 = p2(*parse_input(data_input, 811589153))
    print("result2: {}".format(result2))

u"""
--- Day 20: Grove Positioning System ---

It's finally time to meet back up with the Elves. When you try to contact them, however, you get no reply. Perhaps you're out of range?

You know they're headed to the grove where the star fruit grows, so if you can figure out where that is, you should be able to meet back up with them.

Fortunately, your handheld device has a file (your puzzle input) that contains the grove's coordinates! Unfortunately, the file is encrypted - just in case the device were to fall into the wrong hands.

Maybe you can decrypt it?

When you were still back at the camp, you overheard some Elves talking about coordinate file encryption. The main operation involved in decrypting the file is called mixing.

The encrypted file is a list of numbers. To mix the file, move each number forward or backward in the file a number of positions equal to the value of the number being moved. The list is circular, so moving a number off one end of the list wraps back around to the other end as if the ends were connected.

For example, to move the 1 in a sequence like 4, 5, 6, 1, 7, 8, 9, the 1 moves one position forward: 4, 5, 6, 7, 1, 8, 9. To move the -2 in a sequence like 4, -2, 5, 6, 7, 8, 9, the -2 moves two positions backward, wrapping around: 4, 5, 6, 7, 8, -2, 9.

The numbers should be moved in the order they originally appear in the encrypted file. Numbers moving around during the mixing process do not change the order in which the numbers are moved.

Consider this encrypted file:

1
2
-3
3
-2
0
4

Mixing this file proceeds as follows:

Initial arrangement:
1, 2, -3, 3, -2, 0, 4

1 moves between 2 and -3:
2, 1, -3, 3, -2, 0, 4

2 moves between -3 and 3:
1, -3, 2, 3, -2, 0, 4

-3 moves between -2 and 0:
1, 2, 3, -2, -3, 0, 4

3 moves between 0 and 4:
1, 2, -2, -3, 0, 3, 4

-2 moves between 4 and 1:
1, 2, -3, 0, 3, 4, -2

0 does not move:
1, 2, -3, 0, 3, 4, -2

4 moves between -3 and 0:
1, 2, -3, 4, 0, 3, -2

Then, the grove coordinates can be found by looking at the 1000th, 2000th, and 3000th numbers after the value 0, wrapping around the list as necessary. In the above example, the 1000th number after 0 is 4, the 2000th is -3, and the 3000th is 2; adding these together produces 3.

Mix your encrypted file exactly once. What is the sum of the three numbers that form the grove coordinates?

--- Part Two ---

The grove coordinate values seem nonsensical. While you ponder the mysteries of Elf encryption, you suddenly remember the rest of the decryption routine you overheard back at camp.

First, you need to apply the decryption key, 811589153. Multiply each number by the decryption key before you begin; this will produce the actual list of numbers to mix.

Second, you need to mix the list of numbers ten times. The order in which the numbers are mixed does not change during mixing; the numbers are still moved in the order they appeared in the original, pre-mixed list. (So, if -3 appears fourth in the original list of numbers to mix, -3 will be the fourth number to move during each round of mixing.)

Using the same example as above:

Initial arrangement:
811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612

After 1 round of mixing:
0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153

After 2 rounds of mixing:
0, 2434767459, 1623178306, 3246356612, -2434767459, -1623178306, 811589153

After 3 rounds of mixing:
0, 811589153, 2434767459, 3246356612, 1623178306, -1623178306, -2434767459

After 4 rounds of mixing:
0, 1623178306, -2434767459, 811589153, 2434767459, 3246356612, -1623178306

After 5 rounds of mixing:
0, 811589153, -1623178306, 1623178306, -2434767459, 3246356612, 2434767459

After 6 rounds of mixing:
0, 811589153, -1623178306, 3246356612, -2434767459, 1623178306, 2434767459

After 7 rounds of mixing:
0, -2434767459, 2434767459, 1623178306, -1623178306, 811589153, 3246356612

After 8 rounds of mixing:
0, 1623178306, 3246356612, 811589153, -2434767459, 2434767459, -1623178306

After 9 rounds of mixing:
0, 811589153, 1623178306, -2434767459, 3246356612, 2434767459, -1623178306

After 10 rounds of mixing:
0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153

The grove coordinates can still be found in the same way. Here, the 1000th number after 0 is 811589153, the 2000th is 2434767459, and the 3000th is -1623178306; adding these together produces 1623178306.

Apply the decryption key and mix your encrypted file ten times. What is the sum of the three numbers that form the grove coordinates?

"""
