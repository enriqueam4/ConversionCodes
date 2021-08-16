from scipy.io import loadmat
import os
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import *



def main():
    root = Tk()
    root.withdraw()
    # messagebox.showinfo("Attention", "Select Folder With .mat files")
    directory = filedialog.askdirectory(title="Select Folder With .mat files")

    if directory == "":
        return 0
    else:
        os.chdir(directory)

    for filename in os.listdir(directory):
        extension = os.path.splitext(filename)[1]
        if extension == ".mat" :
            print(filename)
            mat = loadmat(filename)
            matIm = mat['image'][0][0][0]
            matIm = to_uint(matIm)
            ROI = mat['image'][0][0][4]
            fig = plt.figure()
            s = fig.add_subplot(1, 1, 1)
            s.imshow(matIm, extent=(0, ROI[0, 1] - ROI[0, 0], 0, ROI[1, 1] - ROI[1, 0]), interpolation='none',
                     cmap='gray')
            plt.xlabel('x [microns]')
            plt.ylabel('y [microns]')
            plt.savefig(os.path.splitext(filename)[0] + ".png")
            plt.close()


def to_uint(image):
    image = image * 255.0 / image.max()
    image = image.astype(np.uint8)
    return image


if __name__ == '__main__':
    main()