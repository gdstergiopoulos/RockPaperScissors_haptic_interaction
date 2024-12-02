import tkinter as tk
from tkinter import messagebox
from register_page import RegisterFrame
import sqlite3

class LoginFrame(tk.Frame):
    def __init__(self,master=None,**kwargs):
        super().__init__(master,bg='#D2E9E9',**kwargs)
        self.master=master
        w= 350
        h = 400
        ws = self.master.winfo_screenwidth() # width of the screen
        hs = self.master.winfo_screenheight() # height of the screen
        x = (ws/2) - (5*w/3)
        y = h/4
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.pack()
        self.create_content()

    
    def create_content(self):
        login_label=tk.Label(self, text="Login",bg='#D2E9E9',fg='black',font=30)
        upEAT_label=tk.Label(self,text='upEAT',bg='#D2E9E9',fg='black',font=30)
        username_label=tk.Label(self, text="Username",bg='#D2E9E9',fg='black',font=30)
        self.username_entry=tk.Entry(self)
        password_label=tk.Label(self, text="Password",bg='#D2E9E9',fg='black',font=30)
        self.password_entry=tk.Entry(self,show="*")
        login_btn=tk.Button(self,text="LOGIN",command=lambda: self.login(None))
        register_lbl=tk.Label(self,text="Im not a member..",bg='#D2E9E9',fg='black',font=20)
        register_btn=tk.Button(self,text="Register",command=lambda: self.registerbtn())
        var=tk.IntVar()
        show_pass=tk.Checkbutton(self,text="Show Password",variable=var,onvalue=1,offvalue=0,bg='#D2E9E9',fg='black',font=5,command=lambda: self.showpassword(var.get()),selectcolor='white')
        login_label.grid(row=1,column=0,columnspan=2,sticky="news",pady=10)
        username_label.grid(row=2,column=0,padx=5)
        self.username_entry.grid(row=2,column=1,pady=20)
        password_label.grid(row=3,column=0,padx=5)
        self.password_entry.grid(row=3,column=1,pady=20)
        login_btn.grid(row=5,column=0,columnspan=2,pady=10)
        show_pass.grid(row=4,column=0,columnspan=2)
        register_lbl.grid(row=7,column=0,pady=25)
        register_btn.grid(row=7,column=1,columnspan=2,pady=5)
        self.master.bind("<Return>",self.login)

    def login(self,event):
        #sql code here for validation
        username=self.username_entry.get()
        password=self.password_entry.get()
        self.conn=sqlite3.connect('upEAT_1.sqlite')
        self.cursor=self.conn.execute("SELECT username,password FROM ACCOUNT WHERE username=?",(username,))
        data=self.cursor.fetchall()    
        if (data==[]):
            messagebox.showerror("User Not Found", "Check your username, or create an account")

        self.conn.close()
        
        if username == data[0][0] and password == data[0][1]:
            # Destroy current frame and show welcome frame
            self.destroy()
           

            from home_page import WelcomeFrame
            welcome_frame = WelcomeFrame(self.master,username=username)
            welcome_frame.pack()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

        
        
    def registerbtn(self):
        self.destroy()
        register_frame=RegisterFrame(self.master)
        register_frame.pack()

    def showpassword(self,state):
        if state==0:
            self.password_entry.configure(show="*")
        else:
            self.password_entry.configure(show="")

            

