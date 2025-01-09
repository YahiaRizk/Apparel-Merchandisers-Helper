from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkImage
from lib.top_level_forms import Add_color_form
from lib.database_funcs import DB_ADD_COLOR
from lib.funcs import CANCEL_LISTS_FROM_DICT_VALUES, GET_VALUE_IF_NOT_LIST
from settings import *
from PIL import Image


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
            add_func=self.open_add_color_form,
            edit_func=self.open_edit_po_form,
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
            self.create_color_row_widgts(i, self.data)

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

    def create_color_row_widgts(self, row_index, data):
        Simple_label(
            self.data_container,
            text=GET_VALUE_IF_NOT_LIST(data["teams"], row_index),
            column=7,
            row=self.header_rows + row_index,
            colspan=2,
        )
        Simple_label(
            self.data_container,
            text=GET_VALUE_IF_NOT_LIST(data["color_codes"], row_index),
            column=9,
            row=self.header_rows + row_index,
            colspan=2,
        )
        Simple_label(
            self.data_container,
            text=GET_VALUE_IF_NOT_LIST(data["piece1_colors"], row_index),
            column=11,
            row=self.header_rows + row_index,
            colspan=2,
        )
        Simple_label(
            self.data_container,
            text=GET_VALUE_IF_NOT_LIST(data["piece2_colors"], row_index),
            column=13,
            row=self.header_rows + row_index,
            colspan=2,
        )
        Simple_label(
            self.data_container,
            text=GET_VALUE_IF_NOT_LIST(data["color_qtys"], row_index),
            column=15,
            row=self.header_rows + row_index,
            colspan=2,
        )

    def add_color(self, color_data):
        # add po number to the returned color data
        color_data["po_num"] = self.data["po_num"]

        # increase the row count
        self.data_rows += 1
        # create the color row widgets
        self.create_color_row_widgts(self.data_rows, color_data)
        # update rowspan for po data widgets
        # self.update_rowspan() #Hold for now

        # convert color_data dict to suitable format for database(cancels the lists)
        color_data= CANCEL_LISTS_FROM_DICT_VALUES(color_data)
        # add to database
        DB_ADD_COLOR(color_data)

    def update_rowspan(self):
        """# Track processed starting columns
        processed_columns = set()
        # put desired widgets in one list
        widgets = (
            list(self.data_container.children.values())[:9]
            + list(self.data_container.children.values())[17:]
        )
        for widgt in widgets:
            # Get the grid info
            info = widgt.grid_info()
            # Get the starting column for the widget
            start_column = info.get("column", 0)
            # get the current widget column span
            col_span = info.get("colspan", 1)
            # only update widgts that are not already processed
            if start_column not in processed_columns:
                # update the rowspan for the widget
                # info["rowspan"] = self.data_rows
                # update the processed columns
                processed_columns.update(range(start_column, start_column + col_span))
                widgt.grid(
                    row=info.get("row", 0),
                    column=start_column,
                    rowspan=self.data_rows - self.header_rows,
                    columnspan=col_span,
                    sticky="nsew",
                )
        """

    def open_add_color_form(self):
        Add_color_form(parent=self, callback_func=self.add_color)

    def open_edit_po_form(self):
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
