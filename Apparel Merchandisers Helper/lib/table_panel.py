from CTkTable import CTkTable
from customtkinter import CTkScrollableFrame
from settings import *
from lib.database_funcs import *


class Table_panel(CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(
            master=parent,
            scrollbar_button_color=SECONDARY_CLR,
            scrollbar_button_hover_color=THIRD_CLR,
        )
        self.pack(expand=True, fill="both", padx=10, pady=10)

        #  Widget
        self.create_table()

    def create_table(self):
        # get the data from database
        data = DATABASE_GET_DATA()

        # Manipulate data to get 2 col in 1 col
        for index, _ in enumerate(data):
            # merge type in one entry
            data[index][5] = f"{data[index][5]}\n\n{data[index][6]}"
            data[index].pop(6)
            # merge fabric type in one entry
            data[index][9] = f"{data[index][9]}\n\n{data[index][10]}"
            data[index].pop(10)
            # merge fabric type in one entry
            data[index][10] = f"{data[index][10]}\n\n{data[index][11]}"
            data[index].pop(11)

        # add the header row to the data
        data.insert(0, TABLE_HEADER)
        self.table = CTkTable(
            self,
            row=len(data),
            column=len(TABLE_HEADER),
            values=data,
            colors=[MAIN_CLR, SECONDARY_CLR],
            text_color=FOURTH_CLR,
            header_color=MAIN_CLR,
            hover=True,
            corner_radius=6,
            width=1,
            height=60,
            # wraplength= 100,
            command=lambda event: print(event),
        )

        # edit the header row
        self.table.edit_row(0, font=(FONT_FAMILY, 18, "bold"))


        # pack the table in the scrollable frame
        self.table.pack(fill="x")

        self.handle_scroll()

    def handle_scroll(self):
        self.master.master.update_idletasks()

        # print(self.table.winfo_height())
        # print(self._parent_canvas.winfo_height())

        if self.table.winfo_height() <= self._parent_canvas.winfo_height():
            self._scrollbar.grid_forget()
            self.table.pack_configure(padx=(0, 7))

        if self.table.winfo_height() > self._parent_canvas.winfo_height():
            self._scrollbar.grid()
            self.table.pack_configure(padx=0)
            print('greater')

        

