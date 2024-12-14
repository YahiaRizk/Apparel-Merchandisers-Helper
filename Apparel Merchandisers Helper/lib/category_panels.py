# from customtkinter import *
from settings import *
from lib.panels import *
from lib.Window_Separator import CTkWindowSeparator


class Category_panel(CTkFrame):  # for create style frame
    def __init__(self, parent, label_text, scrollable=False):
        super().__init__(master=parent)
        self.pack(expand=True, fill="both")

        # grid layout
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=7, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")

        # Widgets
        # -Create the left side frame contain the section label
        label_frame = CTkFrame(self, fg_color=SECONDARY_CLR, corner_radius=0)
        label_frame.grid(column=0, row=0, sticky="nsew")
        self.label = CTkLabel(
            label_frame,
            text=label_text,
            text_color=FOURTH_CLR,
            font=(FONT_FAMILY, FONT_SIZE, "bold"),
            wraplength=75,
            justify="left",
            anchor="w",
        )
        self.label.pack(fill="x", padx=5, pady=10)

        # -Frame contains the data form
        if scrollable:
            self.data_frame = CTkScrollableFrame(
                self,
                fg_color=MAIN_CLR,
                corner_radius=0,
                scrollbar_button_color=SECONDARY_CLR,
                scrollbar_button_hover_color=THIRD_CLR,
            )
        else:
            self.data_frame = CTkFrame(self, fg_color=MAIN_CLR, corner_radius=0)

        self.data_frame.grid(column=1, row=0, sticky="nsew")

class Main_info_panel(Category_panel):
    def __init__(self, parent, label_text, data_vars, scrollable=False):
        super().__init__(parent=parent, label_text=label_text, scrollable=scrollable)
        self.data_vars = data_vars

        # widgets
        Entry_panel(self.data_frame, "Style# :", data_vars["group_name"])
        Combobox_panel(self.data_frame, "Brand :", BRAND_OPT, data_vars["brand"])
        Combobox_panel(
            self.data_frame, "Brand / Team :", BRAND_TEAM_OPT, data_vars["brand_team"]
        )
        Combobox_panel(
            self.data_frame, "Garment Type :", TYPE_OPT, data_vars["garment_type"]
        )
        self.piece_type = Combobox_panel(
            parent=self.data_frame,
            label_str1="Piece 1 :",
            options1=PIECE_OPT,
            data_var1=data_vars["piece1_type"],
            label_str2="Piece 2 :",
            options2=PIECE_OPT,
            data_var2=data_vars["piece2_type"],
        )
        Entry_panel(
            self.data_frame,
            "Total QTY :",
            data_vars["total_qty"],
            entry_width=120,
            int_bool=True,
        )
        Entry_panel(self.data_frame, "Date RCVD :", data_vars["rcvd_date"])

class Fabric_panel(Category_panel):
    def __init__(self, parent, label_text, data_vars, scrollable=False):
        super().__init__(parent=parent, label_text=label_text, scrollable=scrollable)
        self.pack_configure(padx=0)

        # data
        self.data_vars = data_vars

        # Widgets
        # - add first fabric item
        Fabric_item(parnet=self.data_frame, data_vars=self.data_vars, fabric_panel=self)

        # -create a button to add fabric
        self.add_fabric_button = CTkButton(
            self.data_frame,
            text="Add Fabric",
            font=(FONT_FAMILY, FONT_SIZE),
            text_color=FOURTH_CLR,
            fg_color=SECONDARY_CLR,
            hover_color=THIRD_CLR,
            command=lambda: Fabric_item(
                parnet= self.data_frame, data_vars= self.data_vars, fabric_panel= self
            ),
        )
        self.add_fabric_button.pack(pady=(0, 5))

class Fabric_item(CTkFrame):  # for fabric panel
    # variable to keep track of the number of created fabric
    fabric_num = 0

    def __init__(self, parnet, data_vars, fabric_panel):
        super().__init__(parnet, fg_color="transparent")
        self.pack(fill="x")
        Fabric_item.fabric_num += 1

        # remove the add_fabric_button from the layout
        if hasattr(fabric_panel, "add_fabric_button"):
            fabric_panel.add_fabric_button.pack_forget()

        # create data
        self.data = {
            "fabric_type": StringVar(),
            "fabric_description": StringVar(),
            "fabric_gsm": IntVar(),
        }
        # append the data to fabrics data list
        data_vars.append(self.data)

        # widgets
        self.fabric_type = Combobox_panel(
            parent=self,
            label_str1=f"Fabric {Fabric_item.fabric_num} Type :",
            options1=FABRICS_OPT,
            data_var1=self.data["fabric_type"],
            width=200,
        )

        self.description = Entry_panel(
            parent=self,
            label_str=f"Description :",
            data_var=self.data["fabric_description"],
        )

        self.fabric_gsm = Combobox_panel(
            parent=self,
            label_str1=f"Fabric {Fabric_item.fabric_num} GSM :",
            options1=GSM_OPT,
            data_var1=self.data["fabric_gsm"],
        )

        # Make a separator to separate fabrics
        CTkWindowSeparator(self, length=120, color=SECONDARY_CLR).pack(pady=10)

        # repack add_fabric_button if exists in Fabric_panel
        if hasattr(fabric_panel, "add_fabric_button"):
            fabric_panel.add_fabric_button.pack(pady=(0, 5))
