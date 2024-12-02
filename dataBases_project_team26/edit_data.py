import tkinter as tk
from tkinter import messagebox,ttk,filedialog
from PIL import Image
from navigator import Navigator
import sqlite3
import tkinter.font as tkFont

class EditdataFrame(tk.Frame):
    def __init__(self,master,username,**kwargs):
        super().__init__(master,bg='#D2E9E9',**kwargs)
        self.master=master
        self.master.geometry("620x600")
        self.pack(side='left')
        self.username=username
        self.navigator=Navigator(self,master,username=self.username)
        self.create_content(self.username)
        self.newusername=username
        
    
    def create_content(self,username):
        #labels
        helv1 = tkFont.Font(family="Helvetica",size=20,weight="bold")
        helv2 = tkFont.Font(family="Helvetica",size=10,weight="bold")
        self.conn=sqlite3.connect("upEAT_1.sqlite")
        self.curr=self.conn.execute("SELECT M.firstname,M.lastname,M.phoneno,A.username,A.password,M.SSN,S.studentIDno,S.semester,S.dptname,M.address\
                                    FROM MEMBER AS M,ACCOUNT AS A,STUDENT AS S\
                                    WHERE A.username=? AND M.SSN=A.SSN AND A.SSN=S.SSN",(username,))
        data=self.curr.fetchall()
        self.conn.close()
        register_label=tk.Label(self, text="Edit your account",bg='#D2E9E9',fg='black',font=helv1)
        upEAT_label=tk.Label(self,text='upEAT',bg='#D2E9E9',fg='black',font=helv1)
        #username+password
        username_label=tk.Label(self, text="Username",bg='#D2E9E9',fg='black',font=helv2)
        username_entry=tk.Entry(self)
        username_entry.insert(0,data[0][3])
        oldpass_label=tk.Label(self, text="Old Password",bg='#D2E9E9',fg='black',font=helv2)
        old_pass_entry=tk.Entry(self,show="*")
        #old_pass_entry.insert(0,data[0][4])
        new_pass_label=tk.Label(self, text="New Password",bg='#D2E9E9',fg='black',font=helv2)
        new_pass_entry=tk.Entry(self,show="*")
        new_pass_valid=tk.Entry(self,show="*")
        new_pass_valid_label=tk.Label(self, text="Confirm New Password",bg='#D2E9E9',fg='black',font=helv2)
        #onoma
        name_entry=tk.Entry(self)
        name_entry.insert(0,data[0][0])
        name_label=tk.Label(self,text="Όνομα",bg='#D2E9E9',fg='black',font=helv2)
        
        surr_entry=tk.Entry(self)
        surr_entry.insert(0,data[0][1])
        surr_label=tk.Label(self,text="Επώνυμο",bg='#D2E9E9',fg='black',font=helv2)
        #ssn
        
        ssn_entry=tk.Label(self,text=str(data[0][5]),bg='#D2E9E9',fg='black',font=helv2)
        # ssn_entry.insert(0,data[0][5])
        ssn_label=tk.Label(self, text="ΑΦΜ",bg='#D2E9E9',fg='black',font=helv2)
        #AM and semester
        # am_entry=tk.Entry(self)
        am_entry=tk.Label(self, text=str(data[0][6]),bg='#D2E9E9',fg='black',font=helv2)
        # am_entry.insert(0,data[0][6])
        am_label=tk.Label(self, text="Student Number",bg='#D2E9E9',fg='black',font=helv2)
        semester_entry=tk.Entry(self)
        if(data[0][7]!=None):
            semester_entry.insert(0,data[0][7])
        semester_label=tk.Label(self, text="Semester",bg='#D2E9E9',fg='black',font=helv2)
        #phone num
        phone_entry=tk.Entry(self)
        if(data[0][2]!=None):
            phone_entry.insert(0,data[0][2])
       
        phone_label=tk.Label(self, text="Phone",bg='#D2E9E9',fg='black',font=helv2)
        #address
        
        address_entry=tk.Entry(self)
        if(data[0][9] is not None):
            address_entry.insert(0,data[0][9])

        address_label=tk.Label(self, text="Address",bg='#D2E9E9',fg='black',font=helv2)
       
        
        departments=[]
        conn=sqlite3.connect("upEAT_1.sqlite")
        curr=conn.execute("SELECT dptname\
                          FROM DEPARTMENT")
        dptdata=curr.fetchall()
        for i in range(len(dptdata)-1):
            departments.append(dptdata[i][0])
        conn.close()
        departm_entry=ttk.Combobox(self,width=17,values=departments, state='readonly')
        if(data[0][8]!=None):
            departm_entry.insert(0,data[0][8])

        departm_label=tk.Label(self, text="Department",bg='#D2E9E9',fg='black',font=helv2)
       

        
        
       
        # #register button
        save_btn=tk.Button(self,text="Save",font=helv2,command=lambda: self.saveBtn(data[0][3],username_entry.get(),old_pass_entry.get(),new_pass_valid.get(),new_pass_entry.get(),data[0][5],name_entry.get(),surr_entry.get(),phone_entry.get(),data[0][6],address_entry.get(),departm_entry.get(),semester_entry.get()))

        var=tk.IntVar()
        show_pass=tk.Checkbutton(self,text="Show Password",variable=var,onvalue=1,offvalue=0,bg='#D2E9E9',\
            fg='black',font=helv2,command=lambda: self.showpassword(var.get(),old_pass_entry,new_pass_valid,new_pass_entry))
        upEAT_label.grid(row=0,column=0,columnspan=2,sticky="news",pady=30)

        name_label.grid(row=2,column=0,padx=5)
        name_entry.grid(row=2,column=1,pady=10)

        surr_label.grid(row=3,column=0,padx=5)
        surr_entry.grid(row=3,column=1,pady=10)

        register_label.grid(row=1,column=0,columnspan=2,sticky="news",pady=10)
        username_label.grid(row=4,column=0,padx=5)
        username_entry.grid(row=4,column=1,pady=10)
        oldpass_label.grid(row=5,column=0,padx=5)
        old_pass_entry.grid(row=5,column=1,pady=10)
        new_pass_label.grid(row=6,column=0,padx=5)
        new_pass_entry.grid(row=6,column=1,pady=10)
        new_pass_valid.grid(row=7,column=1,pady=10)
        new_pass_valid_label.grid(row=7,column=0,padx=5)
        show_pass.grid(row=8,column=1,padx=5)

        ssn_entry.grid(row=2,column=3,pady=10)
        ssn_label.grid(row=2,column=2,padx=5)
        am_entry.grid(row=3,column=3,pady=10)
        am_label.grid(row=3,column=2,padx=5)
        semester_entry.grid(row=4,column=3,pady=10)
        semester_label.grid(row=4,column=2,padx=5)
        address_entry.grid(row=5,column=3,pady=10)
        address_label.grid(row=5,column=2,padx=5)
        departm_entry.grid(row=7,column=3,pady=10)
        departm_label.grid(row=7,column=2,padx=5)
        save_btn.grid(row=10,column=1,columnspan=2,pady=20)

      

        phone_label.grid(row=6,column=2,padx=5)
        phone_entry.grid(row=6,column=3,pady=10)

        have_alerg_lbl=tk.Label(self, text="Allergies:",bg='#D2E9E9',fg='black',font=helv2)
        have_allerg_btn=tk.Button(self,text="Add Allergies",font=helv2,command=lambda: self.allergiesBtn())
        have_allerg_btn.grid(row=9,column=1,pady=10)
        have_alerg_lbl.grid(row=9,column=0,padx=5)

        uploadBtn=tk.Button(self,text="Upload Photo",command=lambda: self.uploadBtn(self.username),font=helv2)
        uploadBtn.grid(row=9,column=3,pady=10)

        uploadphoto=tk.Label(self, text="Profile Picture",bg='#D2E9E9',fg='black',font=helv2)
        uploadphoto.grid(row=9,column=2,padx=5)

        back_btn=tk.Button(self,text="Back",command=lambda: self.backBtn(),font=helv2)
        back_btn.grid(column=0,row=10)

    def saveBtn(self,acc,username_entry,oldpass,newpassvalid,newpass,ssn,name,surr,phone,am,address,departm,semester):
        self.conn=sqlite3.connect("upEAT_1.sqlite")
        self.curr=self.conn.execute("SELECT A.password,A.SSN\
                                    FROM ACCOUNT AS A\
                                    WHERE A.username=?",(acc,))
        data=self.curr.fetchall()
        password=data[0][0]
        localssn=data[0][1]


        if (oldpass!="" and newpass!="" and newpassvalid!=""):
            if (password==oldpass):
                if(newpass==newpassvalid):
                    self.conn.execute("UPDATE ACCOUNT\
                                    SET password=?\
                                    WHERE username=?",(newpass,acc,))
                    self.conn.commit()
                else:
                    messagebox.showerror("Change Password Failed", "New Passwords not match")
                    return 0
            else:
                messagebox.showerror("Change Password Failed", "Old Password Not Correct")
                return 0
        
        if(address==""):
            address=None
        
        if(semester!="" and not semester.isdigit()):
            messagebox.showerror("Error", "Invalid Semester")
            return
        
        if(semester==""):
            semester=None

        if(phone!="" and not len(phone)==10):
            messagebox.showerror("Error", "Invalid Phone Number")
            return
        
        if(phone==""):
            phone=None

        
        if(departm==""):
            departm=None
        
        self.conn.execute("UPDATE MEMBER\
                          SET SSN=?,firstname=?,lastname=?,phoneno=?,address=?\
                          WHERE SSN=?",(ssn,name,surr,phone,address,localssn,))

        self.conn.commit()

        self.conn.execute("UPDATE STUDENT\
                          SET studentIDno=?,semester=?,dptname=?\
                          WHERE SSN=?",(am,semester,departm,localssn,))
        self.conn.commit()

        curr=self.conn.execute("SELECT username\
                          FROM ACCOUNT")
        names=curr.fetchall()
        if(self.username!=username_entry):
            for i in range(len(names)-1):
                if (names[i][0]==username_entry):
                    messagebox.showerror("Cannot Change Username","This username is taken, select another")
                    return
            
            self.conn.execute("UPDATE ACCOUNT\
                            SET username=?\
                            WHERE SSN=?",(username_entry,localssn,))
            self.newusername=username_entry
            self.conn.commit()
    
        self.curr=self.conn.execute("SELECT M.firstname,M.lastname,M.phoneno,A.username,A.password,M.SSN,S.studentIDno,S.semester,S.dptname\
                                    FROM MEMBER AS M,ACCOUNT AS A,STUDENT AS S\
                                    WHERE A.username=? AND M.SSN=A.SSN AND A.SSN=S.SSN",(username_entry,))
        updated_data=self.curr.fetchall()
        self.conn.close()
        messagebox.showinfo("Info Changed","Your info changed successfully")

    def showpassword(self,state,oldpass,newpassvalid,newpass):
        if state==0:
            oldpass.configure(show="*")
            newpassvalid.configure(show="*")
            newpass.configure(show="*")
        else:
            oldpass.configure(show="")
            newpassvalid.configure(show="")
            newpass.configure(show="")
        
    def backBtn(self):
        self.destroy()
        self.navigator.destroynav()
        from profile_page import ProfileFrame
        profFrame=ProfileFrame(self.master,username=self.newusername)
        profFrame.pack()
            
    def uploadBtn(self,username):
        file_path=filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        self.conn=sqlite3.connect("upEAT_1.sqlite")
        self.cursor=self.conn.execute("SELECT S.studentIDno,S.SSN\
                                      FROM STUDENT AS S,MEMBER AS M,ACCOUNT AS A\
                                      WHERE S.SSN=M.SSN AND A.username=? AND A.SSN=M.SSN",(username,))
        data=self.cursor.fetchall()
        if file_path:
                # Load the selected image
            original_image = Image.open(file_path)

            # Convert the image to RGB mode if it has an alpha channel
            if original_image.mode == 'RGBA':
                image = original_image.convert('RGB')
            else:
                image = original_image

            save_path="./profpic/"+str(data[0][0])+".jpg"
            image.save(save_path)
            self.conn.execute("UPDATE MEMBER\
                              SET picture=?\
                              WHERE SSN=?",(save_path,data[0][1],))
            self.conn.commit()
        
        self.conn.close()

        
    def allergiesBtn(self):
        from register_alergies import AllergiesWindow
        self.conn=sqlite3.connect('upEAT_1.sqlite')
        self.curr=self.conn.execute('SELECT SSN\
                                    FROM ACCOUNT\
                                    WHERE username=?',(self.username,))
        ssn=self.curr.fetchall()[0][0]
        alerg_win=AllergiesWindow(ssn=ssn)
        self.conn.close()
        
