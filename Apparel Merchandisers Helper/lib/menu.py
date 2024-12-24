from customtkinter import CTkFrame, CTkButton
from settings import *


class Menu(CTkFrame):
    def __init__(self, parent, main_frame_funcs):
        super().__init__(master=parent, fg_color=SECONDARY_CLR, corner_radius=4)
        self.grid(column=0, row=1, sticky="nsew")

        # Widgets
        main_buttons_container = CTkFrame(self, fg_color="transparent", corner_radius=0)
        main_buttons_container.place(relx=0.5, rely=0.5, relwidth=1, anchor="center")

        Menu_button(
            parent=main_buttons_container,
            text="Paths",
            main_frame_func=main_frame_funcs["paths"],
        )
        Menu_button(
            parent=main_buttons_container,
            text="Create Style",
            main_frame_func=main_frame_funcs["create style"],
            activ_bool=True,
        )
        Menu_button(
            parent=main_buttons_container,
            text="View Styles",
            main_frame_func=main_frame_funcs["view styles"],
        )
        Menu_button(
            parent=main_buttons_container,
            text="Pricing",
            main_frame_func=main_frame_funcs["pricing"],
        )
        Menu_button(
            parent=main_buttons_container,
            text="Dummy info",
            main_frame_func=main_frame_funcs["dummy"],
        )


class Menu_button(CTkButton):
    def __init__(self, parent, text, main_frame_func, activ_bool=False):
        self.main_frame_func = main_frame_func
        super().__init__(
            master=parent,
            command=self.handle_button_click,
            text=text,
            font=MENU_BUTTONS_FONT,
            text_color=FOURTH_CLR,
            fg_color=MAIN_CLR if activ_bool else "transparent",
            hover_color=MAIN_CLR,
            corner_radius=0,
            height=50,
        )
        self.pack(fill="x")

    def handle_button_click(self):
        # loop on the buttons in the parent frame to set color transparent
        for button in self.master.winfo_children():
            button.configure(fg_color="transparent")

        # Set the color of the clicked button
        self.configure(fg_color=MAIN_CLR)

        # switch the main frame
        self.main_frame_func()
