from customtkinter import CTkFrame, CTkToplevel, CTkLabel, CTkButton, CTkScrollableFrame, CTkImage
from lib.top_level_forms import Add_po_from, Top_level_form
from lib.panels import Simple_button
from lib.funcs import CENTER_WINDOW
from settings import *
from PIL import Image


class View_style_top_level(CTkToplevel):
    def __init__(self, main_data, pos_data):
        super().__init__(fg_color=MAIN_CLR)
        # setup
        CENTER_WINDOW(window=self, width=1200, height=750)
        self.title(f'Style "{main_data["group_name"]}" Details')
        self.attributes("-topmost", True)
        self.after(10, lambda: self.attributes("-topmost", False))
        # self.state("zoomed")

        # data
        self.main_data = main_data
        self.pos_data = pos_data

        # widgets
        # - main info panel
        self.main_info_panel = Main_info_panel(parent=self, data=self.main_data)

        # - add po button
        Simple_button(self, text="Add PO", func=self.add_po, side="top").pack(
            anchor="w", ipady=0, ipadx=0
        )

        # - rest of the data container
        self.container = CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=SECONDARY_CLR,
            scrollbar_button_hover_color=THIRD_CLR,
        )
        self.container.pack(fill="both", expand=True)

        # - pos data panels
        # -- po panels container
        self.po_panels_container = CTkFrame(self.container, fg_color="transparent")
        self.po_panels_container.pack(fill="x")
        for po in self.pos_data:
            Po_data_panel(parent=self.po_panels_container, data=po)

    def add_po(self):
        print("add po")
        Add_po_from(parent=self)


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
            text=f"{self.data['piece1_type']}\n{self.data['piece2_type']}",
            column=10,
            row=1,
            colspan=2,
            rowspan=2,
        )
        Simple_label(
            self, text="\n".join(self.data["fabric_types"]), column=12, row=1, colspan=3, rowspan=2
        )
        Simple_label(
            self, text="\n".join(self.data["fabric_gsms"]), column=15, row=1, colspan=2, rowspan=2
        )
        Simple_label(self, text=self.data["total_qty"], column=17, row=1, colspan=2, rowspan=2)
        Simple_label(self, text=self.data["rcvd_date"], column=19, row=1, colspan=2, rowspan=2)


class Po_data_panel(CTkFrame):
    def __init__(self, parent, data):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="x", pady=2)

        # data
        self.data = data
        # - calculate rows count with number of color codes  2 (for headers and po title)
        self.data_rows = len(self.data["color_codes"])
        self.header_rows = 1

        # widgets
        # -title (po panel)
        self.header_panel = Po_header_panel(
            parent=self,
            po_num=self.data["po_num"],
            add_func=self.add_color,
            edit_func=self.edit_po,
            delete_func=self.delete_po,
        )

        # -container widget for handle a little padding
        self.container = CTkFrame(self, fg_color=SECONDARY_CLR)
        self.container.pack(fill="both", padx=5)

        # data container for the grid layout
        self.data_container = CTkFrame(self.container, fg_color="transparent")
        self.data_container.pack(fill="both", padx=5)

        # -layout
        self.data_container.columnconfigure(tuple(range(24)), weight=1, uniform="a")
        self.data_container.rowconfigure(
            tuple(range(self.data_rows + self.header_rows)), weight=1, uniform="a"
        )

        # -po header widgets
        self.create_po_header_widgets()
        # -po data widgets
        self.create_po_data_widgets()

    def create_po_header_widgets(self):

        # po headers
        Simple_label(
            self.data_container,
            text="Style#",
            column=0,
            row=self.header_rows - 1,
            colspan=2,
            font=TABLE_HEADER_FONT,
        )
        Simple_label(
            self.data_container,
            text="SMU",
            column=2,
            row=self.header_rows - 1,
            font=TABLE_HEADER_FONT,
        )
        Simple_label(
            self.data_container,
            text="Size Range",
            column=3,
            row=self.header_rows - 1,
            colspan=2,
            font=TABLE_HEADER_FONT,
        )
        Simple_label(
            self.data_container,
            text="Ratio",
            column=5,
            row=self.header_rows - 1,
            colspan=2,
            font=TABLE_HEADER_FONT,
        )
        Simple_label(
            self.data_container,
            text="Team",
            column=7,
            row=self.header_rows - 1,
            colspan=2,
            font=TABLE_HEADER_FONT,
        )
        Simple_label(
            self.data_container,
            text="Color Code",
            column=9,
            row=self.header_rows - 1,
            colspan=2,
            font=TABLE_HEADER_FONT,
        )
        Simple_label(
            self.data_container,
            text="Piece 1 Color",
            column=11,
            row=self.header_rows - 1,
            colspan=2,
            font=TABLE_HEADER_FONT,
        )
        Simple_label(
            self.data_container,
            text="Piece 2 Color",
            column=13,
            row=self.header_rows - 1,
            colspan=2,
            font=TABLE_HEADER_FONT,
        )
        Simple_label(
            self.data_container,
            text="Color QTY",
            column=15,
            row=self.header_rows - 1,
            colspan=2,
            font=TABLE_HEADER_FONT,
        )
        Simple_label(
            self.data_container,
            text="PO Total QTY",
            column=17,
            row=self.header_rows - 1,
            colspan=2,
            font=TABLE_HEADER_FONT,
        )
        Simple_label(
            self.data_container,
            text="Price",
            column=19,
            row=self.header_rows - 1,
            colspan=2,
            font=TABLE_HEADER_FONT,
        )
        Simple_label(
            self.data_container,
            text="Shipping Date",
            column=21,
            row=self.header_rows - 1,
            colspan=3,
            font=TABLE_HEADER_FONT,
        )

    def create_po_data_widgets(self):
        # first 4 columns(style, smu, size range, ratio)
        Simple_label(
            self.data_container,
            text=self.data["style_name"],
            column=0,
            row=self.header_rows,
            colspan=2,
            rowspan=self.data_rows,
        )
        Simple_label(
            self.data_container,
            text=self.data["smu"],
            column=2,
            row=self.header_rows,
            rowspan=self.data_rows,
        )
        Simple_label(
            self.data_container,
            text=self.data["size_range"],
            column=3,
            row=self.header_rows,
            colspan=2,
            rowspan=self.data_rows,
        )
        Simple_label(
            self.data_container,
            text=self.data["ratio"],
            column=5,
            row=self.header_rows,
            colspan=2,
            rowspan=self.data_rows,
        )

        # next 5 columns(team, color code, pc 1 color, pc 2 color, color qty)
        # need to be repeated for each data on the list
        for i in range(self.data_rows):
            Simple_label(
                self.data_container,
                text=self.data["teams"][i],
                column=7,
                row=self.header_rows + i,
                colspan=2,
            )
            Simple_label(
                self.data_container,
                text=self.data["color_codes"][i],
                column=9,
                row=self.header_rows + i,
                colspan=2,
            )
            Simple_label(
                self.data_container,
                text=self.data["piece1_colors"][i],
                column=11,
                row=self.header_rows + i,
                colspan=2,
            )
            Simple_label(
                self.data_container,
                text=self.data["piece2_colors"][i],
                column=13,
                row=self.header_rows + i,
                colspan=2,
            )
            Simple_label(
                self.data_container,
                text=self.data["color_qtys"][i],
                column=15,
                row=self.header_rows + i,
                colspan=2,
            )

        # last 3 columns(po total qty, price, shipping date)
        Simple_label(
            self.data_container,
            text=self.data["po_qty"],
            column=17,
            row=self.header_rows,
            colspan=2,
            rowspan=self.data_rows,
        )
        Simple_label(
            self.data_container,
            text=f"{self.data['price']} $",
            column=19,
            row=self.header_rows,
            colspan=2,
            rowspan=self.data_rows,
        )
        Simple_label(
            self.data_container,
            text=self.data["shipping_date"],
            column=21,
            row=self.header_rows,
            colspan=3,
            rowspan=self.data_rows,
        )

    def add_color(self):
        print("add color")

    def edit_po(self):
        print("edit po")

    def delete_po(self):
        print("delete po")


