import tkinter as tk
import sqlite3
from navigator import Navigator
from PIL import ImageTk, Image
import tkinter.font as tkFont

class WelcomeFrame(tk.Frame):
    def __init__(self, master,username,**kwargs):
        super().__init__(master,bg='#D2E9E9',**kwargs)
        self.navigator=Navigator(self,master,username=username)
        ws = self.master.winfo_screenwidth() # width of the screen
        hs = self.master.winfo_screenheight() # height of the screen
        w= 900
        h = 450
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.username=username
        self.pack()
        self.create_content()

    def create_content(self):
        welcome = tkFont.Font(family="Helvetica",size=30,weight="bold")
        prof = tkFont.Font(family="Helvetica",size=10,weight="bold")
        rest = tkFont.Font(family="Helvetica",size=15,weight="bold")

        self.conn=sqlite3.connect("upEAT_1.sqlite")
        self.cursor=self.conn.execute("SELECT M.firstname\
                                       FROM ACCOUNT AS A, MEMBER AS M\
                                      WHERE A.username=? AND A.SSN=M.SSN",(self.username,))
        data=self.cursor.fetchall() 
        welcomemsg="Welcome to upEAT"
        self.conn.close()
        label = tk.Label(self, text=welcomemsg, font=welcome, bg='#D2E9E9')
        
        
        prof_picture = Image.open("./media/prof.jpg")
        prof_picture = prof_picture.resize((80,80))
        prof_pic = ImageTk.PhotoImage(prof_picture)  

        prof_pic_label = tk.Label(self,image=prof_pic)
        prof_pic_label.image = prof_pic

        log_picture = Image.open("./media/logout.png")
        log_picture = log_picture.resize((50,50))
        log_pic = ImageTk.PhotoImage(log_picture)  

        log_pic_label = tk.Label(self,image=log_pic)
        log_pic_label.image = log_pic

        uni_picture = Image.open("./media/uni.jpg")
        uni_picture = uni_picture.resize((50,50))
        uni_pic = ImageTk.PhotoImage(uni_picture)  

        uni_pic_label = tk.Label(self,image=uni_pic)
        uni_pic_label.image = uni_pic

        coffee_picture = Image.open("./media/coffee.jpg")
        coffee_picture = coffee_picture.resize((50,50))
        coffee_pic = ImageTk.PhotoImage(coffee_picture)  

        coffee_pic_label = tk.Label(self,image=coffee_pic)
        coffee_pic_label.image = coffee_pic

        # rest_picture = Image.open("./media/rest.jpg")
        # rest_picture = rest_picture.resize((50,50))
        # rest_pic = ImageTk.PhotoImage(rest_picture)  

        # rest_pic_label = tk.Label(self,image=rest_pic)
        # rest_pic_label.image = rest_pic

        logout_button = tk.Button(self, text="Logout",image=log_pic,command=self.logout)
        # campus_button = tk.Button(self, text="Campus Restaurant Schedule",image=uni_pic, command=self.campmenu, width=350, height=120, compound='left', font=rest)
        # restaurant_button = tk.Button(self, text="Restaurant Options",image=rest_pic, command=self.restaurants, width=350, height=120, compound='left', font=rest)
        coffee_button = tk.Button(self, text="Start new game",image=coffee_pic, command=self.othershops, width=350, height=120, compound='left', font=rest)
        profile_button = tk.Button(self,image=prof_pic, command=self.myprofile, text=data[0][0], compound='right', padx=5, font=prof)

        # label.grid(column=1, columnspan=5,row=0, rowspan=3, pady=20, sticky='E')

        # campus_button.grid(column=0,row=3, columnspan=4, rowspan=2, padx=10, pady=10)
        # restaurant_button.grid(column=4,row=3, columnspan=4, rowspan=2, padx=10, pady=10)

        coffee_button.grid(column=0,row=5,columnspan=4, rowspan=2,padx=10)

        logout_button.grid(column=8,row=0)
        profile_button.grid(column=7,row=0, padx=20,  pady=10)

    def logout(self):
        # Destroy current frame and show login frame
        self.destroy()
        self.navigator.destroynav()
        from login_page import LoginFrame
        login_frame=LoginFrame(self.master)
        login_frame.pack()
        
    def myprofile(self):
        from profile_page import ProfileFrame
        if hasattr(self,'myprofile_frame'):
            return
        self.destroy()
        self.myprofile_frame=ProfileFrame(self.master,username=self.username)
        self.myprofile_frame.pack()
        
    def campmenu(self):
        from schedule_page import ScheduleFrame
        self.destroy()
        menuFrame=ScheduleFrame(self.master,username=self.username)
        menuFrame.pack()


    def othershops(self):
        from coffeeshopmenu import CoffeShopMenuFrame
        self.destroy()
        othershopFrame=CoffeShopMenuFrame(self.master,username=self.username)
        othershopFrame.pack()

    def restaurants(self):
        from rest_schedule import RestaurantMenuFrame
        self.destroy()
        restaurantFrame=RestaurantMenuFrame(self.master,username=self.username)
        restaurantFrame.pack()