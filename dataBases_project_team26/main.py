import tkinter as tk 
from login_page import LoginFrame

class upEAT(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("upEAT")
        self.configure(bg='#D2E9E9')
        self.geometry("750x750")
        login_frame=LoginFrame(self)
        login_frame.pack()


app=upEAT()


app.mainloop()