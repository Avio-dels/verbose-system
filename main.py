############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk, messagebox as mess
import tkinter.simpledialog as tsd
import customtkinter as ctk
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        
###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'ayushnagdive@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master, old, new, nnew
    master = ctk.CTk()
    master.geometry("400x200")
    master.resizable(False, False)
    master.title("Change Password")

    # Labels
    lbl_old = ctk.CTkLabel(master, text='Enter Old Password', font=('Segoe UI', 12, 'bold'))
    lbl_old.place(x=20, y=20)

    lbl_new = ctk.CTkLabel(master, text='Enter New Password', font=('Segoe UI', 12, 'bold'))
    lbl_new.place(x=20, y=70)

    lbl_confirm = ctk.CTkLabel(master, text='Confirm New Password', font=('Segoe UI', 12, 'bold'))
    lbl_confirm.place(x=20, y=120)

    # Entry fields
    old = ctk.CTkEntry(master, width=200, show="*")
    old.place(x=200, y=20)

    new = ctk.CTkEntry(master, width=200, show="*")
    new.place(x=200, y=70)

    nnew = ctk.CTkEntry(master, width=200, show="*")
    nnew.place(x=200, y=120)

    # Buttons
    save_btn = ctk.CTkButton(master, text="Save", command=save_pass, width=150, fg_color="#00fcca", text_color="black")
    save_btn.place(x=50, y=160)

    cancel_btn = ctk.CTkButton(master, text="Cancel", command=master.destroy, width=150, fg_color="#eb4600", text_color="white")
    cancel_btn.place(x=210, y=160)

    master.mainloop()


