from customtkinter import *
from settings import *


class View_style_top_level(CTkToplevel):
    def __init__(self, main_data, pos_data):
        super().__init__(fg_color=MAIN_CLR)
        # setup
        self.geometry(f"1200x750")
        self.title(f'Style "{main_data["group_name"]}" Details')
        self.attributes("-topmost", True)
        self.after(10, lambda: self.attributes("-topmost", False))

        # data
        self.main_data = main_data
        self.pos_data = pos_data

        # widgets
        self.main_info_panel = Main_info_panel(parent=self, data=self.main_data)


class Main_info_panel(CTkFrame):
    def __init__(self, parent, data):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="x")

        # data
        self.data = data

        # layout
        self.columnconfigure(tuple(range(24)), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2), weight=1, uniform="a")

        # widgets
        # - main info widgets
        self.create_main_info_widgets()

    def create_main_info_widgets(self):
        # title (group name)
        CTkLabel(
            self,
            text=self.data["group_name"],
            font=APP_TITLE_FONT,
            text_color=FOURTH_CLR,
        ).grid(column=0, columnspan=4, row=0, rowspan=3, sticky="nsew")

        # main info headers
        Simple_label(self, text="ID", column=5, row=0, font=TABLE_HEADER_FONT)
        Simple_label(self, text="Customer", column=6, row=0, colspan=2, font=TABLE_HEADER_FONT)
        Simple_label(self, text="Type", column=8, row=0, colspan=2, font=TABLE_HEADER_FONT)
        Simple_label(self, text="PCS", column=10, row=0, colspan=2, font=TABLE_HEADER_FONT)
        Simple_label(self, text="Fabrics", column=12, row=0, colspan=3, font=TABLE_HEADER_FONT)
        Simple_label(self, text="GSM", column=15, row=0, colspan=2, font=TABLE_HEADER_FONT)
        Simple_label(self, text="Total QTY", column=17, row=0, colspan=2, font=TABLE_HEADER_FONT)
        Simple_label(self, text="RCVD Date", column=19, row=0, colspan=2, font=TABLE_HEADER_FONT)

        # main info data
        Simple_label(self, text=self.data["group_id"], column=5, row=1, rowspan=2)
        Simple_label(self, text=self.data["customer"], column=6, row=1, colspan=2, rowspan=2)
        Simple_label(self, text=self.data["garment_type"], column=8, row=1, colspan=2, rowspan=2)
        Simple_label(
            self,
            text=f"{self.data['piece1_type']}\n{self.data['piece1_type']}",
            column=10,
            row=1,
            colspan=2,
            rowspan=2,
        )
        Simple_label(self, text="\n".join(self.data["fabric_types"]), column=12, row=1, colspan=3, rowspan=2)
        Simple_label(self, text="\n".join(self.data["fabric_gsms"]), column=15, row=1, colspan=2, rowspan=2)
        Simple_label(self, text=self.data["total_qty"], column=17, row=1, colspan=2, rowspan=2)
        Simple_label(self, text=self.data["rcvd_date"], column=19, row=1, colspan=2, rowspan=2)


class Simple_label(CTkLabel):
    def __init__(self, parent, text, row, column, colspan=1, rowspan=1, font=PANEL_LABLE_FONT):
        super().__init__(parent, text=text, font=font, fg_color="transparent", text_color=FOURTH_CLR)
        self.grid(
            column=column,
            row=row,
            columnspan=colspan,
            rowspan=rowspan,
            sticky="nsew",
        )
