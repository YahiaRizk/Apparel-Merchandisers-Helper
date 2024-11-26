from customtkinter import CTkToplevel, CTkLabel
from settings import *

class View_style_top_level(CTkToplevel):
    def __init__(self, s_name):
        super().__init__(fg_color= MAIN_CLR)
        self.geometry(f'1200x750')
        self.title('Style Details')
        # self.lift() 
        self.attributes("-topmost", True)
        self.after(10, lambda: self.attributes("-topmost", False))

        CTkLabel(self, text= s_name).pack(expand= True, fill= 'both')

