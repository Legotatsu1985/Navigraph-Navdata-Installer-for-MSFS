
import glob
import os
import shutil
import sys
import tkinter
import tkinter.messagebox
from tkinter import filedialog

import rarfile

def on_nav_update_select_button_click():
    checked = [msfs_native_update.get(), pmdg_update.get(), fenix_update.get()]
    if checked == [1, 0, 0]:
        label.config(text="MSFS Native navdata will be installed only.")
    elif checked == [0, 1, 0]:
        label.config(text="PMDG 737 navtdada will be installed only.")
    elif checked == [0, 0, 1]:
        label.config(text="Fenix A320 navdata will be installed only.")
    elif checked == [1, 1, 0]:
        label.config(text="MSFS Native and PMDG 737 navdatas will be installed.")
    elif checked == [0, 1, 1]:
        label.config(text="PMDG 737 and Fenix A320 navdatas will be installed.")
    elif checked == [1, 0, 1]:
        label.config(text="MSFS Native and Fenix A320 navdatas will be installed.")
    elif checked == [1, 1, 1]:
        label.config(text="All contents will be installed.")
    else:
        label.config(text="Please select the checkbox you want to install!")

root = tkinter.Tk()
root.title("Navigraph Navdata Installer for MSFS")
root.geometry("300x150")
msfs_native_update = tkinter.IntVar()
pmdg_update = tkinter.IntVar()
fenix_update = tkinter.IntVar()
tkinter.Checkbutton(root, text="MSFS Native Navdata", variable=msfs_native_update).pack()
tkinter.Checkbutton(root, text="PMDG 737 Navdata", variable=pmdg_update).pack()
tkinter.Checkbutton(root, text="Fenix A320 Navdata", variable=fenix_update).pack()
button = tkinter.Button(root, text="Start Update", command=on_nav_update_select_button_click)
button.pack()
label = tkinter.Label(root)
label.pack()
root.mainloop()