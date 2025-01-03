from customtkinter import CTk, CTkButton, CTkLabel, set_appearance_mode
from lib.main_frames import Create_style_frame, Paths_frame, View_styles_frame, Pricing_frame, Dummy_info_frame
from lib.menu import Menu
from lib.panels import Color_mode_panel
from lib.database_funcs import DB_CREATE
from lib.funcs import CENTER_WINDOW
from settings import *
from ctypes import windll  # to get the scale factor


class App(CTk):
    def __init__(self):
        # Setup
        super().__init__(fg_color=BLACK_CLR)
        CENTER_WINDOW(window=self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self._set_appearance_mode("dark")
        self.title("")
        self.iconbitmap("empty.ico")
        # self.state("zoomed")
        # self.resizable(False, False)

        self.button= CTkButton(
            master=self,
            text="Change",
            fg_color="red",
            command=lambda: self._set_appearance_mode("light"),
        )
        self.button.place(relx=0.0, rely=0.0, anchor="nw")

        # Initialize parameters
        self.init_parameters()

        # create the database if not exists
        DB_CREATE()

        # Grid layout
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=10, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=7, uniform="a")

        # Widgets
        CTkLabel(
            self,
            text="Apparel Merchandiser Helper",
            font=APP_TITLE_FONT,
            text_color=FOURTH_CLR,
            fg_color=BLACK_CLR,
        ).grid(column=0, columnspan=2, row=0, sticky="nsew")
        self.menu = Menu(parent=self, main_frame_funcs=self.main_frame_funcs)
        self.main_panel = Create_style_frame(parent=self)

        self.color_mode_panel = Color_mode_panel(self, self.toggle_mode)

        self.mainloop()

    def init_parameters(self):
        self.main_frame_funcs = {
            "paths": self.paths,
            "create style": self.create_style,
            "view styles": self.view_styles,
            "pricing": self.pricing,
            "dummy": self.dummy,
        }

    def paths(self):
        self.main_panel.pack_forget()
        self.main_panel = Paths_frame(parent=self)

    def create_style(self):
        self.main_panel.pack_forget()
        self.main_panel = Create_style_frame(parent=self)

    def view_styles(self):
        self.main_panel.pack_forget()
        self.main_panel = View_styles_frame(parent=self)

    def pricing(self):
        self.main_panel.pack_forget()
        self.main_panel = Pricing_frame(parent=self)

    def dummy(self):
        self.main_panel.pack_forget()
        self.main_panel = Dummy_info_frame(parent=self)

    def toggle_mode(self):
        set_appearance_mode(self.color_mode_panel.switch.get())


if __name__ == "__main__":
    App()
