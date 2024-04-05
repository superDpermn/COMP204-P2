import random
import copy as cp


def pickRandom(arr):
    random.seed()
    return random.choice(arr)


def linear(t):
    return t


def ease_in_out_expo(t):
    return 0 if t == 0 else 1 if t == 1 else (2**(20*t-10))/2 if t < 0.5 else (2-(2**(-20*t+10)))/2


def ease_in_out_quint(t):
    return 16 * (t**5) if t < 0.5 else 1 - (((-2*t)+2)**5)/2


class Animation:
    def __init__(self, start_pos, end_pos, duration=300, timing_function=ease_in_out_quint, fps=60):
        # define starting, current and end positions
        self.start_pos: list = start_pos
        self.current_pos: list = start_pos
        self.end_pos: list = end_pos

        # define time-related values
        self.duration: float = duration
        self.timing_function = timing_function
        self.fps: int = fps
        self.frame_duration: float = 1 / fps
        self.elapsed_time: float = 0

        # define animation control values
        self.firstCall: bool = True
        self.isActive: bool = False  # start as inactive

    def start(self, target):
        self.start_pos = cp.deepcopy(self.current_pos)
        self.isActive = True
        self.end_pos = target
        self.firstCall = True
        self.update()

    def update(self, delta_time=0):
        if not self.isActive:
            self.current_pos = self.end_pos
            return self.end_pos

        if self.firstCall:
            self.firstCall = False
            self.elapsed_time = 0
            return self.start_pos

        elapsed_time = delta_time + self.elapsed_time
        if elapsed_time >= self.duration:
            self.isActive = False
            self.current_pos = self.end_pos
            return self.end_pos

        progress = elapsed_time / self.duration
        eased_progress = self.timing_function(progress)

        current_pos = [
            self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * eased_progress,
            self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * eased_progress
        ]
        self.current_pos = current_pos
        return current_pos

    def set_fps(self, fps):
        self.fps = fps
        self.frame_duration = 1 / fps
