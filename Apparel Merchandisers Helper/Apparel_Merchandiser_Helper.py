from customtkinter import *
from settings import *
from lib.main_frames import *
from lib.menu import *
import ctypes  # to get the scale factor


class App(CTk):
    def __init__(self):
        # Setup
        super().__init__(fg_color=BLACK_CLR)
        self.center_window()
        self._set_appearance_mode("dark")
        self.title("")
        self.iconbitmap("empty.ico")
        self.resizable(False, False)

        # Initialize parameters
        self.init_parameters()

        # Grid layout
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=10, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=7, uniform="a")

        # Widgets
        CTkLabel(
            self,
            text="Apparel Merchandiser Helper",
            font=(FONT_FAMILY, TITLE_FONT_SIZE),
            text_color=FOURTH_CLR,
            fg_color=BLACK_CLR,
        ).grid(column=0, columnspan=2, row=0, sticky="nsew")
        self.menu = Menu(self, self.main_frames_funcs)
        self.main_panel = Create_style_frame(self)

        self.mainloop()

    def center_window(self):
        # window setup to place the window on the center
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        screen_width = self.winfo_screenwidth() * scale_factor
        screen_height = self.winfo_screenheight() * scale_factor
        window_width = WINDOW_WIDTH * scale_factor
        window_height = WINDOW_HEIGHT * scale_factor
        left_point = int((screen_width - window_width) / 2)
        top_point = int((screen_height - window_height) / 2) - 100
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{left_point}+{top_point}")

    def init_parameters(self):
        self.main_frames_funcs = {
            "create style": self.create_style,
            "view styles": self.view_styles,
            "pricing": self.pricing,
            "dummy": self.dummy,
        }

    def create_style(self):
        self.main_panel.pack_forget()
        self.main_panel = Create_style_frame(self)

    def view_styles(self):
        self.main_panel.pack_forget()
        self.main_panel = View_styles_frame(self)

    def pricing(self):
        self.main_panel.pack_forget()
        self.main_panel = Pricing_frame(self)

    def dummy(self):
        self.main_panel.pack_forget()
        self.main_panel = Dummy_info_frame(self)


if __name__ == "__main__":
    App()
