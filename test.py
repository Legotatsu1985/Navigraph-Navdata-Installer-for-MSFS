
import glob
import os
import shutil
import sys
import tkinter
import tkinter.messagebox
from tkinter import filedialog

import rarfile

def on_nav_update_select_button_click():
    if msfs_native_update.get() == 1:
        result_text = "It will update MSFS Native navdata."
    if pmdg_update.get() == 1:
        result_text = "It will update PMDG 737 navdata."
    label.config(text=result_text)

root = tkinter.Tk()
msfs_native_update = tkinter.IntVar()
msfs_check_box = tkinter.Checkbutton(root, text="MSFS Native Navdata", variable=msfs_native_update)
msfs_check_box.pack()
pmdg_update = tkinter.IntVar()
pmdg_check_box = tkinter.Checkbutton(root, text="PMDG 737 Navdata", variable=pmdg_update)
pmdg_check_box.pack()
button = tkinter.Button(root, text="Update", command=on_nav_update_select_button_click)
button.pack()
label = tkinter.Label(root)
label.pack()
root.mainloop()