from customtkinter import CTkToplevel, CTkFrame, CTkLabel, CTkButton, StringVar
from lib.panels import Entry_panel, Combobox_panel
from lib.style_top_level_panels import Po_data_panel
from lib.funcs import CENTER_WINDOW
from lib.database_funcs import DB_ADD_PO
from settings import *


class Top_level_form(CTkToplevel):
    def __init__(self, parent, title, width, height):
        super().__init__(master=parent, fg_color=MAIN_CLR)
        self.title(title)
        CENTER_WINDOW(window=self, width=width, height=height)
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.focus_set()
        self.grab_set()

        # Widgets
        # - title
        CTkLabel(
            self,
            text=title,
            font=APP_TITLE_FONT,
            text_color=FOURTH_CLR
        ).pack(fill="x", pady=10)

        # -submit button
        CTkButton(
            self,
            text="Submit",
            fg_color=SECONDARY_CLR,
            hover_color=THIRD_CLR,
            text_color=FOURTH_CLR,
            font=BUTTON_FONT,
            width=100,
            command=self.submit,
        ).pack(side="bottom", pady=(10, 20))

    def submit(self):
        self.grab_release()
        self.destroy()


class Add_po_form(Top_level_form):
    def __init__(self, parent, id, pos_container):
        super().__init__(parent=parent, title="Add Purchase Order", width=500, height=600)
        
        # data
        self.init_parameters()
        self.id= id
        self.po_panels_container= pos_container

        # widgets
        # - containers left for po data and right for color data
        self.left_container= CTkFrame(self, fg_color="transparent")
        self.left_container.pack(side="left", fill="both", expand=True)
        self.right_container= CTkFrame(self, fg_color="transparent")
        self.right_container.pack(side="right", fill="both", expand=True)
        # - po widgets and color widgets
        self.create_po_widgets()
        self.create_color_widgets()

    def init_parameters(self):
        self.po_vars= {
            "po_number": StringVar(),
            "smu": StringVar(),
            "style": StringVar(),
            "size_range": StringVar(),
            "ratio": StringVar(),
            "po_qty": StringVar(),
            "cost_price": StringVar(),
            "Shipping_date": StringVar(),
        }
        
        self.color_vars= {
            "po_number": self.po_vars["po_number"],
            "team": StringVar(),
            "color_code": StringVar(),
            "piece1_color": StringVar(),
            "piece2_color": StringVar(),
            "color_qty": StringVar(),
        }

    def create_po_widgets(self):
        Entry_panel(
            parent=self.left_container,
            label_str="PO Number:",
            data_var=self.po_vars["po_number"],
            entry_width=100,
            int_bool=True,
        )
        Entry_panel(
            parent=self.left_container,
            label_str="SMU:",
            data_var=self.po_vars["smu"],
            entry_width=100,
        )
        Entry_panel(
            parent=self.left_container,
            label_str="Style:",
            data_var=self.po_vars["style"],
            entry_width=100,
        )
        Combobox_panel(
            parent=self.left_container,
            label_str1="Size Range:",
            data_var1=self.po_vars["size_range"],
            options1=SIZE_SCALES_OPT,
        )
        Combobox_panel(
            parent=self.left_container,
            label_str1="Ratio:",
            data_var1=self.po_vars["ratio"],
            options1=RATIO_OPT,
        )
        Entry_panel(
            parent=self.left_container,
            label_str="PO Qty:",
            data_var=self.po_vars["po_qty"],
            int_bool=True,
            entry_width=100,
        )
        Entry_panel(
            parent=self.left_container,
            label_str="Cost Price:",
            data_var=self.po_vars["cost_price"],
            entry_width=100,
            float_bool=True,
        )
        Entry_panel(
            parent=self.left_container,
            label_str="Shipping Date:",
            data_var=self.po_vars["Shipping_date"],
            entry_width=100,
        )

    def create_color_widgets(self):
        Combobox_panel(
            parent=self.right_container,
            label_str1="Team:",
            data_var1=self.color_vars["team"],
            options1=TEAMS_OPT,
        )
        Entry_panel(
            parent=self.right_container,
            label_str="Color Code:",
            data_var=self.color_vars["color_code"],
            entry_width=100,
        )
        Entry_panel(
            parent=self.right_container,
            label_str="Piece1 Color:",
            data_var=self.color_vars["piece1_color"],
            entry_width=100,
        )
        Entry_panel(
            parent=self.right_container,
            label_str="Piece2 Color:",
            data_var=self.color_vars["piece2_color"],
            entry_width=100,
        )
        Entry_panel(
            parent=self.right_container,
            label_str="Color Qty:",
            int_bool=True,
            entry_width=100,
            data_var=self.color_vars["color_qty"],
        )

    def submit(self):
        # get data suitable for po_data_panel
        po_data= {
            "po_num": int(self.po_vars["po_number"].get()) if self.po_vars["po_number"].get() else None,
            "group_id": self.id,
            "smu": self.po_vars["smu"].get().upper(),
            "style_name": self.po_vars["style"].get().upper(),
            "size_range": self.po_vars["size_range"].get(),
            "ratio": self.po_vars["ratio"].get(),
            "po_qty": int(self.po_vars["po_qty"].get()) if self.po_vars["po_qty"].get() else 0,
            "price": float(self.po_vars["cost_price"].get()) if self.po_vars["cost_price"].get() else 0.00,
            "shipping_date": self.po_vars["Shipping_date"].get(),
        }
        color_data= {
            "po_num": po_data["po_num"],
            "teams": [self.color_vars["team"].get().upper()],
            "color_codes": [self.color_vars["color_code"].get().upper()],
            "piece1_colors": [self.color_vars["piece1_color"].get().upper()],
            "piece2_colors": [self.color_vars["piece2_color"].get().upper()],
            "color_qtys": [int(self.color_vars["color_qty"].get())] if self.color_vars["color_qty"].get() else [0],
        }
        # merge data to create po_data_panel
        merged_data = {**po_data, **color_data}
        # create po_data_panel and add to po_panels_container
        Po_data_panel(
            parent=self.po_panels_container,
            data=merged_data,
        )

        # convert color_data dict to suitable format for database(cancels the lists)
        color_data={
            key: value[0] if isinstance(value, list) else value for key, value in color_data.items()
        }

        # add to database
        DB_ADD_PO(po_data, color_data)
        # print(color_data)

        # close window
        super().submit()

# class Add_color_form(Top_level_form):
#     def __init__(self, parent, id):
#         super().__init__(parent=parent, title="Add Color", id=id, width=300, height=400)