class Po_header_panel(CTkFrame):
    def __init__(self, parent, po_num, add_func, edit_func, delete_func):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(fill="x", padx=5, pady=(5, 0))

        # widgets
        # -po number label
        CTkLabel(
            self,
            text=f"PO# {po_num}",
            font=MENU_BUTTONS_FONT,
            text_color=FOURTH_CLR,
            anchor="w",
        ).pack(side="left")

        # -buttons container
        self.buttons_container = CTkFrame(self, fg_color="transparent")
        self.buttons_container.pack(side="right")
        # --buttons
        # ---create icons images
        delete_icon = CTkImage(
            light_image=Image.open(r"lib\ico\delete_light.png"),
            dark_image=Image.open(r"lib\ico\delete_dark.png"),
            size=(15, 15),
        )
        edit_icon = CTkImage(
            light_image=Image.open(r"lib\ico\edit_light.png"),
            dark_image=Image.open(r"lib\ico\edit_dark.png"),
            size=(15, 15),
        )
        add_icon = CTkImage(
            light_image=Image.open(r"lib\ico\add_light.png"),
            dark_image=Image.open(r"lib\ico\add_dark.png"),
            size=(15, 15),
        )

        # ---buttons widgets
        # ----delete button
        Icon_button(self.buttons_container, icon=delete_icon, func=delete_func)
        # ----edit button
        Icon_button(self.buttons_container, icon=edit_icon, func=edit_func)
        # ----add button
        Icon_button(self.buttons_container, icon=add_icon, func=add_func)


class Simple_label(CTkLabel):
    def __init__(self, parent, text, row, column, colspan=1, rowspan=1, font=PANEL_LABLE_FONT):
        super().__init__(
            parent,
            text=text,
            font=font,
            # fg_color=SECONDARY_CLR,
            text_color=FOURTH_CLR,
        )
        self.grid(
            column=column,
            row=row,
            columnspan=colspan,
            rowspan=rowspan,
            sticky="nsew",
            # padx=1,
            # pady=1,
        )


class Icon_button(CTkButton):
    def __init__(self, parent, icon, func):
        super().__init__(
            parent,
            text="",
            image=icon,
            text_color=FOURTH_CLR,
            fg_color="transparent",
            hover_color=THIRD_CLR,
            width=15,
            height=15,
            command=func,
        )
        self.pack(side="right", padx=2)
