import tkinter as tk
from PIL import ImageTk, Image,ImageDraw,ImageFont
from navigator import Navigator
import sqlite3
import qrcode

class ProfileFrame(tk.Frame):
    def __init__(self,master,username,**kwargs):
        super().__init__(master,bg='#D2E9E9',**kwargs)
        self.username=username
        self.navigator=Navigator(self,master,username=self.username)
        self.master=master
        self.master.geometry("500x520")
        self.pack()
        self.create_content()
        
    
    def create_content(self):
        color1 = '#D2E9E9'
        color2 = '#D2E9E9'
        west1_frame = tk.Frame(self, bg=color1)
        west1_frame.grid(column=0,row=0,columnspan=4)
        
        west2_frame = tk.Frame(self, bg=color2)
        west2_frame.grid(column=0,row=2)

        east_frame = tk.Frame(self, bg=color1)
        east_frame.grid(column=3,row=0,rowspan=3)
        
        
        self.conn=sqlite3.connect("upEAT_1.sqlite")
        self.cursor=self.conn.execute("SELECT A.username,A.barcode,M.SSN,M.firstname,M.lastname,M.phoneno,M.picture,S.studentIDno,S.semester,S.dptname,M.address\
                                       FROM ACCOUNT AS A, MEMBER AS M, STUDENT AS S\
                                      WHERE A.username=? AND A.SSN=M.SSN AND A.SSN=S.SSN",(self.username,))
        data=self.cursor.fetchall()
        
        prof_img=data[0][6]
        if (prof_img==None): #check that there is a relative profpic path otherwise put default pic
            prof_img="./profpic/user-profile.jpg"
        
        self.conn.close()
        # PROFILE IMAGE
        try:
            profile_picture = Image.open(prof_img)
        except IOError as e:
            prof_img="./profpic/user-profile.jpg"
            profile_picture=Image.open(prof_img)

        profile_picture = profile_picture.resize((100,100))
        prof_pic = ImageTk.PhotoImage(profile_picture)    
        
        #EDIT IMAGE
        edit_picture = Image.open("./media/edit.png")
        edit_picture = edit_picture.resize((20,20))
        edit_pic = ImageTk.PhotoImage(edit_picture)  
        



        labels = []
        edit_pic_label = tk.Label(west1_frame,image=edit_pic)
        edit_pic_label.image = edit_pic
        prof_pic_label = tk.Label(west1_frame,image=prof_pic)
        prof_pic_label.image = prof_pic
        name_label=tk.Label(west1_frame, text=data[0][3]+" "+data[0][4],bg=color1,fg='black',font=('Calibri', 22, 'bold'))
        afm_label=tk.Label(west1_frame, text=data[0][2],bg=color1,fg='black',font=('Calibri', 18, 'bold'))

        fname="Όνομα: "+data[0][3]
        lname="Επίθετο: "+data[0][4]
        if(data[0][5]==None):
            phone="Τηλ: "+"-"
        else:
            phone="Τηλ: "+data[0][5]

        am="Αρ.Μητ: "+str(data[0][7])

        if(data[0][8]==None):
             semester="Εξάμηνο: "+"-"
        else:
            semester="Εξάμηνο: "+str(data[0][8])
        
        if(data[0][9]==None):
            school="Τμήμα: "+"-"
        else:
            school="Τμήμα: "+data[0][9]

        
        username="Ον.χρήστη: "+data[0][0]
        barcode="Barcode: "+str(data[0][1])
        ssn="ΑΜΚΑ: "+str(data[0][2])

        if(data[0][10]==None):
            address="Διεύθυνση: "+"-"
        else:
            address="Διεύθυνση: "+str(data[0][10])
        
        
        fname_label=tk.Label(west2_frame, text=fname,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        lname_label=tk.Label(west2_frame, text=lname,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        phone_label=tk.Label(west2_frame, text=phone,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        am_label=tk.Label(west2_frame, text=am,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        semester_label=tk.Label(west2_frame, text=semester,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        school_label=tk.Label(west2_frame, text=school,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        username_label=tk.Label(west2_frame, text=username,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        barcode_label=tk.Label(west2_frame, text=barcode,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        SSN_label=tk.Label(west2_frame, text=ssn,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        address_label=tk.Label(west2_frame,text=address,bg=color2,fg='black',font=('Calibri',13,'bold'))
        
        back_btn = tk.Button(east_frame,text="Back",command=lambda: self.back(self.username),font=('Calibri', 13, 'bold'))
        back_btn.grid(row=3, column=0, pady=10)
        #WEST 2
        #categories
        fname_label.grid(column=0,row=1)
        lname_label.grid(column=0,row=2)
        phone_label.grid(column=0,row=3)
        am_label.grid(column=0,row=4)
        semester_label.grid(column=0,row=5)
        school_label.grid(column =0, row=6)
        username_label.grid(column=0,row=7)
        barcode_label.grid(column=0,row=8)
        SSN_label.grid(column=0,row=9)
        address_label.grid(column=0,row=10)

        



        my_upeat_card=tk.Button(west2_frame,font=('Calibri', 13, 'bold'), height=1, width =15,\
            text="My upEAT Card",pady=5,command=lambda: self.showCard(self.username))
        purchase_btn=tk.Button(east_frame,font=('Calibri', 13, 'bold'), height=1, width =25,\
            text="Purchase & Review History",command=lambda: self.purchase(self.username), pady=10)
        edit_btn=tk.Button(west2_frame,text="Edit your profile",image=edit_pic,compound='right'  ,font=('Calibri', 13, 'bold'), height=20, width =150,\
            command=lambda: self.edit(self.username))
        
        logout_btn=tk.Button(east_frame,font=('Calibri', 13, 'bold'), height=1, width =15,\
            text="Logout",command=lambda: self.logout_btn())
        
        
        #WEST 1
        prof_pic_label.grid(column=0,row=0, rowspan=5)
        name_label.grid(column=1,row=0, padx=5, columnspan=3)
        afm_label.grid(column=1,row=1)
        
        

        
    
        edit_btn.grid(column =0, row=11, pady=10)
        
        #RIGHT
        purchase_btn.grid(column=0,row=1, pady=5)
        logout_btn.grid(column=0,row=2, pady=5)
        my_upeat_card.grid(column=0,row=13)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(2, weight=1)
        
    
    def generate_digital_card(self,username):

        self.conn=sqlite3.connect("upEAT_1.sqlite")
        self.cursor=self.conn.execute("SELECT A.barcode,M.firstname,M.lastname,M.phoneno,M.picture,S.studentIDno,S.semester,S.dptname\
                                       FROM ACCOUNT AS A, MEMBER AS M, STUDENT AS S\
                                      WHERE A.username=(?) AND A.SSN=M.SSN AND A.SSN=S.SSN",(username,))
        data=self.cursor.fetchall() 
        barcode=data[0][0]
      
        barcode=data[0][0]
        fname=data[0][1]
        lname=data[0][2]
        if(data[0][3]==None):
            phone="-"
        else:
            phone=str(data[0][3])
        
        if(data[0][7]==None):
            dptname="-"
        else:
            dptname=str(data[0][7])
        
        photo=data[0][4]
        am=str(data[0][5])
        
        qr=qrcode.QRCode(version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        qr.add_data(barcode) #edw tha mpei to barcode
        qr.make(fit=True) 
        save_qr_path="./qrcodes/"+str(data[0][5])+".png"

        img=qr.make_image(fill_color='black',back_color='#D2E9E9')
        img.save(save_qr_path) #edw tha mpei to path tou qrcode tou acc
        # Create a blank image
        card = Image.new('RGB', (600, 400), '#D2E9E9')
        draw = ImageDraw.Draw(card)

        # Load a font
        font_path = "arial.ttf"  # Use a font file path on your system
        font_size = 24
        font = ImageFont.truetype(font_path, font_size)

        # Draw name and surname
        draw.text((230,10),"upEAT CARD",font=font,fill='black')
        draw.text((50, 50), fname, font=font, fill='black') 
        draw.text((50, 100), lname, font=font, fill='black')
        draw.text((50,150), phone,font=font,fill='black')
        draw.text((50,200), am,font=font,fill='black')
        #draw.text((50,250), semester,font=font,fill='black')
        draw.text((50,250),dptname,font=font,fill='black')

        # Load the QR code image
        qr_code = Image.open(save_qr_path) #edw tha mpei to path tou qr pou dimiourgithike gia to user
        qr_code = qr_code.resize((160, 160))  # Adjust the size as needed

        if photo is not None:
            prof_pic_path=photo
        else:
            prof_pic_path="./profpic/user-profile.jpg"
        user_prof=Image.open(prof_pic_path) #edw tha anoigei tin profpic tou user i to default
        user_prof= user_prof.resize((150, 150))
        # Paste the QR code onto the digital card
        card.paste(qr_code, (420, 250))
        card.paste(user_prof,(420,20))
        output_path="./digital_cards/"+"upeatcard_"+str(data[0][5])+".png"
        # Save the digital card in the correct path
        card.save(output_path)

        self.conn.close()
        return output_path



    def showCard(self,username):
        self.conn=sqlite3.connect("upEAT_1.sqlite")
        curr=self.conn.execute("SELECT S.studentIDno\
                            FROM STUDENT AS S,ACCOUNT AS A, MEMBER AS M\
                            WHERE A.SSN=M.SSN AND M.SSN=S.SSN AND A.username=?",(username,))
        studnum=curr.fetchall()
        mypath="./digital_cards/upeatcard_"+str(studnum[0][0])+".png"
        
        mypath=self.generate_digital_card(username)
        from upEAT_card import upeatCardWindow
        self.conn.close()
        upeatcard_win=upeatCardWindow(self,path=mypath)
        return

        
        


    
    #FUNCTIONS
    def purchase(self, username):
        from purch_rev_page import PurchRevFrame
        self.destroy()
        purchase_frame=PurchRevFrame(self.master, username=username)
        purchase_frame.pack()
            
    def edit(self,username):
        from edit_data import EditdataFrame
        self.destroy()
        edit_frame=EditdataFrame(self.master,username=self.username)
        edit_frame.pack()
        
    def logout_btn(self):
        from login_page import LoginFrame
        self.navigator.destroynav()
        self.destroy()
        login_frame=LoginFrame(self.master)
        login_frame.pack()

    def back(self,username):
        from home_page import WelcomeFrame
        self.destroy()
        purchase_frame=WelcomeFrame(self.master, username=username)
        purchase_frame.pack()
