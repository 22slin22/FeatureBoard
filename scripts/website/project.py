import numpy as np
import time
from threading import Thread
from featureboard.board import Board

NUM_PANELS = 3

COLORS = ["o", "b", "g", "r", "c", "m", "y", "w"]


class Project:
    def __init__(self, name):
        self.name = name
        self.fps = 1
        # create array of frames with one emtpy frame
        self.frames = [np.zeros(shape=(int(NUM_PANELS / 3), 3, 8, 8), dtype='int').tolist()]

    def add_frame(self, frame):
        self.frames.append(frame)

    def set_fps(self, fps):
        self.fps = fps

    def to_dict(self):
        return {"name": self.name, "fps": self.fps, "frames": self.frames}


def project_from_dict(d):
    project = Project(d["name"])
    project.fps = d["fps"]
    project.frames = d["frames"]
    return project


class ProjectPlayer(Thread):

    def __init__(self, project, num_panels):
        super().__init__()
        # daemon=True will make the thread terminate if the main program exits
        self.setDaemon(True)

        self.board = Board(num_panels)
        self.project = project
        self.frames = self.frames_to_string_array(project.frames)

        self.running = True
        self.frame_index = 0

    def _show_next_frame(self):
        self.board.matrix.set_array(self.frames[self.frame_index])
        self.frame_index += 1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

    def start(self):
        self.board.start_displaying()
        super().start()

    def run(self):
        self._do_every(1 / self.project.fps, self._show_next_frame)

    def stop(self):
        self.running = False
        self.board.matrix.clear()

    def _do_every(self, period, f, *args):
        """execute a method with a fixed period"""

        # create generator
        def g_tick():
            t = time.time()
            count = 0
            while True:
                count += 1
                yield max(t + count * period - time.time(), 0)

        g = g_tick()
        while self.running:
            time.sleep(next(g))
            f(*args)

    @staticmethod
    def frames_to_string_array(frames):
        # "<U1" is just 1 character (like "r" for red)
        string_array = np.empty_like(frames, dtype="<U1")

        for f, frame in enumerate(frames):
            for i, panel_row in enumerate(frame):
                for j, panel in enumerate(panel_row):
                    for k, row in enumerate(panel):
                        for l, led in enumerate(row):
                            for index, color in enumerate(COLORS):
                                if led == index:
                                    string_array[f][i][j][k][l] = color

        # reshape the array
        """ warning: this is only for 3 panels for now"""
        print(string_array.shape)
        reshaped_array = np.empty(shape=(string_array.shape[0], 8, 24), dtype="<U1")
        for i, frame in enumerate(string_array):
            reshaped_array[i] = frame[0].swapaxes(0, 1).reshape(8, 24)
        return reshaped_array
