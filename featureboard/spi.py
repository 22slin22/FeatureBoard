#from RPi import GPIO
import numpy as np


class Spi:

    def __init__(self, clk=23, mosi=19, latch=10):
        self.clk = clk
        self.mosi = mosi
        self.latch = latch
        """
        GPIO.setmode(GPIO.BOARD)  # GPIO Modus festlegen
        GPIO.setwarnings(False)
        GPIO.setup(clk, GPIO.OUT)  # Clock(Daten) definieren
        GPIO.setup(mosi, GPIO.OUT)  # MOSI (Daten) definieren
        GPIO.setup(latch, GPIO.OUT)  # LE definieren
        GPIO.output(clk, False)  # Clock initialisieren
        GPIO.output(mosi, False)  # MOSI initialisieren
        GPIO.output(latch, False)  # LE initialisieren
        """

    @staticmethod
    def set_pin(pin, boolean):
        #GPIO.output(pin, boolean)
        pass

    def latch_data(self):
        self.set_pin(self.latch, True)
        self.set_pin(self.latch, False)

    def send_bool(self, boolean):
        self.set_pin(self.mosi, boolean)

    def send_binary_array(self, array):
        for d in array:
            self.send_bool(bool(d))
            self.set_pin(self.clk, True)
            self.set_pin(self.clk, False)

    def send_row(self, row, array, num_panels):
        """
        send data for one row to the shift registers
        array should look like this:
        [[row1], [row2]] for 6 panels or
        [[row]] for 3 panels
        """
        data_row = np.ones(8, dtype=bool)
        data_row[row] = False

        for i in array:
            self.send_binary_array(data_row)
            self.send_binary_array(i)

        self.latch_data()
