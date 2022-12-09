from utils import utils

Matrix = list[list[int]]


def p1(level_map: Matrix) -> int:
    side = len(level_map)
    visibility = [x[:] for x in [[False] * side] * side]

    def check_cell(max_seen: int, i: int, j: int) -> int:
        if level_map[j][i] > max_seen:
            visibility[j][i] = True
        return max(level_map[j][i], max_seen)

    def scan_h(range_params: tuple[int, int, int]):
        for dx in range(0, side):
            max_seen = -1
            for dy in range(*range_params):
                max_seen = check_cell(max_seen, dx, dy)

    def scan_v(range_params: tuple[int, int, int]):
        for dy in range(0, side):
            max_seen = -1
            for dx in range(*range_params):
                max_seen = check_cell(max_seen, dx, dy)

    # top to bottom ltr sideview
    scan_h((0, side, 1))

    # top to bottom rtl sideview
    scan_h((side - 1, 0, -1))

    # ltr top view
    scan_v((0, side, 1))

    # ltr bottom view
    scan_v((side - 1, 0, -1))

    result = 0
    for i in range(0, side):
        for j in range(0, side):
            if visibility[j][i]:
                result += 1

    return result


def p2(level_map: Matrix) -> int:
    side = len(level_map)
    scenic_score = 0

    for candidate_x in range(1, side - 1):
        for candidate_y in range(1, side - 1):
            local_scenic_score = get_candidate_scenic_score(level_map, candidate_x, candidate_y)
            scenic_score = max(scenic_score, local_scenic_score)

    return scenic_score


def get_candidate_scenic_score(level_map: Matrix, candidate_x: int, candidate_y: int) -> int:
    side = len(level_map)
    candidate_height = level_map[candidate_y][candidate_x]

    # if __debug__:
    #     print('\n')
    #     for x in range(0, side):
    #         for y in range(0, side):
    #             print('{:4}'.format(level_map[x][y]), end=' ')
    #         print('\n')

    # right
    rd = 1
    for i in range(candidate_x + 1, side - 1):
        if level_map[candidate_y][i] >= candidate_height:
            break
        rd += 1
    # left
    ld = 1
    for i in range(candidate_x - 1, 0, -1):
        if level_map[candidate_y][i] >= candidate_height:
            break
        ld += 1
    # up
    ud = 1
    for j in range(candidate_y - 1, 0, -1):
        if level_map[j][candidate_x] >= candidate_height:
            break
        ud += 1
    # down
    dd = 1
    for j in range(candidate_y + 1, side - 1):
        if level_map[j][candidate_x] >= candidate_height:
            break
        dd += 1

    if __debug__:
        print("For [{}:{}] with height {} formula is {}*{}*{}*{}".format(
            candidate_x, candidate_y, candidate_height,
            ud, ld, dd, rd
        ))
    return rd * ld * ud * dd


def parse_input(lines: list[str]) -> Matrix:
    side = len(lines)
    level_map = [x[:] for x in [[0] * side] * side]
    for i in range(0, side):
        for j in range(0, side):
            level_map[j][i] = int(lines[j][i])

    return level_map


if __name__ == "__main__":
    data_input = utils.read_file("in.txt")
    parsed_map = parse_input(data_input)
    result1 = p1(parsed_map)
    print("result1: {}".format(result1))
    result2 = p2(parsed_map)
    print("result2: {}".format(result2))

u"""
--- Day 8: Treetop Tree House ---

The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

    The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
    The top-middle 5 is visible from the top and right.
    The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
    The left-middle 5 is visible, but only from the right.
    The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
    The right-middle 3 is visible from the right.
    In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?

--- Part Two ---

Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

    Looking up, its view is not blocked; it can see 1 tree (of height 3).
    Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
    Looking right, its view is not blocked; it can see 2 trees.
    Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).

A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390

    Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
    Looking left, its view is not blocked; it can see 2 trees.
    Looking down, its view is also not blocked; it can see 1 tree.
    Looking right, its view is blocked at 2 trees (by a massive tree of height 9).

This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?

"""
