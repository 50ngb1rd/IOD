# -*- coding: utf-8 -*-
"""
Created on Wed May 26 19:07:13 2021

@author: marchia
"""

from tkinter import *
import tkinter.font as font
from PIL import ImageTk
from PIL import Image
import cv2
import speech_recognition as sr
from gtts import gTTS
import playsound
import os

import re
import subprocess




'''
Rememember! Set your file path to where you have darknet.exe

'''


window = Tk()
window.title("Vision- Money Counter")

logo_img = cv2.imread("D:/projects/vision_2_logo.png")
logo_img = Image.fromarray(logo_img)
logo = ImageTk.PhotoImage(logo_img)



width, height = 600, 400
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)





lmain = Label(window)
cv2image = None
            
def show_frame():
    global frame
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
    
    
def take_picture(event):
    cv2.imwrite('C:/darknet/build/darknet/x64/data/snap1.jpg', frame)
    result = subprocess.run('darknet.exe detector test data/obj.data yolov4-dollars.cfg backup/dollars/yolov4-dollars_last.weights -dont_show data/snap1.jpg', capture_output = True)
    result = result.stdout
    print(result)
    result = str(result)
    result = result.replace("\\r", "")
    result = result.replace("\\n", " ")
    result_list = re.split('\s', result)
    
    target_index = None
    for i in range(len(result_list)-1,0,-1):
        print(result_list[i])
        if result_list[i] == 'milli-seconds.':
            target_index = i
            break;
        else:
            continue
        
    
    obj_list = []
    
    for i in range(target_index +1, len(result_list)):
        val = re.sub('[:%]', '', result_list[i])
        obj_list.append(val)
        
        
    obj_list.pop()
    
    for i in range(len(obj_list)):
        if i % 2 !=0:
            obj_list[i] = float(obj_list[i]) / 100
        else:
            obj_list[i] = float(obj_list[i])
            
            
    final_obj_list = []
    for i in range(len(obj_list)):
        if i%2 == 0:
            continue
        else:
            if obj_list[i] > 0.8:
                final_obj_list.append(obj_list[i-1])
                final_obj_list.append(obj_list[i])
                
                
    total = 0
    for i in range(len(obj_list)):
        if i%2 == 0:
            total += obj_list[i]
        else:
            continue


    text = str(total) + ' dollars'
    tts = gTTS(text = text, lang='en')
    filename = 'voice1.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)
                               
    
    

        


#photo = tkinter.PhotoImage(file = r"C:/Users/marchia/Pictures/money_icon.png")


myFont = font.Font(size=50)

btn = Button(window, text="Detect", height =5, width = 5)
btn['font'] = myFont
lbl = Label(window,image=logo)

btn.bind('<Button-1>', take_picture)

Grid.rowconfigure(window,0,weight=1)
Grid.columnconfigure(window,0,weight=1)
 
Grid.rowconfigure(window,1,weight=1)
Grid.rowconfigure(window,2,weight=1)



#frame  = Frame(window)
#frame.grid(column=0, row=1, sticky="nsew")

#btn = Button(window, image = image)
btn.grid(row=2,column=0, sticky="NSEW")
lbl.grid(row=0,column=0, sticky='NSEW')
lmain.grid(row=1,column=0, sticky = 'NSEW')




show_frame()



window.mainloop()





    

    
        

