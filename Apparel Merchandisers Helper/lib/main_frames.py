from CTkMessagebox import CTkMessagebox
from lib.category_panels import *
from lib.style_top_level import View_style_top_level
from settings import *
from lib.database_funcs import *
from lib.table_panel import *
import json


class Main_frame(CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=MAIN_CLR, corner_radius=5)
        self.grid(column=1, row=1, sticky="nsew")


class Create_style_frame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # Data
        self.init_parameters()
        self.data_vars["type"].trace_add("write", self.handle_type_var)
        self.data_vars["size_scale"].trace_add("write", self.change_ratio)
        self.data_vars["piece1_type"].trace_add("write", self.handle_piece_type_var)
        self.data_vars["piece2_type"].trace_add("write", self.handle_piece_type_var)

        # Database
        # CREATE_DATABASE(self.get_data())

        # grid layot
        self.columnconfigure((0, 1), weight=4, uniform="a")
        self.rowconfigure(0, weight=8, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")

        # Widgets
        # -Two main frames
        left_frame = CTkFrame(self, fg_color="transparent")
        left_frame.grid(column=0, row=0, sticky="nsew", padx=(10, 0), pady=(5, 0))
        right_frame = CTkFrame(self, fg_color="transparent")
        right_frame.grid(column=1, row=0, sticky="nsew", padx=0, pady=(5, 0))

        # --pack category panels to the frames
        self.main_info_panel = Main_info_panel(
            left_frame, "Main information", data_vars=self.data_vars
        )
        self.Size_panel = Size_panel(
            left_frame, "Sizes & PPK", data_vars=self.data_vars
        )
        self.fabric_color_panel = Fabric_color_panel(
            right_frame, "Fabrics and Colors", data_vars=self.data_vars, scrollable=True
        )

        # -Submit panel
        Submit_panel(self, lambda: SAVE_TO_DATABASE(self.get_data()), self.reset)

    def init_parameters(self):

        self.data_vars = {
            "style": StringVar(),
            "po": StringVar(),
            "po_qty": StringVar(),
            "brand": StringVar(value=BRAND_OPT[0]),
            "type": StringVar(value=TYPE_OPT[0]),
            "piece1_type": StringVar(value=PIECE_OPT[0]),
            "piece2_type": StringVar(value=PIECE_OPT[0]),
            "date_rcvd": StringVar(),
            "size_scale": StringVar(value=SIZE_SCALES_OPT[3]),
            "ratio": StringVar(value=RATIO_OPT[0]),
            "piece1_fabric": StringVar(),
            "piece2_fabric": StringVar(),
            "piece1_gsm": StringVar(),
            "piece2_gsm": StringVar(),
            "colors": [],
        }

    def reset(self):
        self.master.create_style()
        # self.data_vars["style"].set("")
        # self.data_vars["po"].set("")
        # self.data_vars["po_qty"].set("")
        # self.data_vars["brand"].set(value=BRAND_OPT[0])
        # self.data_vars["type"].set(value=TYPE_OPT[0])
        # self.data_vars["piece1_type"].set(value=PIECE_OPT[0])
        # self.data_vars["piece2_type"].set(value=PIECE_OPT[0])
        # self.data_vars["date_rcvd"].set("")
        # self.data_vars["size_scale"].set(value=SIZE_SCALES_OPT[3])
        # self.data_vars["ratio"].set(value=RATIO_OPT[0])
        # self.data_vars["piece1_fabric"].set("")
        # self.data_vars["piece2_fabric"].set("")
        # self.data_vars["piece1_gsm"].set("")
        # self.data_vars["piece2_gsm"].set("")

        # # loop on colors dictionary to clear its values
        # for dict in self.data_vars["colors"]:
        #     for value in dict.values():
        #         value.set("")

        # self.data_vars["colors"].clear()

        # for color in Fabric_color_panel.color1_list:
        #     color.unpack()

    def handle_type_var(self, *arg):
        if self.data_vars["type"].get() == TYPE_OPT[2]:  # if garment type is piece
            # pack forget the second combobox for piece 2 type
            self.main_info_panel.piece_type.unpack_sec_combobox()

            # pack forget second fabric type, gsm and color
            self.fabric_color_panel.fabric2.unpack()
            self.fabric_color_panel.gsm2.unpack()
            # loop on all colors for second pieces to remove them
            for color_entry in Fabric_color_panel.color2_list:
                color_entry.unpack()
        else:
            # repack second combobox for piece 2
            self.main_info_panel.piece_type.repack_sec_combobox()

            # repack second fabric type and color
            self.fabric_color_panel.fabric2.repack()
            self.fabric_color_panel.gsm2.repack()
            # loop on colors to repack the second piece
            for color_entry in Fabric_color_panel.color2_list:
                color_entry.repack()

    def handle_piece_type_var(self, *args):
        # Change labels for piece 1
        piece1_type = self.data_vars["piece1_type"].get()
        self.fabric_color_panel.fabric1.change_label(f"{piece1_type} Fabric :")
        self.fabric_color_panel.gsm1.change_label(f"{piece1_type} GSM :")
        # -loop on all color panels and change its label
        for color_entry in Fabric_color_panel.color1_list:
            color_entry.change_label(f"{piece1_type} Color :")

        # Change labels for piece 2
        piece2_type = self.data_vars["piece2_type"].get()
        self.fabric_color_panel.fabric2.change_label(f"{piece2_type}2 Fabric :")
        self.fabric_color_panel.gsm2.change_label(f"{piece2_type}2 GSM :")
        # -loop on all color panels and change its label
        for color_entry in Fabric_color_panel.color2_list:
            color_entry.change_label(f"{piece2_type} Color :")

    def change_ratio(self, *args):
        if self.data_vars["size_scale"].get() in ("8-20", "S-XL"):
            self.data_vars["ratio"].set(RATIO_OPT[1])
        else:
            self.data_vars["ratio"].set(RATIO_OPT[0])

    def get_data(self):
        # New approach
        # create colors list from data_vars['colors']
        colors_list = []
        for dict in self.data_vars["colors"]:
            color_info = {}
            for key, value in dict.items():
                if key == "color_qty":
                    color_info[key] = int(value.get()) if value.get() != "" else 0
                else:
                    color_info[key] = value.get()

            colors_list.append(color_info)

        data = {
            "style": self.data_vars["style"].get().upper(),
            "po": self.data_vars["po"].get(),
            "po_qty": (
                int(self.data_vars["po_qty"].get())
                if self.data_vars["po_qty"].get() != ""
                else 0
            ),
            "brand": self.data_vars["brand"].get(),
            "type": self.data_vars["type"].get(),
            "piece1_type": self.data_vars["piece1_type"].get(),
            "piece2_type": self.data_vars["piece2_type"].get(),
            "date_rcvd": self.data_vars["date_rcvd"].get(),
            "size_scale": self.data_vars["size_scale"].get(),
            "ratio": self.data_vars["ratio"].get(),
            "piece1_fabric": self.data_vars["piece1_fabric"].get(),
            "piece2_fabric": self.data_vars["piece2_fabric"].get(),
            "piece1_gsm": (
                int(self.data_vars["piece1_gsm"].get())
                if self.data_vars["piece1_gsm"].get() != ""
                else 0
            ),
            "piece2_gsm": (
                int(self.data_vars["piece2_gsm"].get())
                if self.data_vars["piece2_gsm"].get() != ""
                else 0
            ),
            "colors": json.dumps(colors_list),
        }
        # Old approach with loop will replace with new that will manipulate the inserted data
        # data = {}
        # Loop on data_vars dictionary and transfer all ctk vars to string values
        # and qty vars to int values and assign them to data object
        # for key, value in self.data_vars.items():
        # if key == 'colors':
        #     data['colors'] = []
        # elif key == 'po_qty':
        #     data[key] = int(value.get()) if value.get() != '' else 0
        # else:
        #     data[key] = value.get()

        # for dict in self.data_vars['colors']:
        # color_info = {}

        # for key, value in dict.items():
        #     if key == 'color_qty':
        #         color_info[key] = int(value.get()) if value.get() != '' else 0
        #     else:
        #         color_info[key] = value.get()

        # data['colors'].append(color_info)

        return data


class View_styles_frame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent=parent)

        #  Widget
        self.buttons_panel = Buttons_panel(self, self.view_style, self.delete_style, self.archive_style)
        self.table_panel = Table_panel(self, self.view_style)

    def view_style(self):
        if self.table_panel.table.get_selected_row()["row_index"] != None:
            # get the style name for selected row
            style = self.table_panel.table.get_selected_row()["values"][0]

            # create the top level to view style details
            self.view_style_top_level= View_style_top_level(style)

    def delete_style(self):
        # The following appraoch when delete_row method give error
        # if row is selected
        if self.table_panel.table.get_selected_row()["row_index"] != None:
            # get the style name for selected row
            style = self.table_panel.table.get_selected_row()["values"][0]

            # give confirm message before delete
            msg = CTkMessagebox(
                title="Warning!",
                message=f"Style {style} will be deleted permanently,\nAre you sure ?",
                wraplength= 400,
                option_1= 'Yes',
                option_2= 'No',
                icon= 'warning',
                text_color= FOURTH_CLR,
                fg_color= MAIN_CLR,
                bg_color= BLACK_CLR,
                button_color= SECONDARY_CLR,
                button_hover_color= THIRD_CLR,
                button_text_color= FOURTH_CLR,
                title_color= FOURTH_CLR,
                cancel_button_color= FOURTH_CLR,
                justify= 'center',
            )

            # Check if the user approved delete
            if msg.get() == 'Yes':
                # delete row from database
                DB_DELETE_STYLE(style.strip())

                # recreate the table
                self.table_panel.create_table()

    def archive_style(self):
        print("Archive")


class Pricing_frame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # Widget
        CTkLabel(
            master=self,
            text="Pricing",
            text_color=FOURTH_CLR,
            font=(FONT_FAMILY, TITLE_FONT_SIZE),
        ).pack(expand=True)


class Dummy_info_frame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # Widget
        CTkLabel(
            master=self,
            text="Dummy info",
            text_color=FOURTH_CLR,
            font=(FONT_FAMILY, TITLE_FONT_SIZE),
        ).pack(expand=True)
