from customtkinter import *
from settings import *


class Panel(CTkFrame):
    def __init__(self, parent, label_str):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(fill="x", padx=5, pady=10)

        # widgets
        self.label1 = CTkLabel(
            self,
            text=label_str,
            text_color=FOURTH_CLR,
            width=60,
            anchor="w",
            wraplength=60,
        )
        self.label1.pack(side="left", padx=10)

    def unpack(self):
        self.configure(height=0)
        self.label1.pack_forget()

    def repack(self):
        self.label1.pack(side="left", padx=10)

    def change_label(self, str):
        self.label1.configure(text=str)


class Entry_panel(Panel):
    def __init__(self, parent, label_str, data_var, entry_width=200, int_bool=False):
        super().__init__(parent=parent, label_str=label_str)
        self.data_var = data_var

        # widgets
        self.entry = CTkEntry(
            self,
            width=entry_width,
            fg_color=THIRD_CLR,
            text_color=MAIN_CLR,
            border_color=SECONDARY_CLR,
            border_width=1,
            textvariable=data_var,
        )
        self.entry.pack(side="left")

        # bind a function to entry if int_bool is true
        if int_bool:
            self.old_value = ""
            self.entry.bind("<KeyRelease>", self.check_int)

    def check_int(self, event):
        if self.entry.get() == '':
            pass
        else:
            if self.entry.get().isdigit():
                self.old_value = self.entry.get()
            else:
                self.data_var.set(self.old_value)

    def unpack(self):
        super().unpack()
        self.entry.pack_forget()

    def repack(self):
        super().repack()
        self.entry.pack(side="left")


class Combobox_panel(Panel):
    def __init__(
        self,
        parent,
        label_str1,
        options1,
        data_var1,
        label_str2=None,
        options2=None,
        data_var2=None,
        width=90,
    ):
        super().__init__(parent=parent, label_str=label_str1)

        # widgets
        self.combobox1 = CTkComboBox(
            self,
            width=width,
            values=options1,
            text_color=MAIN_CLR,
            fg_color=THIRD_CLR,
            button_color=SECONDARY_CLR,
            border_width=0,
            variable=data_var1,
            # justify= 'center'
        )
        self.combobox1.pack(side="left")

        if label_str2:
            self.label2 = CTkLabel(
                self, text=label_str2, text_color=FOURTH_CLR, width=60
            )
            self.label2.pack(side="left", padx=10)
            self.combobox2 = CTkComboBox(
                self,
                width=width,
                values=options2,
                text_color=MAIN_CLR,
                fg_color=THIRD_CLR,
                button_color=SECONDARY_CLR,
                border_width=0,
                variable=data_var2,
            )
            self.combobox2.pack(side="left")

    def unpack(self):
        super().unpack()
        self.combobox1.pack_forget()

    def repack(self):
        super().repack()
        self.combobox1.pack(side="left")

    def unpack_sec_combobox(self):
        self.label2.pack_forget()
        self.combobox2.pack_forget()

    def repack_sec_combobox(self):
        self.label2.pack(side="left", padx=10)
        self.combobox2.pack(side="left")


class Submit_panel(CTkFrame):
    def __init__(self, parent, submit_func, reset_func):
        super().__init__(
            master=parent,
            fg_color="transparent",
            corner_radius=0,
            border_color=SECONDARY_CLR,
            border_width=1,
        )
        self.grid(column=0, row=1, columnspan=2, sticky="nsew", padx=(10, 0))

        # grid layout
        self.columnconfigure((0, 1), weight=1, uniform="a")
        self.columnconfigure(2, weight=2, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")

        # widgets
        CTkButton(
            self,
            text="Submit",
            fg_color=SECONDARY_CLR,
            hover_color=THIRD_CLR,
            text_color=FOURTH_CLR,
            font=(FONT_FAMILY, FONT_SIZE, "bold"),
            width=100,
            height=35,
            command=submit_func,
        ).grid(column=0, row=0)

        CTkButton(
            self,
            text="Reset",
            fg_color=SECONDARY_CLR,
            hover_color=THIRD_CLR,
            text_color=FOURTH_CLR,
            font=(FONT_FAMILY, FONT_SIZE, "bold"),
            width=100,
            height=35,
            command=reset_func,
        ).grid(column=1, row=0)


class Buttons_panel(CTkFrame):  # for style view tab
    def __init__(self, parent, view_func, delete_func, archive_func):
        super().__init__(
            master=parent,
            fg_color="transparent",
            # height= 100,
            border_width=1,
            border_color=FOURTH_CLR,
        )
        self.pack(
            side="bottom", fill="x", padx=10
        )  # side bottom to pack it before the table for scroll fix

        # Widgets
        buttons_container = CTkFrame(self, fg_color="transparent")
        buttons_container.pack(pady= 20)

        self.delete_button = Simple_button(buttons_container, text="View Style", func= view_func)
        self.delete_button = Simple_button(buttons_container, text="Delete Selected", func= delete_func)
        self.archive_button = Simple_button(buttons_container, text="Archive Selected", func= archive_func)


class Simple_button(CTkButton):
    def __init__(self, parent, text, func):
        super().__init__(
            master=parent,
            text=text,
            command= func,
            font=(FONT_FAMILY, MENU_BUTTONS_FONT_SIZE),
            text_color=FOURTH_CLR,
            fg_color=SECONDARY_CLR,
            hover_color=THIRD_CLR,
        )
        self.pack(side= 'left', padx= 10, ipadx= 10, ipady= 5)
