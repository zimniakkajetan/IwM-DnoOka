#!/usr/bin/python3
from tkinter import *
from tkinter import filedialog

from _thread import *
from math import *

import numpy as np
import time

from PIL import ImageTk, Image
import PIL
from skimage import io, filters
from skimage.color import rgb2gray
from PIL import ImageFilter
import cv2


class obraz():
    wejsciowy = []
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget
        self.master.title("Dno oka")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        self.grid(padx=4,pady=4)

        canvasSize=300

        # creating image canvases
        self.inputCanvas = Canvas(self,width=canvasSize, height=canvasSize,bg='white')
        self.inputCanvas.create_rectangle(2,2,canvasSize,canvasSize)
        self.inputCanvas.create_text(canvasSize/2,canvasSize/2,text="Obraz wejściowy")
        self.inputCanvas.grid(row=0,column=0)

        self.firstCanvas = Canvas(self, width=canvasSize,height=canvasSize,bg='white')
        self.firstCanvas.create_rectangle(2,2,canvasSize,canvasSize)
        self.firstCanvas.create_text(canvasSize/2,canvasSize/2,text="Obraz po pierwszej obróbce")
        self.firstCanvas.grid(row=0,column=1)

        self.outputCanvas = Canvas(self,width=canvasSize,height=canvasSize,bg='white')
        self.outputCanvas.create_rectangle(2,2,canvasSize,canvasSize)
        self.outputCanvas.create_text(canvasSize/2,canvasSize/2,text="Obraz wyjściowy")
        self.outputCanvas.grid(row=0,column=2)

        self.uploadInputButton = Button(self,text="Wgraj obraz",command=self.upload_input_file)
        self.uploadInputButton.grid(row=1,column=0,pady=2)

        xpadding=10
        top_padding=20
        bottom_padding=5

        self.startButton = Button(self, text="Start", command=self.firstStep, width=8)
        self.startButton.grid(row=8, column=2, sticky='e', padx=20, pady=10)

        self.error = StringVar()
        Label(self, textvariable=self.error, fg="red", font=("Helvetica", 16)).grid(row=8)

        self.master.update()


    def upload_input_file(self):
        filename = filedialog.askopenfilename(filetypes=[('Image','jpg jpeg png gif')])
        if filename != "": self.set_input_image(filename)

    def set_image(self,path,canvas):
        img = Image.open(path)
        print(img)

        img = img.resize((canvas.winfo_width(), canvas.winfo_height()), Image.ANTIALIAS)

        obraz.wejsciowy = img

        canvas.image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=canvas.image, anchor=NW)

    def set_input_image(self,path):
        self.set_image(path,self.inputCanvas)

    def firstStep(self):
        #self.error.set("")
        self.firstCanvas.create_rectangle(0, 0, self.firstCanvas.winfo_width(), self.firstCanvas.winfo_height(), fill="black")
        start_new_thread(self.firstStep1, ())

    def firstStep1(self):
        pic = obraz.wejsciowy
        print(pic)
        pic = pic.convert('L')

        pic = pic.filter(ImageFilter.FIND_EDGES)

        pic = np.array(pic)

        th, pic = cv2.threshold(pic, 20, 255, cv2.THRESH_BINARY);

        #filtr gaszący pixel jeżeli każdy z 8 sąsiadów jest zgaszony
        pic=self.denoise(pic)
        #zamkniecie naczyn
        pic=self.contourClose(pic)
        #alternatywne:
        #pic=self.morphologicClose(pic)

        self.setFirstStepOutput(Image.fromarray(pic))
        return pic

    def denoise(self,pic):
        pic2=np.copy(pic)
        for i in range(1,pic.shape[0]-1):
            for j in range(1, pic.shape[1]-1):
                if pic[i][j]==255:
                    if pic[i-1][j-1]==0 and pic[i-1][j]==0 and pic[i-1][j+1]==0 and pic[i][j-1]==0 and pic[i][j+1]==0 and pic[i+1][j-1]==0 and pic[i+1][j]==0 and pic[i+1][j+1]==0:
                        pic2[i][j]=0
        return pic2

    def contourClose(selfs,pic):
        im2, contours, hierarchy = cv2.findContours(pic, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return cv2.drawContours(pic, contours, -1, (255, 255, 255), 2)

    def morphologicClose(self,pic):
        kernel = np.ones((3, 3), np.uint8)
        return cv2.morphologyEx(pic, cv2.MORPH_CLOSE, kernel)

    def setFirstStepOutput(self,pic):
        #self.sinogramCanvas.delete("all")
        self.firstCanvas.image = ImageTk.PhotoImage(pic)
        #self.firstCanvas.image = ImageTk.PhotoImage(pic)
        self.firstCanvas.create_image(0, 0, image=self.firstCanvas.image, anchor=NW)

    def blad(self, pic1, pic2):
        suma = 0
        for row in range(len(pic1)):
            for col in range(len(pic1[0])):
                suma += (pic1[row][col] - pic2[row][col]) * (pic1[row][col] - pic2[row][col])

        return sqrt(suma / (len(pic1)*len(pic1[0])))

root = Tk()
root.geometry("920x460")

app=Window(root)



root.mainloop()
