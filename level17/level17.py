from utils import read_file

tetriminos = [
    [[1, 1, 1, 1]],

    [[0, 1, 0],
     [1, 1, 1],
     [0, 1, 0]],

    [[0, 0, 1],
     [0, 0, 1],
     [1, 1, 1]],

    [[1],
     [1],
     [1],
     [1]],

    [[1, 1],
     [1, 1]]
]

wind_dxes = {'>': 1, '<': -1}


def collision(matrix, tetrimino, potential_x, potential_y) -> bool:
    # Reached walls:
    if potential_x < 0 or potential_x + len(tetrimino[0]) - 1 >= 7:
        return True
    # Reached bottom:
    if potential_y + len(tetrimino) - 1 >= len(matrix):
        return True
    # Collision with landed pieces
    for ty in range(0, len(tetrimino)):
        for tx in range(0, len(tetrimino[0])):
            if tetrimino[ty][tx] == 1 and matrix[potential_y + ty][potential_x + tx] == 1:
                return True
    return False


def p1(input_winds: str) -> int:
    matrix = [x[:] for x in
              [[0] * 7] * (4 * 2022 + 100)]  # 7 by 2022 longest vertical tetriminos + a bit more, should be enough
    current_top = len(matrix)

    ph = 0
    wind_turn = 0
    for shape_turn in range(0, 2022):
        # spawn
        tetrimino = tetriminos[shape_turn % len(tetriminos)]
        tetrimino_x = 2
        tetrimino_y = current_top - len(tetrimino) - 3
        # fall:
        while True:
            # pushed by gas
            gas_dx = wind_dxes[input_winds[wind_turn % len(input_winds)]]
            potential_x = tetrimino_x + gas_dx
            if not collision(matrix, tetrimino, potential_x, tetrimino_y):
                tetrimino_x = potential_x
            wind_turn += 1

            # gravity
            potential_y = tetrimino_y + 1
            if collision(matrix, tetrimino, tetrimino_x, potential_y):
                # land
                for dy in range(0, len(tetrimino)):
                    for dx in range(0, len(tetrimino[0])):
                        if tetrimino[dy][dx] == 1:
                            matrix[tetrimino_y + dy][tetrimino_x + dx] = 1
                dh = current_top
                current_top = min(current_top, tetrimino_y)
                dh = dh - current_top
                break
            else:
                tetrimino_y = potential_y
        """
        if __debug__:
            # print_level(matrix)
            # print('{}, brick dropped, height: {}: {}'.format(shape_turn, len(matrix) - current_top, dh))
            # print(dh, end='')
            if shape_turn % len(tetriminos) == 0 and shape_turn % len(input_winds) == 0:
                print('{}, brick dropped, height: {}: {} '.format(shape_turn, len(matrix) - current_top,
                                                                  ph - current_top))
                ph = current_top
        """
    return len(matrix) - current_top


#
# 11928, brick dropped, height: 18071: 2
# 11929, brick dropped, height: 18071: 0
# 11930, brick dropped, height: 18071: 0
# 11931, brick dropped, height: 18073: 2
# 11932, brick dropped, height: 18076: 3
#
#
# 11947, brick dropped, height: 18098: 2
# 11948, brick dropped, height: 18098: 0
# 11949, brick dropped, height: 18098: 0
# 11950, brick dropped, height: 18099: 1
# 11951, brick dropped, height: 18102: 3
#
# 11963, brick dropped, height: 18124: 2
# 11964, brick dropped, height: 18124: 0
# 11965, brick dropped, height: 18124: 0
# 11966, brick dropped, height: 18126: 2
# 11967, brick dropped, height: 18129: 3
#
#
# 11982, brick dropped, height: 18151: 2
# 11983, brick dropped, height: 18151: 0
# 11984, brick dropped, height: 18151: 0
# 11985, brick dropped, height: 18152: 1
# 11986, brick dropped, height: 18155: 3
#
#
# 11998, brick dropped, height: 18177: 2
# 11999, brick dropped, height: 18177: 0
# 12000, brick dropped, height: 18177: 0
# 12001, brick dropped, height: 18179: 2
# 12002, brick dropped, height: 18182: 3

def p2(input_winds: str) -> int:
    return -1


def print_level(matrix):
    print('')
    print('\n'.join(['|' + ''.join([' ' if item == 0 else '#' for item in row]) + '|'
                     for row in matrix[-20:]]))
    print('+-------+')


if __name__ == "__main__":
    data_input = read_file("in.txt")[0]
    result1 = p1(data_input)
    print("result1: {}".format(result1))
    # result2 = p2(data_input)
    # print("result2: {}".format(result2))

