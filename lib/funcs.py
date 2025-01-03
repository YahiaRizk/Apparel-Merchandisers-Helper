from ctypes import windll  # to get the scale factor
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

def CENTER_WINDOW(window):
    # window setup to place the window on the center
    scale_factor = windll.shcore.GetScaleFactorForDevice(0) / 100
    screen_width = window.winfo_screenwidth() * scale_factor
    screen_height = window.winfo_screenheight() * scale_factor
    window_width = WINDOW_WIDTH * scale_factor
    window_height = WINDOW_HEIGHT * scale_factor
    left_point = int((screen_width - window_width) / 2)
    top_point = int((screen_height - window_height) / 2) - 50
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{left_point}+{top_point}")