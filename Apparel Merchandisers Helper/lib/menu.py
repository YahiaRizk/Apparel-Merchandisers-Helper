from customtkinter import *
from settings import *


class Menu(CTkFrame):
    def __init__(self, parent, main_frames):
        super().__init__(master=parent, fg_color=SECONDARY_CLR, corner_radius=4)
        self.grid(column=0, row=1, sticky="nsew")

        # Widgets
        main_buttons_container = CTkFrame(self, fg_color="transparent", corner_radius= 0)
        main_buttons_container.place(relx=0.5, rely=0.5, relwidth= 1, anchor="center")

        Menu_button(main_buttons_container, 'Create Style', main_frames['create style'], activ_bool= True)
        Menu_button(main_buttons_container, 'View Styles', main_frames['view styles'])
        Menu_button(main_buttons_container, 'Pricing', main_frames['pricing'])
        Menu_button(main_buttons_container, 'Dummy info', main_frames['dummy'])

class Menu_button(CTkButton):
    def __init__(self, parent, text, main_frame_func, activ_bool= False):
        self.main_frame_func = main_frame_func
        super().__init__(
            master=parent,
            command= self.handle_button_click,
            text=text,
            font= (FONT_FAMILY, MENU_BUTTONS_FONT_SIZE, 'bold'),
            text_color= FOURTH_CLR,
            fg_color=MAIN_CLR if activ_bool else "transparent",
            hover_color=MAIN_CLR,
            corner_radius= 0,
            height= 50,
        )
        self.pack(fill= 'x')

    def handle_button_click(self):
        # loop on the buttons in the parent frame to set color transparent
        for button in self.master.winfo_children():
            button.configure(fg_color= 'transparent')
        
        # Set the color of the clicked button
        self.configure(fg_color= MAIN_CLR)

        # switch the main frame
        self.main_frame_func()



