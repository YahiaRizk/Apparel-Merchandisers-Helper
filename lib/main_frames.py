from customtkinter import StringVar, CTkFrame, CTkLabel
from CTkMessagebox import CTkMessagebox
from lib.panels import Path_panel, Add_path_panel, Submit_panel, Buttons_panel
from lib.category_panels import Main_info_panel, Fabric_panel
from lib.style_top_level import View_style_top_level
from lib.table_panel import Table_panel
from lib.database_funcs import (
    DB_GET_PATHS_DATA,
    DB_INSERT_PATH,
    DB_SAVE_MAIN_INFO,
    DB_GET_PATH,
    DB_GET_TOP_LEVEL_DATA,
    DB_DELETE_STYLE,
)
from settings import *
import os


class Main_frame(CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=MAIN_CLR, corner_radius=5)
        self.grid(column=1, row=1, sticky="nsew")


class Paths_frame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # get paths data from database
        self.data = DB_GET_PATHS_DATA()

        # intialize parameters
        self.init_parameters()

        # widgets
        # the main container
        self.container = CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # - paths panels
        for key, value in self.paths_vars.items():
            Path_panel(
                parent=self.container,
                label_str=f"{key} :",
                label_width=50,
                data_var=value,
                customer=key,
            )

        # the add_path_panel
        # - string var to pass to add_path_panel
        self.add_path_var = StringVar()
        # - create the add path panel
        Add_path_panel(parent=self, entry_var=self.add_path_var, func=self.add_path)

    def init_parameters(self):
        # create dict contains string vars for every coustomer in database to use with entry
        self.paths_vars = {customer: StringVar(value=path) for customer, path in self.data.items()}

    def add_path(self):
        # get the customer name from the entry var
        customer = self.add_path_var.get()
        # add the customer to database and check if it added
        if DB_INSERT_PATH(customer):
            # append the customer in to self.paths_vars dict
            self.paths_vars[customer] = StringVar()

            # create a path panel for the new customer
            Path_panel(
                parent=self.container,
                label_str=f"{customer} :",
                label_width=50,
                data_var=self.paths_vars[customer],
                customer=customer,
            )


class Create_style_frame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # Data
        self.init_parameters()
        self.main_data_vars["garment_type"].trace_add("write", self.handle_type_var)

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
            parent=left_frame,
            label_text="Main information",
            data_vars=self.main_data_vars,
        )
        self.fabric_panel = Fabric_panel(
            parent=right_frame,
            label_text="  Fabrics",
            data_vars=self.fabric_data_vars,
            scrollable=True,
        )

        # -Submit panel
        Submit_panel(
            parent=self,
            submit_func=self.submit,
            reset_func=self.reset,
        )

    def init_parameters(self):
        # main data vars to get the values from widgets
        self.main_data_vars = {
            "group_name": StringVar(),
            "customer": StringVar(value=CUSTOMER_OPT[0]),
            "brand_team": StringVar(value=BRAND_TEAM_OPT[0]),
            "garment_type": StringVar(value=TYPE_OPT[0]),
            "piece1_type": StringVar(value=PIECE_OPT[0]),
            "piece2_type": StringVar(value=PIECE_OPT[0]),
            "total_qty": StringVar(),
            "rcvd_date": StringVar(),
        }

        # empty list to append fabrics data from fabric panel
        self.fabric_data_vars = []

    def submit(self):
        # get the data from the form
        data = self.get_data()

        # Save the date to the database
        DB_SAVE_MAIN_INFO(data)

        # get the needed data for make_folders_files
        main_data = data[0]  # dict
        style_name = main_data["group_name"] if main_data["group_name"] else "Temp"
        customer = main_data["customer"]
        path = DB_GET_PATH(customer)

        # make the folder and files
        self.make_folders_files(path, style_name)

    def reset(self):
        self.master.create_style()

    def handle_type_var(self, *arg):
        # if garment type is piece
        if self.main_data_vars["garment_type"].get() == TYPE_OPT[2]:
            # pack forget the second combobox for piece 2 type
            self.main_info_panel.piece_type.unpack_sec_combobox()
        else:
            # repack second combobox for piece 2
            self.main_info_panel.piece_type.repack_sec_combobox()

    def get_data(self):
        # manage the data to send to the database
        main_data = {
            "group_name": self.main_data_vars["group_name"].get().upper(),
            "customer": self.main_data_vars["customer"].get(),
            "brand_team": self.main_data_vars["brand_team"].get(),
            "garment_type": self.main_data_vars["garment_type"].get(),
            "piece1_type": self.main_data_vars["piece1_type"].get(),
            "piece2_type": self.main_data_vars["piece2_type"].get(),
            "total_qty": (
                int(self.main_data_vars["total_qty"].get())
                if self.main_data_vars["total_qty"].get() != ""
                else 0
            ),
            "rcvd_date": self.main_data_vars["rcvd_date"].get(),
        }

        fabric_data = []
        for obj in self.fabric_data_vars:
            fabric_item = {
                "fabric_type": obj["fabric_type"].get(),
                "fabric_description": obj["fabric_description"].get(),
                "fabric_gsm": obj["fabric_gsm"].get(),
            }
            fabric_data.append(fabric_item)

        return main_data, fabric_data

    def make_folders_files(self, path, style_name):
        # Define Folders and Files names
        folders = ["Fabric", "ACC", "PO", "TP", "ART", "Pattern", "Specs", "Production"]
        files = ["QTY", "Recap", "Samples FollowUp"]

        # Make style main folder if not exist
        try:
            os.mkdir(rf"{path}\{style_name}")
        except FileExistsError:
            print("Folder already Exist.")

        # Loop on folders names and make the subfolders
        for folder in folders:
            try:
                os.mkdir(rf"{path}\{style_name}\{folder}")
            except FileExistsError:
                print("Folder already Exist.")

        # Loop on files names and create files in style main folder
        for file in files:
            filePath = rf"{path}\{style_name}\{file} {style_name}.xlsx"
            if not os.path.exists(filePath):
                open(filePath, "a").close()


