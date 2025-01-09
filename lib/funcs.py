from ctypes import windll  # to get the scale factor

def CENTER_WINDOW(window, width, height):
    # window setup to place the window on the center
    scale_factor = windll.shcore.GetScaleFactorForDevice(0) / 100
    screen_width = window.winfo_screenwidth() * scale_factor
    screen_height = window.winfo_screenheight() * scale_factor
    window_width = width * scale_factor
    window_height = height * scale_factor
    left_point = int((screen_width - window_width) / 2)
    top_point = int((screen_height - window_height) / 2) - 50
    window.geometry(f"{width}x{height}+{left_point}+{top_point}")

def CANCEL_LISTS_FROM_DICT_VALUES(dict):
    return {key: value[0] if isinstance(value, list) else value for key, value in dict.items()}

def GET_VALUE_IF_NOT_LIST(value, index):
    # check if the value is a list if not return the value
    if isinstance(value, list):
        return value[index] if index < len(value) else ""
    else:
        return value