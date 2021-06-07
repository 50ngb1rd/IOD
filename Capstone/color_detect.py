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
from sklearn.cluster import KMeans
import pandas as pd
import re




window = Tk()
window.title("Vision - Colour Detection")

logo_img = cv2.imread("D:/projects/vision_2_logo.png")
logo_img = Image.fromarray(logo_img)
logo = ImageTk.PhotoImage(logo_img)



width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

color_chart = pd.read_csv('D:/projects/color_chart.txt', header = None, sep = '\t')
r_list = []
g_list = []
b_list = []
total_list = []
rgb = color_chart[3]
for index, val in rgb.iteritems():
    val = re.sub("[\(\)]", "", val)
    val = re.split('\,', val)
    r_list.append(int(val[0]))
    g_list.append(int(val[1]))
    b_list.append(int(val[2]))
    total_list.append(int(val[0]) + int(val[1]) + int(val[2]))
    
color_chart['R'] = r_list
color_chart['G'] = g_list
color_chart['B'] = b_list






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
    cv2.imwrite('D:/projects/snap1.jpg', frame)
    print('working')
    img = frame
    img = img.reshape((img.shape[0] * img.shape[1], 3))
    clt = KMeans(n_clusters = 2)
    clt.fit(img)
    
    kmeans_label = list(clt.labels_)
    clt_centroids = clt.cluster_centers_
    
    percent=[]
    for i in range(len(clt_centroids)):
      j=kmeans_label.count(i)
      j=j/(len(kmeans_label))
      percent.append(j)
    
    target_ind = percent.index(max(percent))
    test_arr= clt_centroids[target_ind]
    print(test_arr)
    
    total_diff = []

    for index, val in color_chart.iterrows():
        diff_r = abs(test_arr[0] - val['R'])
        diff_g = abs(test_arr[1] - val['G'])
        diff_b = abs(test_arr[2] - val['B'])
        total = diff_r + diff_g + diff_b
        
        total_diff.append([total, index])

    
    
    total_diff.sort()
    result_list = []
    for i in range(10):
        result_list.append(color_chart.iloc[total_diff[i][1], 1])
        
    for i in range(3):
        print(result_list[i])
    text = 'The top 3 colours for the image are' +  str(result_list[0]) + ',' +  str(result_list[1]) + 'and' + str(result_list[2])
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





    

    
        

