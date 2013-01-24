# use python 3
from itertools import product, repeat
import random

def status(grid, x, y):
    if x < 0 or x >= len(grid):
        return 0
    if y < 0 or y >= len(grid[x]):
        return 0
    return grid[x][y]

def neighbours(grid, x, y):
    count = 0
    count += status(grid, x + 1, y)
    count += status(grid, x + 1, y - 1)
    count += status(grid, x, y - 1)
    count += status(grid, x - 1, y - 1)
    count += status(grid, x - 1, y)
    count += status(grid, x - 1, y + 1)
    count += status(grid, x, y + 1)
    count += status(grid, x + 1, y + 1)
    return count

def lifestep(grid):
    nexgrid = [[0 for col in row] for row in grid]
    for y, row in enumerate(grid):
        for x, state in enumerate(row):
            # number of neighbours
            n = neighbours(grid, x, y)

            # alive cell
            if state == 1:
                # allowed to live
                if 2 <= n <= 3:
                    ns = 1
                # isolation or overcrowding
                else:
                    ns = 0
            # dead cell
            elif state == 0:
                # reproduction
                if n == 3:
                    ns = 1
                # stays dead
                else:
                    ns = 0
            nexgrid[y][x] = ns
    return nexgrid

if __name__ == "__main__":
    import sys

    blinker = [[0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0],
               [0, 0, 1, 0, 0],
               [0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0]]

    beacon = [[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 0, 0, 0, 0]]

    grid = [[round(random.random()) for cell in range(50)] for row in range(50)] 

    while True:
        nex = lifestep(grid)
        for row in nex:
            for cell in row:
                if cell == 1:
                    sys.stdout.write("oo")
                elif cell == 0:
                    sys.stdout.write("  ")
            print
        grid = nex
        #input()
