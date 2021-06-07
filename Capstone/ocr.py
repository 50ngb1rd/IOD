# -*- coding: utf-8 -*-
"""
Created on Fri May 28 22:04:41 2021

@author: march
"""

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
import easyocr




'''
Rememember! Set your file path to where you have darknet.exe

'''


window = Tk()
window.title("Vision- Money Counter")

logo_img = cv2.imread("D:/projects/vision_2_logo.png")
logo_img = Image.fromarray(logo_img)
logo = ImageTk.PhotoImage(logo_img)



width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

reader = easyocr.Reader(['en'])





lmain = Label(window)
cv2image = None
            
def show_frame():
    global frame
    _, frame = cap.read()
    #frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
    
    
def take_picture(event):
    cv2.imwrite('D:/projects/word1.jpg', frame)
    result = reader.readtext(frame)
    print(result)
    
    counter = 1
    area_list = []
    label_list = {}
    for i in result:
        
        label = i[1]
        if label == 'PRESCRIPTION ONLY MEDICINE' or label == 'KEEP OUT OF REACH OF CHILDREN':
            prescp_med = True
            continue
        else:
            label_list[counter] = label
            
            bbox = i[0]
            width = bbox[1][0] - bbox[0][0]
            height = bbox[3][1] - bbox[0][1]
            obj_area = width * height
            area_list.append([obj_area, counter])
            counter += 1
            
    sorted_area_list = sorted(area_list,reverse=True)
    
    word_len = len(sorted_area_list)
    val_list = []
    for i in range(len(result)):
        ind = sorted_area_list[i][1]
       # val = label_list[ind]
        val = result[i][1]
        val_list.append(val)
        text = val

        tts = gTTS(text = text, lang='en')
        filename = 'voice1.mp3'
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
                                   
    
    

        


#photo = tkinter.PhotoImage(file = r"C:/Users/marchia/Pictures/money_icon.png")


myFont = font.Font(size=30)

btn = Button(window, text="Picture", height =10, width = 10)
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





    

    
        

