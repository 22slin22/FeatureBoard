from featureboard.board import Board

if __name__ == '__main__':
    board = Board(3)
    board.start_displaying()

    board.matrix.set_led(0, 0, "b")
    board.matrix.set_led(3, 9, "r")
    board.matrix.set_led(6, 18, "g")
