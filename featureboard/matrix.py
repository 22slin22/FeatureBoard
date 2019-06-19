import numpy as np

COLORS = {}
for k in ["o", "off"]:
    COLORS[k] = (False, False, False)
for k in ["b", "blue"]:
    COLORS[k] = (True, False, False)
for k in ["g", "green"]:
    COLORS[k] = (False, True, False)
for k in ["r", "red"]:
    COLORS[k] = (False, False, True)
for k in ["c", "cyan"]:
    COLORS[k] = (True, True, False)
for k in ["m", "magenta"]:
    COLORS[k] = (True, False, True)
for k in ["y", "yelllow"]:
    COLORS[k] = (False, True, True)
for k in ["w", "white"]:
    COLORS[k] = (True, True, True)


class Matrix:

    def __init__(self, num_panels):
        self.num_panels = num_panels
        self.num_rows = int(num_panels/3) * 8
        num_columns = 3 * 8
        num_colors = 3
        self.array = np.zeros((self.num_rows, num_columns, num_colors), dtype=bool)
        # self.rows stores data that can be directly send to the shift registers
        # it is computed every time the array is changes.
        self.rows = np.zeros((self.num_rows, num_columns * num_colors), dtype=bool)

    def clear(self):
        self.array[:][:] = COLORS["off"]
        self._update_rows()

    def set_led(self, row, column, color):
        self._check_color(color)
        self.array[row, column] = COLORS[color]
        self._update_rows()

    def set_row(self, row, color):
        self._check_color(color)
        self.array[row] = COLORS[color]
        self._update_rows()

    def set_column(self, column, color):
        self._check_color(color)
        self.array[:, column] = COLORS[color]
        self._update_rows()

    def _update_rows(self):
        """copy the content of self.array to self.rows"""
        for i, row in enumerate(self.array):
            self.rows[i] = row.reshape(-1, 8, 3).swapaxes(1, 2).ravel()
            """
            equivalent to this

            new_array = np.array([])
            np.append(new_array, old_array[0:8, 0])
            np.append(new_array, old_array[0:8, 1])
            np.append(new_array, old_array[0:8, 2])

            np.append(new_array, old_array[8:16, 0])
            np.append(new_array, old_array[8:16, 1])
            np.append(new_array, old_array[8:16, 2])

            np.append(new_array, old_array[16:24, 0])
            np.append(new_array, old_array[16:24, 1])
            np.append(new_array, old_array[16:24, 2])
            """

    def get_row(self, row_num):
        """get a row in the correct order for sending it to the shift registers"""
        return self.rows[row_num]

    def _check_color(self, color):
        assert color in COLORS, 'color must be one of ("b", "blue", "blau", "g", "green", "gruen", "grün", ' \
                                '"r", "red", "rot", "c", "cyan", "lightblue", "hellblau", "tuerkis", "türkis", ' \
                                '"m", "magenta", "y", "yelllow", "ge", "gelb", "w", "white", "weiss", "weiß")'

