from customtkinter import CTkToplevel
from lib.funcs import CENTER_WINDOW
from settings import *


class Top_level_form(CTkToplevel):
    # def __init__(self, parent, title):
    #     super().__init__(master=parent)
    #     self.title(title)
    def __init__(self, parent, title, width, height):
        super().__init__(master=parent, fg_color=MAIN_CLR)
        self.title(title)
        CENTER_WINDOW(window=self, width=width, height=height)
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.focus_set()
        self.grab_set()

class Add_po_from(Top_level_form):
    def __init__(self, parent):
        super().__init__(parent=parent, title="Add Purchase Order", width=400, height=400)
