from CTkTable import CTkTable
from customtkinter import CTkScrollableFrame, CTkFrame
from settings import *
from lib.database_funcs import *


class Table_panel(CTkFrame):
    def __init__(self, parent, view_style_func):
        super().__init__(
            master=parent,
            fg_color="transparent",
            border_width=1,
            border_color= FOURTH_CLR,
            
        )
        self.pack(expand=True, fill="both", padx=10, pady=10)

        #  Widget
        self.scrollable_frame = CTkScrollableFrame(
            master=self,
            scrollbar_button_color=SECONDARY_CLR,
            scrollbar_button_hover_color=THIRD_CLR,
        )
        self.scrollable_frame.pack(expand= True, fill= 'both', padx= 2, pady= 2)
        self.create_table()

        # events
        self.table.bind('<Double-Button-1>', lambda event: view_style_func())

    def create_table(self):
        # Check if the table is already created and pack_forget it
        if hasattr(self, 'table'):
            self.table.pack_forget()

        # get the data from database
        data = DB_GET_TABLE_DATA()

        # add the header row to the data
        data.insert(0, TABLE_HEADER)
        self.table = CTkTable(
            self.scrollable_frame,
            row=len(data),
            column=len(TABLE_HEADER),
            values=data,
            colors=[MAIN_CLR, SECONDARY_CLR],
            text_color=FOURTH_CLR,
            header_color=MAIN_CLR,
            hover= True,
            hover_color= THIRD_CLR,
            corner_radius=6,
            width=1,
            height=60,
            # wraplength= 100,
            command=self.handle_cell_click,
        )

        # edit the header row
        self.table.edit_row(0, font=(FONT_FAMILY, 18, "bold"))

        # pack the table in the scrollable frame
        self.table.pack(fill="x")

        self.handle_scroll()

    def handle_scroll(self):
        # update widgets from the root app to get real height
        self.master.master.update_idletasks()

        # if the table height is less than scroll frame height hide the scrollbar
        if self.table.winfo_height() <= self.scrollable_frame._parent_canvas.winfo_height():
            self.scrollable_frame._scrollbar.grid_forget()
            # self.table.pack_configure(padx=(0, 7))
        else:  # else show it
            self.scrollable_frame._scrollbar.grid(column=1)
            # self.table.pack_configure(padx=0)

    def handle_cell_click(self, event):
        # unselect all rows
        for index in range(self.table.rows):
            self.table.deselect_row(index)

        # select clicked row
        self.table.select_row(event["row"])
        # Change selected row color
        # self.table.edit_row(event['row'], fg_color= THIRD_CLR)
