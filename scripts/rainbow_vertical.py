import math
import time

from featureboard.board import Board

COLORS = ["b", "c", "g", "y", "r", "m", "w"]

if __name__ == '__main__':
    num_panels = input("Number of panels: ")
    width = input("Width of the stripes: ")
    wait_time = input("Number of seconds until the rainbow moves again: ")

    try:
        num_panels = int(num_panels)
        width = int(width)
        wait_time = int(wait_time)
    except ValueError:
        print("all values entered must be integers")
        exit()

    board = Board(num_panels)
    board.start_displaying()

    index = 0

    while True:
        for i in range(24):
            color_index = int(math.floor((i + index) / width))
            color_index %= len(COLORS)
            board.matrix.set_column(i, COLORS[color_index])

        index -= 1
        time.sleep(wait_time)