u"""
--- Day 17: Pyroclastic Flow ---

Your handheld device has located an alternative exit from the cave for you and the elephants. The ground is rumbling almost continuously now, but the strange valves bought you some time. It's definitely getting warmer in here, though.

The tunnels eventually open into a very tall, narrow chamber. Large, oddly-shaped rocks are falling into the chamber from above, presumably due to all the rumbling. If you can't work out where the rocks will fall next, you might be crushed!

The five types of rocks have the following peculiar shapes, where # is rock and . is empty space:

####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##

The rocks fall in the order shown above: first the - shape, then the + shape, and so on. Once the end of the list is reached, the same order repeats: the - shape falls first, sixth, 11th, 16th, etc.

The rocks don't spin, but they do get pushed around by jets of hot gas coming out of the walls themselves. A quick scan reveals the effect the jets of hot gas will have on the rocks as they fall (your puzzle input).

For example, suppose this was the jet pattern in your cave:

>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>

In jet patterns, < means a push to the left, while > means a push to the right. The pattern above means that the jets will push a falling rock right, then right, then right, then left, then left, then right, and so on. If the end of the list is reached, it repeats.

The tall, vertical chamber is exactly seven units wide. Each rock appears so that its left edge is two units away from the left wall and its bottom edge is three units above the highest rock in the room (or the floor, if there isn't one).

After a rock appears, it alternates between being pushed by a jet of hot gas one unit (in the direction indicated by the next symbol in the jet pattern) and then falling one unit down. If any movement would cause any part of the rock to move into the walls, floor, or a stopped rock, the movement instead does not occur. If a downward movement would have caused a falling rock to move into the floor or an already-fallen rock, the falling rock stops where it is (having landed on something) and a new rock immediately begins falling.

Drawing falling rocks with @ and stopped rocks with #, the jet pattern in the example above manifests as follows:

The first rock begins falling:
|..@@@@.|
|.......|
|.......|
|.......|
+-------+

Jet of gas pushes rock right:
|...@@@@|
|.......|
|.......|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
|.......|
|.......|
+-------+

Jet of gas pushes rock right, but nothing happens:
|...@@@@|
|.......|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
|.......|
+-------+

Jet of gas pushes rock right, but nothing happens:
|...@@@@|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
+-------+

Jet of gas pushes rock left:
|..@@@@.|
+-------+

Rock falls 1 unit, causing it to come to rest:
|..####.|
+-------+

A new rock begins falling:
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|..####.|
+-------+

Jet of gas pushes rock left:
|..@....|
|.@@@...|
|..@....|
|.......|
|.......|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|..@....|
|.@@@...|
|..@....|
|.......|
|.......|
|..####.|
+-------+

Jet of gas pushes rock right:
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|...@...|
|..@@@..|
|...@...|
|.......|
|..####.|
+-------+

Jet of gas pushes rock left:
|..@....|
|.@@@...|
|..@....|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|..@....|
|.@@@...|
|..@....|
|..####.|
+-------+

Jet of gas pushes rock right:
|...@...|
|..@@@..|
|...@...|
|..####.|
+-------+

Rock falls 1 unit, causing it to come to rest:
|...#...|
|..###..|
|...#...|
|..####.|
+-------+

A new rock begins falling:
|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|...#...|
|..###..|
|...#...|
|..####.|
+-------+

The moment each of the next few rocks begins falling, you would see this:

|..@....|
|..@....|
|..@....|
|..@....|
|.......|
|.......|
|.......|
|..#....|
|..#....|
|####...|
|..###..|
|...#...|
|..####.|
+-------+

|..@@...|
|..@@...|
|.......|
|.......|
|.......|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@@@@.|
|.......|
|.......|
|.......|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|..#....|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@....|
|..@....|
|..@....|
|..@....|
|.......|
|.......|
|.......|
|.....#.|
|.....#.|
|..####.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@@...|
|..@@...|
|.......|
|.......|
|.......|
|....#..|
|....#..|
|....##.|
|....##.|
|..####.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@@@@.|
|.......|
|.......|
|.......|
|....#..|
|....#..|
|....##.|
|##..##.|
|######.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

To prove to the elephants your simulation is accurate, they want to know how tall the tower will get after 2022 rocks have stopped (but before the 2023rd rock begins falling). In this example, the tower of rocks will be 3068 units tall.

How many units tall will the tower of rocks be after 2022 rocks have stopped falling?

--- Part Two ---

The elephants are not impressed by your simulation. They demand to know how tall the tower will be after 1000000000000 rocks have stopped! Only then will they feel confident enough to proceed through the cave.

In the example above, the tower would be 1514285714288 units tall!

How tall will the tower be after 1000000000000 rocks have stopped?

"""
