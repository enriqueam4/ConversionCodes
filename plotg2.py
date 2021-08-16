import matplotlib
import matplotlib.pyplot as plt
import os
import csv
import numpy as np
import string

from tkinter import filedialog
from tkinter import *
import os.path
from os import path


def main():
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select Folder With g2 ascii files")
    os.chdir(directory)

    for filename in os.listdir(directory):
        name, extension = os.path.splitext(filename)
        plt.style.use('dark_background')
        plt.rcParams['axes.prop_cycle']
        plt.rcParams["figure.figsize"] = (14, 4)
        if extension == ".dat":
            with open(filename, newline='\n') as f:
                reader = csv.reader(f)
                i = 0
                j = 0
                for row in reader:
                    if i == 2:
                        numRows = int(row[0])
                        counts = np.zeros(numRows)
                        delay = np.zeros(numRows)
                    elif i == 8:
                        temp = row[0].split("\t")
                        nsPerBin = float(temp[0])
                    elif i > 10 and i <= numRows + 10:
                        temp = row[0].split("\t")
                        data = int(temp[0])
                        counts[j] = data
                        j += 1
                    i += 1

                num = 0
                delay = []
                while num < 400:
                    delay.append(num)
                    num += nsPerBin

                delay = np.asarray(delay)
                counts = counts[0:len(delay)]

                plt.plot(delay, counts)
                plt.title("g2 measurement")
                plt.ylim([0, 1.1 * np.max(counts)])  # here we go 10 percent above top for nice looking data
                plt.xlabel("Delay [ns]")
                plt.ylabel("Counts")
                plt.savefig(name + ".png")
                print(name)
                plt.close('all')


if __name__ == '__main__':
    main()
