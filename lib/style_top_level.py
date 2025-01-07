from customtkinter import CTkFrame, CTkToplevel, CTkScrollableFrame
from lib.style_top_level_panels import Main_info_panel, Po_data_panel
from lib.top_level_forms import Add_po_form
from lib.panels import Simple_button
from lib.database_funcs import DB_ADD_PO
from lib.funcs import CENTER_WINDOW
from settings import *


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
        Simple_button(self, text="Add PO", func=self.open_add_po_from, side="top").pack(
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

    def open_add_po_from(self):
        Add_po_form(parent=self, callback_func=self.add_po)

    def add_po(self, data):
        # manage the data get from the form (po_data, color_data)
        po_data, color_data = data
        # append id to po_data dict
        po_data["group_id"] = self.main_data["group_id"]
        # merge data to create po_data_panel
        merged_data = {**po_data, **color_data}
        # create po_data_panel and add to po_panels_container
        Po_data_panel(
            parent=self.po_panels_container,
            data=merged_data,
        )

        # convert color_data dict to suitable format for database(cancels the lists)
        color_data = {
            key: value[0] if isinstance(value, list) else value for key, value in color_data.items()
        }

        # add to database
        DB_ADD_PO(po_data, color_data)
