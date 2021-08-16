from scipy.io import loadmat
import os
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os.path
from os import path
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import h5py
from PIL import ImageTk, Image

def main():
    root = tk.Tk()
    s = spectralScanGUI(root)
    root.mainloop()

class spectralScanGUI():
    wl_center = 530
    wl_bin_width = 10
    filename = []
    data = []
    scan = []
    wavelength = []


    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.pack()
        self.selectFile = tk.Button(self.frame, text="Select File", command=self.set_file)
        self.selectFile.pack(side=tk.LEFT)
        self.wl_center = 550
        self.wl_bin_width = 10
        self.set_file()
        self.button = tk.Button(self.frame, text="QUIT", fg="red", command=quit)
        self.button.pack(side=tk.LEFT)
        self.slider = tk.Scale(self.frame, from_=round(self.wavelength[0, 0]), to=round(self.wavelength[len(self.wavelength) - 1, 0]),orient=HORIZONTAL, label="Center Wavelength [nm]")
        self.slider.pack(side=tk.LEFT)
        self.width_slider = tk.Scale(self.frame, from_= 0 , to=round(self.wavelength[len(self.wavelength) - 1, 0]) - round(self.wavelength[0, 0]),orient=HORIZONTAL, label="Bin Width [nm]")
        self.width_slider.pack(side=tk.RIGHT)
        self.runButton = tk.Button(self.frame, text="RUN", command = self.run)
        self.runButton.pack(side=tk.RIGHT)
        self.saveButton = tk.Button(self.frame, text = "SAVE IMAGE", command=self.save)
        self.saveButton.pack(side=tk.RIGHT)
        image = self.produceImage(self.scan[:])
        pilIm = Image.fromarray(image)
        tkIm = ImageTk.PhotoImage(pilIm)
        self.canvas = tk.Canvas(root, width = 512, height = 512)
        self.canvas.create_image(0, 0, anchor=NW, image=tkIm)
        self.canvas.image = tkIm
        self.canvas.pack(side="bottom", fill="both", expand="yes")

    def run(self):
        self.wl_center = self.slider.get()
        self.wl_bin_width = self.width_slider.get()
        im = self.produceImage(self.scan[self.i_floor():self.i_ceil()])
        pilIm = Image.fromarray(im)
        tkIm = ImageTk.PhotoImage(pilIm)
        self.canvas.create_image(0,0, anchor=NW, image=tkIm)
        self.canvas.create_image(0,0, anchor=NW, image=tkIm)
        self.canvas.image = tkIm

    def i_floor(self):
        wl_floor = WavelengthClass(self.wl_center - self.wl_bin_width / 2, self.wavelength)
        return wl_floor.toIndex()

    def i_ceil(self):
        wl_ciel = WavelengthClass(self.wl_center + self.wl_bin_width / 2, self.wavelength)

    def set_file(self):
        self.filename = filedialog.askopenfilename()
        self.data = h5py.File(self.filename, 'r')
        self.scan = self.data['data']['data']['scan']
        self.wavelength = self.data['data']['data']['freq']

    def plotSpectra(self, wavelength, spectra):
        plt.plot(wavelength, spectra)
        plt.ylabel('Spectrum')
        plt.show()

    def produceImage(self, subscan):
        pixel = 0
        imsize = np.shape(subscan[0])
        current_image = np.zeros(imsize)
        buffer_image = np.copy(current_image)

        for i in range(imsize[0]):
            for j in range(imsize[1]):
                pixel = np.ma.mean(subscan[:, i, j])
                buffer_image[i][j] = pixel

        buffer_image -= buffer_image.min()
        buffer_image *= 255.0 / buffer_image.max()
        buffer_image = buffer_image.astype('uint8')
        current_image = buffer_image
        current_image = cv2.resize(current_image, (512, 512))
        return current_image

    def save(self):
        tempfilename = os.path.splitext(self.filename)[0]
        print(tempfilename)
        cv2.imwrite(tempfilename+"center"+str(self.wl_center)+"binwidth"+str(self.wl_bin_width)+".png", self.produceImage(self.scan[self.i_floor():self.i_ceil()]))

class WavelengthClass():
    val = 0
    array = []
    def __init__(self, val, array):
        self.val =  val
        self.array = array

    def toIndex(self):
        nearest_distance = np.inf
        nearest_index = 0
        for i in range(len(self.array)):
            current_distance = abs(self.array[i] - self.val)
            if current_distance < nearest_distance:
                nearest_distance = current_distance
                nearest_index = i
        return nearest_index

if __name__ == '__main__':
    main()