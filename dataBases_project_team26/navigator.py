import tkinter as tk
class Navigator(tk.Frame):
    def __init__(self,frame,master,username,**kwargs):
        self.navigator=tk.Menu(master)
        self.frame=frame
        self.username=username
        self.cascnav=tk.Menu(self.navigator)
        self.histnav=tk.Menu(self.navigator)
        self.menunav=tk.Menu(self.navigator)
        self.helpnav=tk.Menu(self.navigator)

        self.master=master
        self.master.config(menu=self.navigator)
        self.navigator.config(background='#D2E9E9')

        self.navigator.add_cascade(label="Menu",menu=self.cascnav,background='#D2E9E9')
        self.cascnav.add_command(label="Home",command=lambda: self.homepage(self.username))
        self.cascnav.add_command(label="My Profile",command=lambda: self.myprofile(self.username))
        self.cascnav.add_command(label="Logout",command=lambda: self.logout())

        
        self.navigator.add_cascade(label="History",menu=self.histnav)
        self.histnav.add_command(label="Purchase & Review History", command=lambda: self.purchrevmenu(self.username))
        # self.histnav.add_command(label="Campus Restaurant History")

        self.navigator.add_cascade(label="Food Menu",menu=self.menunav)
        self.menunav.add_command(label="Uni Restaurant Menu",command=lambda: self.campmenu(self.username))
        self.menunav.add_command(label="Other Restaurant Menus",command=lambda: self.restaurants())
        self.menunav.add_command(label="Coffee and Snack Shops",command=lambda: self.othershops())
        
        self.navigator.add_cascade(label="Help",menu=self.helpnav)
        self.helpnav.add_command(label="Info",command=lambda: self.info())


    def destroynav(self):
        self.navigator.destroy()

    
    def logout(self):
        from login_page import LoginFrame
        self.destroynav()
        self.frame.destroy()
        login_frame=LoginFrame(self.master)
        login_frame.pack()

    def myprofile(self,username):
        from profile_page import ProfileFrame
        if hasattr(self,'myprofile_frame'):
            return
        self.frame.destroy()
        self.myprofile_frame=ProfileFrame(self.master,username=username)
        self.myprofile_frame.pack()
    
    def homepage(self,username):
        from home_page import WelcomeFrame
        if hasattr(self,'home_frame'):
            return
        self.frame.destroy()
        self.home_frame=WelcomeFrame(self.master,username=username)
        self.home_frame.pack()
        
    def campmenu(self,username):
        from schedule_page import ScheduleFrame
        self.frame.destroy()
        menuFrame=ScheduleFrame(self.master,username=self.username)
        menuFrame.pack()

    def purchrevmenu(self,username):
        from purch_rev_page import PurchRevFrame
        self.frame.destroy()
        menuFrame=PurchRevFrame(self.master,username=self.username)
        menuFrame.pack()

    def othershops(self):
        from coffeeshopmenu import CoffeShopMenuFrame
        self.frame.destroy()
        othershopFrame=CoffeShopMenuFrame(self.master,username=self.username)
        othershopFrame.pack()
        
    def restaurants(self):
        from rest_schedule import RestaurantMenuFrame
        self.frame.destroy()
        restaurantFrame=RestaurantMenuFrame(self.master,username=self.username)
        restaurantFrame.pack()

    def info(self):
        from infoframe import InfoFrame
        self.frame.destroy()
        infoFrame=InfoFrame(self.master,username=self.username)
        infoFrame.pack()