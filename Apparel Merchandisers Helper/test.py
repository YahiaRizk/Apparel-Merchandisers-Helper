from customtkinter import *

app = CTk()
app.geometry('500x500')

frame = CTkScrollableFrame(app)
frame.pack(expand= True, fill= 'both')

for i in range(30):
    CTkLabel(frame).pack(fill= 'x', pady= 10)

app.mainloop()