#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")

    # Load or create student CSV
    serial = 0
    exists = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            next(reader1)  # skip header
            for l in reader1:
                serial += 1
        serial += 1
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+', newline='') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1

    Id = txt.get().strip()
    name = txt2.get().strip()

    if name.replace(' ', '').isalpha():
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while True:
            ret, img = cam.read()
            if not ret:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                # Save image with correct path format
                filename = f"{name}.{serial}.{Id}.{sampleNum}.jpg"
                cv2.imwrite(os.path.join("TrainingImage", filename),
                            gray[y:y + h, x:x + w])
                cv2.imshow('Taking Images', img)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum >= 50:  # can increase to 100 if you want
                break

        cam.release()
        cv2.destroyAllWindows()

        # Save student info in CSV
        row = [serial, '', Id, '', name]
        with open('StudentDetails/StudentDetails.csv', 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

        message1.configure(text=f"Images Taken for ID : {Id}")
        txt.delete(0, 'end')
        txt2.delete(0, 'end')
    else:
        message1.configure(text="Enter a valid name (letters only)")


########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []

    for imagePath in imagePaths:
        try:
            filename = os.path.split(imagePath)[-1]
            parts = filename.split(".")
            if len(parts) < 4:
                continue  # skip files with wrong format
            ID = int(parts[1])  # SERIAL NO.
            pilImage = Image.open(imagePath).convert('L')
            imageNp = np.array(pilImage, 'uint8')
            faces.append(imageNp)
            Ids.append(ID)
        except Exception as e:
            print(f"Skipped file {imagePath}: {e}")
            continue

    return faces, Ids


###########################################################################################

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")

    # Clear existing entries in the GUI table
    for k in tv.get_children():
        tv.delete(k)

    # Load recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel/Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel/Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return

    # Load Haar Cascade
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    # Load student details
    exists1 = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails/StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        return

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']

    logged_ids = set()  # Keep track of students already logged in this session

    while True:
        ret, im = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < 50:
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values

                if len(aa) > 0 and len(ID) > 0:
                    name_str = str(aa[0])
                    ID_str = str(ID[0])
                else:
                    name_str = "Unknown"
                    ID_str = "Unknown"

                # Log attendance only once per student per session
                if ID_str != "Unknown" and ID_str not in logged_ids:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    attendance = [ID_str, '', name_str, '', date, '', timeStamp]

                    file_path = f"Attendance/Attendance_{date}.csv"
                    if os.path.isfile(file_path):
                        with open(file_path, 'a+', newline='') as csvFile1:
                            writer = csv.writer(csvFile1)
                            writer.writerow(attendance)
                    else:
                        with open(file_path, 'a+', newline='') as csvFile1:
                            writer = csv.writer(csvFile1)
                            writer.writerow(col_names)
                            writer.writerow(attendance)

                    logged_ids.add(ID_str)
                    tv.insert('', 0, text=ID_str, values=(name_str, date, timeStamp))

                # Label face with name
                cv2.putText(im, name_str, (x, y - 10), font, 1, (255, 255, 255), 2)

            else:
                cv2.putText(im, "Unknown", (x, y - 10), font, 1, (255, 255, 255), 2)

        cv2.imshow('Taking Attendance', im)

        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    
###########################################################################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################

# ------------------------ CLOCK ------------------------ #
def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.configure(text=time_string)   # ✅ CustomTkinter uses configure
    clock.after(1000, tick)

# ------------------------ SMOOTH HOVER EFFECT ------------------------ #
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

def smooth_hover(btn, start_color, end_color, steps=10, delay=20):
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    dr = (end_rgb[0] - start_rgb[0]) / steps
    dg = (end_rgb[1] - start_rgb[1]) / steps
    db = (end_rgb[2] - start_rgb[2]) / steps

    def enter(event):
        for i in range(1, steps + 1):
            new_color = rgb_to_hex((int(start_rgb[0] + dr*i),
                                    int(start_rgb[1] + dg*i),
                                    int(start_rgb[2] + db*i)))
            window.after(i*delay, lambda c=new_color: btn.config(bg=c))

    def leave(event):
        for i in range(1, steps + 1):
            new_color = rgb_to_hex((int(end_rgb[0] - dr*i),
                                    int(end_rgb[1] - dg*i),
                                    int(end_rgb[2] - db*i)))
            window.after(i*delay, lambda c=new_color: btn.config(bg=c))

    btn.bind("<Enter>", enter)
    btn.bind("<Leave>", leave)

######################################## MODERN CUSTOMTKINTER UI ###########################################


# Set CustomTkinter theme
ctk.set_appearance_mode("dark")        # "light" or "dark"
ctk.set_default_color_theme("blue")    # "blue", "green", "dark-blue"

# ------------------------ MAIN WINDOW ------------------------ #
window = ctk.CTk()
window.title("Face Recognition Attendance System")
window.geometry("1280x720")
window.resizable(True, False)

# ------------------------ HEADER ------------------------ #
header = ctk.CTkLabel(window, 
                      text="Face Recognition Attendance Monitoring System",
                      font=("Arial", 26, "bold"))
header.pack(pady=10)

# ------------------------ CLOCK & DATE ------------------------ #
frame_top = ctk.CTkFrame(window)
frame_top.pack(fill='x', pady=5)

day, month, year = datetime.datetime.now().strftime('%d-%m-%Y').split("-")
mont = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June',
        '07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}

date_label = ctk.CTkLabel(frame_top, 
                          text=f"{day}-{mont[month]}-{year}", 
                          font=("Arial", 16, "bold"))
date_label.pack(side='left', padx=20)

clock = ctk.CTkLabel(
    frame_top,
    font=("Segoe UI", 18, "bold"),
    text_color="white"
)
clock.pack(side="right", padx=20)
tick()


# ------------------------ FRAMES ------------------------ #
frame_left = ctk.CTkFrame(window, width=600, height=580, corner_radius=15)
frame_left.place(x=50, y=100)

frame_right = ctk.CTkFrame(window, width=580, height=580, corner_radius=15)
frame_right.place(x=650, y=100)

# ------------------------ LEFT FRAME (Attendance Table) ------------------------ #
att_btn = ctk.CTkButton(frame_left, text="Take Attendance", command=TrackImages, width=250, fg_color="#3ffc00", text_color="black")
att_btn.place(x=150, y=20)

quit_btn = ctk.CTkButton(frame_left, text="Quit", command=window.destroy, width=250, fg_color="#eb4600", text_color="white")
quit_btn.place(x=150, y=520)

tv = ttk.Treeview(frame_left, columns=('name','date','time'), show='headings', height=20)
tv.heading('name', text='NAME')
tv.heading('date', text='DATE')
tv.heading('time', text='TIME')
tv.column('name', width=180)
tv.column('date', width=140)
tv.column('time', width=140)
tv.place(x=20, y=80)

scroll = ttk.Scrollbar(frame_left, orient='vertical', command=tv.yview)
scroll.place(x=570, y=80, height=435)
tv.configure(yscrollcommand=scroll.set)

# ------------------------ RIGHT FRAME (New Registration) ------------------------ #
ctk.CTkLabel(frame_right, text="New Registration", font=("Arial", 18, "bold"), text_color="#00fcca").place(x=180, y=10)

ctk.CTkLabel(frame_right, text="Enter ID:", font=("Arial", 12)).place(x=50, y=60)
txt = ctk.CTkEntry(frame_right, width=200, placeholder_text="Enter Student ID")
txt.place(x=200, y=60)
clear_id_btn = ctk.CTkButton(frame_right, text="Clear", command=clear, width=80, fg_color="#ff7221")
clear_id_btn.place(x=420, y=60)

ctk.CTkLabel(frame_right, text="Enter Name:", font=("Arial", 12)).place(x=50, y=120)
txt2 = ctk.CTkEntry(frame_right, width=200, placeholder_text="Enter Student Name")
txt2.place(x=200, y=120)
clear_name_btn = ctk.CTkButton(frame_right, text="Clear", command=clear2, width=80, fg_color="#ff7221")
clear_name_btn.place(x=420, y=120)

message1 = ctk.CTkLabel(frame_right, text="1) Take Images  >>>  2) Save Profile", font=("Arial", 12))
message1.place(x=50, y=180)

takeImg = ctk.CTkButton(frame_right, text="Take Images", command=TakeImages, width=300, fg_color="#6d00fc")
takeImg.place(x=120, y=230)

trainImg = ctk.CTkButton(frame_right, text="Save Profile", command=psw, width=300, fg_color="#6d00fc")
trainImg.place(x=120, y=300)

# ------------------------ MENUBAR ------------------------ #
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Change Password', command=change_pass)
filemenu.add_command(label='Contact Us', command=contact)
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', menu=filemenu)
window.config(menu=menubar)

window.mainloop()
######################################## END OF MODERN UI ###########################################
