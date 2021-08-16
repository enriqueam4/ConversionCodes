import h5py
import os
import cv2
import numpy as np
from tkinter import filedialog
from tkinter import *

def main():
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select Folder with .emd files")
    if directory == "":
        return 0
    else:
        os.chdir(directory)

    k = 0
    n_emds = 0
    for filename in os.listdir(directory):
        if os.path.splitext(filename)[1] ==".emd":
            n_emds += 1
    
    for filename in os.listdir(directory):
        
        if os.path.splitext(filename)[1] == ".emd":
            k += 1
            f = h5py.File(filename, 'r')
            ff = f['Data']['Image']

            a = list(ff.keys())
            print(a)
            name = os.path.splitext(filename)[0]
            name = name.replace(' ', '_')
            print('file ' +str(k)+' of '+ str(n_emds)+'::'+name + ': ')

            for i in range(len(a)):
                image = ff[a[i]]
                imt = image['Data']
                frames = imt.shape[2]
                for j in range(frames):
                    print("Frame : " + str(j + 1) +' of ' + str(frames))
                    im = imt[:, :, j]
                    im = cv2.resize(im, (512, 512))
                    im = to_uint(im)
                    cv2.imwrite(name + '_frame' + str(j) + '.png', im)

            f.close()

def to_uint(image):
    image = image * 255.0 / image.max()
    image = image.astype(np.uint8)
    return image

if __name__ == '__main__':
    main()
