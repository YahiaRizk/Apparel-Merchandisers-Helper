from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkButton,
    CTkComboBox,
    CTkSwitch,
)
from tkinter import filedialog
from settings import *
from lib.database_funcs import DB_UPDATE_PATH
import tkinter.font as tkFont


class Panel(CTkFrame):
    def __init__(self, parent, label_str, label_width=95):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(fill="x", padx=5, pady=10)

        # widgets
        self.label1 = CTkLabel(
            self,
            text=label_str,
            font=PANEL_LABLE_FONT,
            text_color=FOURTH_CLR,
            width=label_width,
            anchor="w",
            # wraplength=60,
        )
        self.label1.pack(side="left", padx=7)

    def unpack(self):
        self.configure(height=0)
        self.label1.pack_forget()

    def repack(self):
        self.label1.pack(side="left", padx=10)

    def change_label(self, str):
        self.label1.configure(text=str)


class Entry_panel(Panel):
    def __init__(
        self,
        parent,
        label_str,
        data_var,
        label_width=95,
        entry_width=200,
        int_bool=False,
    ):
        super().__init__(parent=parent, label_str=label_str, label_width=label_width)
        self.data_var = data_var

        # widgets
        self.entry = CTkEntry(
            self,
            width=entry_width,
            font=FORM_ENTRY_FONT,
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
        if self.entry.get() == "":
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


class Path_panel(Entry_panel):
    def __init__(
        self,
        parent,
        label_str,
        data_var,
        customer,
        label_width=20,
        entry_width=500,
        int_bool=False,
    ):
        super().__init__(
            parent=parent,
            label_str=label_str,
            label_width=label_width,
            data_var=data_var,
            entry_width=entry_width,
        )

        # turn data_var and customer key into a property
        self.entry_var = data_var
        self.customer = customer

        # widgets
        button = CTkButton(
            self,
            text="...",
            fg_color=SECONDARY_CLR,
            text_color=FOURTH_CLR,
            hover_color=THIRD_CLR,
            width=30,
            command=self.get_path,
        )
        button.pack(side="left", padx=10)

    def get_path(self):
        # get the path from the user
        path = filedialog.askdirectory()

        # set the path to entry var
        self.entry_var.set(path)

        # update the path in the database
        DB_UPDATE_PATH(self.customer, path)


class Combobox_panel(Panel):
    def __init__(
        self,
        parent,
        label_str1,
        options1,
        data_var1,
        label_width=95,
        label_str2=None,
        options2=None,
        data_var2=None,
        width=90,
    ):
        super().__init__(parent=parent, label_str=label_str1, label_width=label_width)

        # widgets
        self.combobox1 = CTkComboBox(
            self,
            width=width,
            values=options1,
            font=FORM_ENTRY_FONT,
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
                self, text=label_str2, text_color=FOURTH_CLR, font=PANEL_LABLE_FONT
            )
            self.label2.pack(side="left", padx=10)

            self.combobox2 = CTkComboBox(
                self,
                width=width,
                values=options2,
                font=FORM_ENTRY_FONT,
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
            font=BUTTON_FONT,
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
            font=BUTTON_FONT,
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
        buttons_container.pack(pady=20)

        self.delete_button = Simple_button(
            parent=buttons_container, text="View Style", func=view_func
        )
        self.delete_button = Simple_button(
            parent=buttons_container, text="Delete Selected", func=delete_func
        )
        self.archive_button = Simple_button(
            parent=buttons_container, text="Archive Selected", func=archive_func
        )


class Simple_button(CTkButton):
    def __init__(self, parent, text, func):
        super().__init__(
            master=parent,
            text=text,
            command=func,
            font=BUTTON_FONT,
            text_color=FOURTH_CLR,
            fg_color=SECONDARY_CLR,
            hover_color=THIRD_CLR,
        )
        self.pack(side="left", padx=10, ipadx=10, ipady=5)


class Add_path_panel(CTkFrame):
    def __init__(self, parent, entry_var, func):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(side="bottom", pady=20)

        # widgets
        CTkEntry(
            master=self,
            fg_color=THIRD_CLR,
            font=FORM_ENTRY_FONT,
            text_color=MAIN_CLR,
            border_color=SECONDARY_CLR,
            border_width=1,
            textvariable=entry_var,
        ).pack(side="left")

        # add path button
        CTkButton(
            master=self,
            text="Add Customer",
            width=50,
            command=func,
            font=SMALL_BUTTON_FONT,
            text_color=FOURTH_CLR,
            fg_color=SECONDARY_CLR,
            hover_color=THIRD_CLR,
        ).pack(side="left", padx=10)


class Color_mode_panel(CTkFrame):
    def __init__(self, parent, mode_func):
        super().__init__(parent, fg_color="transparent")
        self.place(x=20, y=0, anchor="nw")

        # widgets
        CTkLabel(
            master=self,
            text="Dark",
            font=("Calibri", 11, "bold"),
            fg_color="transparent",
            text_color=FOURTH_CLR,
        ).pack(side="left")

        self.switch = CTkSwitch(
            master=self,
            text="",
            fg_color=SECONDARY_CLR,
            progress_color=SECONDARY_CLR,
            button_color=THIRD_CLR,
            button_hover_color=FOURTH_CLR,
            width=20,
            onvalue="light",
            offvalue="dark",
            command=mode_func,
        )
        self.switch.pack(side="left", padx=(10, 0))

        CTkLabel(
            master=self,
            text="Light",
            font=("Calibri", 11, "bold"),
            fg_color="transparent",
            text_color=FOURTH_CLR,
            anchor="w",
        ).pack(side="left")
