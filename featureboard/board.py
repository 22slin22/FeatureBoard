from threading import Thread

from featureboard.matrix import Matrix
from featureboard.spi import Spi


class Board(Thread):

    def __init__(self, num_panels):
        super().__init__()
        self.setDaemon(True)    # daemon=True will make the thread terminate if the main program exits
        assert num_panels == 3 or num_panels == 6, "Number of panels can only be 3 or 6"
        self.num_panels = num_panels
        self.matrix = Matrix(num_panels)
        self.spi = Spi()

        self.thread = None
        self.row_index = 0
        self.running = False

    def start_displaying(self):
        """start displaying"""
        self.running = True
        self.start()       # start the thread, this will call the run() method

    def run(self):
        while self.running:
            self._show_next_row()

    def _show_next_row(self):
        """display the next row of the board"""
        if self.num_panels == 3:
            array = [self.matrix.get_row(self.row_index)]
        else:
            array = [self.matrix.get_row(self.row_index), self.matrix.get_row(self.row_index + 8)]

        self.spi.send_row(self.row_index, array, num_panels=self.num_panels)

        self.row_index += 1
        if self.row_index > 7:
            self.row_index = 0



