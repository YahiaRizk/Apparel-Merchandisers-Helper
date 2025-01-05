from customtkinter import CTkToplevel, CTkLabel, CTkButton
# from lib.panels import Simple_button
from lib.funcs import CENTER_WINDOW
from settings import *


class Top_level_form(CTkToplevel):
    def __init__(self, parent, title, width, height):
        super().__init__(master=parent, fg_color=MAIN_CLR)
        self.title(title)
        CENTER_WINDOW(window=self, width=width, height=height)
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.focus_set()
        self.grab_set()

        # Widgets
        # - title
        CTkLabel(
            self,
            text=title,
            font=APP_TITLE_FONT,
            text_color=FOURTH_CLR
        ).pack(fill="x", pady=10)

        # -submit button
        CTkButton(
            self,
            text="Submit",
            fg_color=SECONDARY_CLR,
            hover_color=THIRD_CLR,
            text_color=FOURTH_CLR,
            font=BUTTON_FONT,
            width=100,
            command=self.submit,
        ).pack(side="bottom", pady=30)

    def submit(self):
        self.grab_release()
        self.destroy()
        



class Add_po_from(Top_level_form):
    def __init__(self, parent):
        super().__init__(parent=parent, title="Add Purchase Order", width=400, height=400)
