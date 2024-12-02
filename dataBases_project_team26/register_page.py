import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
# from register_alergies import AllergiesWindow
from PIL import Image
import sqlite3
from datetime import datetime
import tkinter.font as tkFont

class RegisterFrame(tk.Frame):
    def __init__(self,master=None,**kwargs):
        super().__init__(master,bg='#D2E9E9',**kwargs)
        self.master=master
        ws = self.master.winfo_screenwidth() # width of the screen
        hs = self.master.winfo_screenheight() # height of the screen
        w= 660
        h = 600
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.pack(side='left')
        self.create_content()
        self.path=""
        
    
    def create_content(self):
        #labels
        helv36 = tkFont.Font(family="Helvetica",size=15,weight="bold")
        register_label=tk.Label(self, text="Hello, create your account",bg='#D2E9E9',fg='black',font=helv36)
        upEAT_label=tk.Label(self,text='upEAT',bg='#D2E9E9',fg='black',font=('Helvetica', 18, 'bold'))
        #username+password
        username_label=tk.Label(self, text="*Username",bg='#D2E9E9',fg='black',font=30)
        username_entry=tk.Entry(self)
        password_label=tk.Label(self, text="*Password",bg='#D2E9E9',fg='black',font=30)
        password_entry=tk.Entry(self,show="*")
        pass_valid_entry=tk.Entry(self,show="*")
        pass_valid_entry_label=tk.Label(self, text="*Confirm Password",bg='#D2E9E9',fg='black',font=30)
        #onoma
        name_entry=tk.Entry(self)
        name_label=tk.Label(self,text="*Όνομα",bg='#D2E9E9',fg='black',font=30)
        
        surr_entry=tk.Entry(self)
        surr_label=tk.Label(self,text="*Επώνυμο",bg='#D2E9E9',fg='black',font=30)
        #ssn
        self.ssn_entry=tk.Entry(self)
        ssn_label=tk.Label(self, text="*ΑΜΚΑ",bg='#D2E9E9',fg='black',font=30)
        #AM and semester
        am_entry=tk.Entry(self)
        am_label=tk.Label(self, text="*Student Number",bg='#D2E9E9',fg='black',font=30)
        semester_entry=tk.Entry(self)
        semester_label=tk.Label(self, text="Semester",bg='#D2E9E9',fg='black',font=30)
        #phone num
        phone_entry=tk.Entry(self)
        phone_label=tk.Label(self, text="Phone",bg='#D2E9E9',fg='black',font=30)
        #address
        address_entry=tk.Entry(self)
        address_label=tk.Label(self, text="Address",bg='#D2E9E9',fg='black',font=30)
        
        
        #dep.name droplist
        conn=sqlite3.connect("upEAT_1.sqlite")
        curr=conn.execute("SELECT dptname\
                          FROM DEPARTMENT")
        data=curr.fetchall()
        departments=[]
        for i in range(len(data)-1):
            departments.append(data[i][0])
        
        conn.close()
        
        departm_entry=ttk.Combobox(self,width=17,values=departments,state='readonly')
        departm_label=tk.Label(self, text="Department",bg='#D2E9E9',fg='black',font=30)

      
        
        #already a member login
        login_btn=tk.Button(self,text="LOGIN",command=lambda: self.login(),font=('Helvetica', 13, 'bold'))

        login_lbl=tk.Label(self,text="Im already a member..",bg='#D2E9E9',fg='black',font=('Helvetica', 13, 'bold'))
        # #register button
        create_btn=tk.Button(self,text="Create"\
            ,font=('Helvetica', 13, 'bold'),command=lambda: self.createBtn(username_entry,password_entry,pass_valid_entry,self.ssn_entry,name_entry,surr_entry,phone_entry,am_entry,address_entry,departm_entry,semester_entry))

        var=tk.IntVar()
        show_pass=tk.Checkbutton(self,text="Show Password",variable=var,onvalue=1,offvalue=0,bg='#D2E9E9',fg='black',font=('Helvetica', 13, 'bold'),command=lambda: self.showpassword(var.get(),password_entry,pass_valid_entry))
        upEAT_label.grid(row=0,column=0,columnspan=2,sticky="news",pady=30)

        name_label.grid(row=2,column=0,padx=5)
        name_entry.grid(row=2,column=1,pady=10)

        surr_label.grid(row=3,column=0,padx=5)
        surr_entry.grid(row=3,column=1,pady=10)

        register_label.grid(row=1,column=0,columnspan=2,sticky="news",pady=10)
        username_label.grid(row=4,column=0,padx=5)
        username_entry.grid(row=4,column=1,pady=10)
        password_label.grid(row=5,column=0,padx=5)
        password_entry.grid(row=5,column=1,pady=10)
        pass_valid_entry.grid(row=6,column=1,pady=10)
        pass_valid_entry_label.grid(row=6,column=0,padx=5)
        show_pass.grid(row=7,column=1,padx=5)

        self.ssn_entry.grid(row=2,column=3,pady=10)
        ssn_label.grid(row=2,column=2,padx=5)
        
        am_entry.grid(row=3,column=3,pady=10)
        am_label.grid(row=3,column=2,padx=5)
        semester_entry.grid(row=4,column=3,pady=10)
        semester_label.grid(row=4,column=2,padx=5)
        address_entry.grid(row=5,column=3,pady=10)
        address_label.grid(row=5,column=2,padx=5)
        departm_entry.grid(row=7,column=3,pady=10)
        departm_label.grid(row=7,column=2,padx=5)
        create_btn.grid(row=8,column=0,columnspan=2,pady=20)
        login_btn.grid(row=9,column=1,pady=20)
        login_lbl.grid(row=9,column=0,padx=5)

        phone_label.grid(row=6,column=2,padx=5)
        phone_entry.grid(row=6,column=3,pady=10)


        uploadphoto=tk.Label(self, text="Profile Picture",bg='#D2E9E9',fg='black',font=('Helvetica', 13, 'bold'))
        uploadBtn=tk.Button(self,text="Upload Photo",font=('Helvetica', 13, 'bold'),command=lambda: self.uploadBtn(username_entry.get(),am_entry.get()))
        uploadBtn.grid(row=14,column=1,pady=10)
        uploadphoto.grid(row=14,column=0,padx=5)
        


    # def allergiesBtn(self,ssn):
    #     alerg_win=AllergiesWindow(ssn)
    
    def uploadBtn(self,username,am_entry):
        if username=="":
            messagebox.showerror("Photo Not Uploaded","You need to select a username first")
            return 
        
        file_path=filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
   
        if file_path:
                # Load the selected image
            original_image = Image.open(file_path)

            # Convert the image to RGB mode if it has an alpha channel
            if original_image.mode == 'RGBA':
                image = original_image.convert('RGB')
            else:
                image = original_image

            save_path="./profpic/"+am_entry+".jpg"
            image.save(save_path)
            self.path=save_path
         


    def createBtn(self,username_entry,password_entry,pass_valid_entry,ssn_entry,name_entry,surr_entry,phone_entry,am_entry,address_entry,departm_entry,semester_entry):
    
        if(username_entry.get()=="" or password_entry.get()=="" or pass_valid_entry.get()=="" or name_entry.get()=="" or surr_entry.get()=="" or ssn_entry.get()=="" or am_entry.get()==""):
            messagebox.showerror("Account not created","Please fill all fields marked with *")
            return 0

        
        if(self.path==""):
            pic_path=None
        else:
            pic_path=self.path
       
        
        
        if(address_entry.get()==""):
            address_entry_value=None
        else:
            address_entry_value=address_entry.get()

        if(semester_entry.get()==""):
            semester_entry_value=None
        else:
            semester_entry_value=semester_entry.get()
        
        if(phone_entry.get()==""):
            phone_entry_value=None
        else:
           phone_entry_value=phone_entry.get()
        
        if(departm_entry.get()==""):
            departm_entry_value=None
        else:
            departm_entry_value=departm_entry.get()

        if(not ssn_entry.get().isdigit() or len(ssn_entry.get())!=11):
            messagebox.showerror("Couldnt Create Account","Invalid SSN Number")
            return
        
        if(not am_entry.get().isdigit() or len(am_entry.get())!=7):
            messagebox.showerror("Couldnt Create Account","Invalid StudentID Number")
            return
        
        if(semester_entry.get()!=""):
            if(not semester_entry.get().isdigit()):
                messagebox.showerror("Error", "Invalid Semester")
                return
        if(phone_entry.get()!=""):
            if(not len(phone_entry.get())==10):
                messagebox.showerror("Error", "Invalid Phone Number")
                return
            
        self.conn=sqlite3.connect('upEAT_1.sqlite')
        curr=self.conn.execute("SELECT SSN FROM MEMBER")
        ssns=curr.fetchall()
        for i in range(len(ssns)-1):
            if(ssns[i][0]==ssn_entry.get()):
                messagebox.showerror("Couldnt Create Account","There is already a user with this SSN")
                return

        curr=self.conn.execute("SELECT username FROM ACCOUNT")
        names=curr.fetchall()
        for i in range(len(names)-1):
                if (names[i][0]==username_entry.get()):
                    messagebox.showerror("Username Not Valid","This username is taken, select another")
                    return
        
        curr=self.conn.execute("SELECT studentIDno FROM STUDENT")
        studids=curr.fetchall()
        for i in range(len(studids)-1):
            if(studids[i][0]==int(am_entry.get())):
                messagebox.showerror("Couldnt Create Account","There is already a user with this studentID number")
                return
        
        barcode=ssn_entry.get()+am_entry.get()

        if(password_entry.get()==pass_valid_entry.get()):
            self.conn.execute("INSERT INTO MEMBER (SSN,firstname,lastname,phoneno,picture,address) VALUES (?,?,?,?,?,?);"\
                ,(ssn_entry.get(),name_entry.get(),surr_entry.get(),phone_entry_value,pic_path,address_entry_value))
            self.conn.execute("INSERT INTO ACCOUNT (username,password,barcode,datecreated,SSN) VALUES (?,?,?,?,?);"\
                ,(username_entry.get(),password_entry.get(),barcode,datetime.now().date(),ssn_entry.get()))
            self.conn.execute("INSERT INTO STUDENT (studentIDno,SSN,semester,dptname) VALUES (?,?,?,?);"\
                ,(am_entry.get(),ssn_entry.get(),semester_entry_value,departm_entry_value))
            self.conn.commit()
            self.conn.close()
            messagebox.showinfo("Account Created","Great,your upEAT account has been created")
            return
        else:
            messagebox.showerror("Warning","Passwords do NOT match")
            return
       
        
        
     
  
    

    
    def login(self):
        from login_page import LoginFrame
        self.destroy()
        # allergen_frame.destroy()
        login_frame=LoginFrame(self.master)
        login_frame.pack()

    def showpassword(self,state,password_entry,pass_valid_entry):
        if state==0:
            password_entry.configure(show="*")
            pass_valid_entry.configure(show="*")
        else:
            password_entry.configure(show="")
            pass_valid_entry.configure(show="")

