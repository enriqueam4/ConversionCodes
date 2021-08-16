from tkinter import filedialog
from tkinter import *
import h5py
import os.path
from os import path
import string
import numpy as np

def main():
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select Folder With Spectra")
    if directory == "":
        return
    os.chdir(directory)

    for filename in os.listdir(directory):
        if filename[0] == 'E':                              # yes i know this isn't secure, but i'm not spending any more time on this
            name, extension = os.path.splitext(filename)
            date = name.split("_")
            save_name = ""
            save_name += "Spectrum_"
            year = filter(str.isdigit, date[1])
            year = "".join(year)
            month = date[2]
            day = date[3]
            hour = date[4]
            minute = date[5]
            second = date[6]
            if extension == ".mat":
                h5_file = h5py.File(os.path.join(directory, filename), 'r')
                data = h5_file['data']['data']
                keys = list(data.keys())

                if "flake" in keys:
                    flake = bytes(data.get('flake')[:])
                    flake = str(flake.decode('utf-8'))
                    save_name += 'F'
                    save_name += flake.strip()
                    save_name += '_'

                if "emitter" in keys:
                    emitter = bytes(data.get('emitter')[:])
                    emitter = emitter.decode('utf-8')
                    save_name += 'E'
                    save_name += emitter.strip()
                    save_name += '_'

                if "cursor_x" in keys:
                    x_pos_float = data["cursor_x"][0][0]
                    x_pos_round = np.round(x_pos_float, 2)
                    x_pos = str(x_pos_round)
                    x_pos = x_pos.replace("-","n")
                    x_pos = x_pos.replace(".","p")
                    save_name += "X"
                    save_name += x_pos
                    save_name += '_'

                if "cursor_y" in keys:
                    y_pos = str(data["cursor_y"][0][0])
                    y_pos_float = data["cursor_y"][0][0]
                    y_pos_round = np.round(y_pos_float, 2)
                    y_pos = str(y_pos_round)
                    y_pos = y_pos.replace("-", "n")
                    y_pos = y_pos.replace(".", "p")
                    save_name += "Y"
                    save_name += y_pos
                    save_name += '_'

                save_name += year
                save_name += '_'
                save_name += month
                save_name += '_'
                save_name += day
                save_name += '_'
                save_name += hour
                save_name += '_'
                save_name += minute
                save_name += '_'
                save_name += second
                save_name += ".mat"
                save_path = os.path.join(directory, save_name.strip()).strip()
                file_path = os.path.join(directory, filename.strip()).strip()

                h5_file.close()
                new_content = ''
                for letter in save_path:
                    clean_line = letter.replace('\00', '')
                    new_content += clean_line

                save_path = str(new_content)
                try:
                    os.rename(file_path, save_path)
                except Exception as e:
                    print(e)


if __name__=="__main__":
    main()