from customtkinter import CTkToplevel, CTkLabel
from settings import MAIN_CLR

class View_style_top_level(CTkToplevel):
    def __init__(self, main_data, pos_data):
        super().__init__(fg_color= MAIN_CLR)
        # setup
        self.geometry(f'1200x750')
        self.title(f'Style \"{main_data["group_name"]}\" Details')
        self.attributes("-topmost", True)
        self.after(10, lambda: self.attributes("-topmost", False))

        # data
        self.main_data = main_data
        self.pos_data = pos_data

        # widgets
        



