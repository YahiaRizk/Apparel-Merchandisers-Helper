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
        Entry_panel(self.data_frame, "Style# :", data_vars["style"])
        Entry_panel(self.data_frame, "PO# :", data_vars["po"])
        Entry_panel(self.data_frame, "PO QTY :", data_vars["po_qty"], int_bool= True)
        Combobox_panel(self.data_frame, "Brand :", BRAND_OPT, data_vars["brand"])
        Combobox_panel(self.data_frame, "Type :", TYPE_OPT, data_vars["type"])
        self.piece_type = Combobox_panel(
            parent=self.data_frame,
            label_str1="Piece 1 :",
            options1=PIECE_OPT,
            data_var1=data_vars["piece1_type"],
            label_str2="Piece 2 :",
            options2=PIECE_OPT,
            data_var2=data_vars["piece2_type"],
        )
        Entry_panel(self.data_frame, "Date RCVD :", data_vars["date_rcvd"])


class Size_panel(Category_panel):
    def __init__(self, parent, label_text, data_vars, scrollable=False):
        super().__init__(parent=parent, label_text=label_text, scrollable=scrollable)

        # Widgets
        CTkWindowSeparator(self.data_frame, length=120, color=SECONDARY_CLR).pack(pady=10)
        Combobox_panel(
            self.data_frame,
            "Size Scale",
            SIZE_SCALES_OPT,
            data_vars["size_scale"],
            width=100,
        )
        Combobox_panel(self.data_frame, "Size_Ratio", RATIO_OPT, data_vars["ratio"], width=100)


class Fabric_color_panel(Category_panel):
    # -list containes all created color related to class itself
    color1_list = []
    color2_list = []

    def __init__(self, parent, label_text, data_vars, scrollable=False):
        super().__init__(parent=parent, label_text=label_text, scrollable=scrollable)
        self.pack_configure(padx=0)

        # data
        self.data_vars = data_vars

        # Widgets
        self.fabric1 = Combobox_panel(
            self.data_frame,
            "T-Shirt Fabric :",
            FABRICS_OPT,
            data_vars["piece1_fabric"],
            width=200,
        )
        self.gsm1 = Combobox_panel(self.data_frame, "T-Shirt GSM :", GSM_OPT, data_vars["piece1_gsm"])
        self.fabric2 = Combobox_panel(
            self.data_frame,
            "T-Shirt2 Fabric :",
            FABRICS_OPT,
            data_vars["piece2_fabric"],
            width=200,
        )
        self.gsm2 = Combobox_panel(
            self.data_frame, "T-Shirt2 GSM :", GSM_OPT, data_vars["piece2_gsm"]
        )
        self.create_color()

    def create_color(self):
        # Remove add color button if exist
        if hasattr(self, "add_color_button"):
            self.add_color_button.pack_forget()

        # Create the data vars to pass to the widget
        color_vars = {
            "color_code": StringVar(),
            "color_qty": StringVar(),
            "piece1_color": StringVar(),
            "piece2_color": StringVar(),
        }

        # Create the colors widgets
        self.color_code = Entry_panel(self.data_frame, "Color Code :", color_vars["color_code"])
        self.color_qty = Entry_panel(self.data_frame, "Color QTY :", color_vars["color_qty"], int_bool= True)
        self.color1 = Entry_panel(
            self.data_frame,
            f'{self.data_vars['piece1_type'].get()} Color :',
            color_vars["piece1_color"],
            entry_width=100,
        )
        self.color2 = Entry_panel(
            self.data_frame,
            f'{self.data_vars['piece2_type'].get()}2 Color :',
            color_vars["piece2_color"],
            entry_width=100,
        )

        # add the created colors to the lists ability to acces them and modify its lables
        Fabric_color_panel.color1_list.append(self.color1)
        Fabric_color_panel.color2_list.append(self.color2)

        # Append the colors vars to the create_style_vars['colors']
        self.data_vars["colors"].append(color_vars)

        # Make a separator to separate colors
        CTkWindowSeparator(self.data_frame, length=120, color=SECONDARY_CLR).pack(pady=10)

        # create a button to add color
        self.add_color_button = CTkButton(
            self.data_frame,
            text="Add Color",
            font=(FONT_FAMILY, FONT_SIZE),
            text_color=FOURTH_CLR,
            fg_color=SECONDARY_CLR,
            hover_color=THIRD_CLR,
            command=self.create_color,
        )
        self.add_color_button.pack(pady=(0, 5))
