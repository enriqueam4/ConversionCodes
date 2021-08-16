import matplotlib
import matplotlib.pyplot as plt
import os
import csv
import numpy as np
from tkinter import filedialog
from tkinter import *
import os.path
from os import path
import h5py

def main():
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select Folder With .mat spectra files")
    os.chdir(directory)

    for filename in os.listdir(directory):
        name, extension = os.path.splitext(filename)
        wavelength = []
        intensity = []
        exposure = 0
        center_wavelength = 0
        plt.style.use('dark_background')
        plt.rcParams['axes.prop_cycle']
        plt.rcParams["figure.figsize"] = (14, 4)
        if extension == ".mat":
            data = h5py.File(filename, 'r')
            intensity = data['data']['data']['y']
            wavelength = data['data']['data']['x']
            exposure =  data['data']['data']['exposure']
            center_wavelength = data['data']['data']['center_wl']
            plt.plot(wavelength, intensity)
            plt.title("Spectrum at Center = "+str(center_wavelength[0][0])+" nm, Exposure = "+str(exposure[0][0])+" ms")
            plt.xlabel("Wavelength [nm]")
            plt.ylabel("Counts [a.u.]")
            # plt.show()
            plt.savefig(name + ".png")
            print(name)
            plt.close('all')


if __name__ == '__main__':
    main()