class View_styles_frame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent=parent)

        #  Widget
        self.buttons_panel = Buttons_panel(
            parent=self,
            view_func=self.view_style,
            delete_func=self.delete_style,
            archive_func=self.archive_style,
        )

        self.table_panel = Table_panel(parent=self, view_style_func=self.view_style)

    def view_style(self):
        if self.table_panel.table.get_selected_row()["row_index"] != None:
            # get the style name for selected row
            style = self.table_panel.table.get_selected_row()["values"][1]
            id = self.table_panel.table.get_selected_row()["values"][0]
            # get the main data and pos data for selected row from database
            main_data, pos_data = DB_GET_TOP_LEVEL_DATA(id)

            # create the top level to view style details
            self.view_style_top_level = View_style_top_level(main_data=main_data, pos_data=pos_data)

    def delete_style(self):
        # The following appraoch when delete_row method give error
        # if row is selected
        if self.table_panel.table.get_selected_row()["row_index"] != None:
            # get the style name for selected row
            style = self.table_panel.table.get_selected_row()["values"][1]
            # get the id for selected row
            id = self.table_panel.table.get_selected_row()["values"][0]

            # give confirm message before delete
            msg = CTkMessagebox(
                title="Warning!",
                message=f"Style '{style}' will be deleted permanently,\nAre you sure ?",
                wraplength=400,
                option_1="Yes",
                option_2="No",
                icon="warning",
                text_color=FOURTH_CLR,
                fg_color=MAIN_CLR,
                bg_color=BLACK_CLR,
                button_color=(SECONDARY_CLR, SECONDARY_CLR),
                button_hover_color=THIRD_CLR,
                button_text_color=FOURTH_CLR,
                title_color=FOURTH_CLR,
                cancel_button_color=FOURTH_CLR,
                justify="center",
            )

            # Check if the user approved delete
            if msg.get() == "Yes":
                # delete row from database
                DB_DELETE_STYLE(id)

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
            font=APP_TITLE_FONT,
        ).pack(expand=True)

class Dummy_info_frame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # Widget
        CTkLabel(
            master=self,
            text="Dummy info",
            text_color=FOURTH_CLR,
            font=APP_TITLE_FONT,
        ).pack(expand=True)
