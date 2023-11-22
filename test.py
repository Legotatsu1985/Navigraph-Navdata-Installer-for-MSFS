
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
        install_confirmation("MSFS Native navdata will be installed only. Do you continue?")
    elif checked == [0, 1, 0]:
        install_confirmation("PMDG 737 navtdada will be installed only. Do you continue?")
    elif checked == [0, 0, 1]:
        install_confirmation("Fenix A320 navdata will be installed only. Do you continue?")
    elif checked == [1, 1, 0]:
        install_confirmation("MSFS Native and PMDG 737 navdatas will be installed. Do you continue?")
    elif checked == [0, 1, 1]:
        install_confirmation("PMDG 737 and Fenix A320 navdatas will be installed. Do you continue?")
    elif checked == [1, 0, 1]:
        install_confirmation("MSFS Native and Fenix A320 navdatas will be installed. Do you continue?")
    elif checked == [1, 1, 1]:
        install_confirmation("All contents will be installed. Do you continue?")
    else:
        tkinter.Tk().withdraw()
        tkinter.messagebox.showerror(title="Selection Error", message="Please select at least one checkbox to continue installation.")
    return 0

def install_confirmation(install_contents):
    tkinter.Tk().withdraw()
    install_yesno = tkinter.messagebox.askokcancel("Continue?", install_contents)
    if install_yesno == True:
        msfs_native_install()
        pmdg_install()
        fenix_install()
    else:
        return 0

def msfs_native_install():
    if msfs_native_update == 1:
        print("Installing MSFS Native navdata...")
    else:
        return 0

def pmdg_install():
    if pmdg_update == 1:
        print("Installing PMDG 737 navdata...")
    else:
        return 0

def fenix_install():
    if fenix_update == 1:
        print("Installing Fenix A320 navdata...")
    else:
        return 0

root = tkinter.Tk()
root.title("Navigraph Navdata Installer for MSFS")
root.geometry("300x150")
msfs_native_update = tkinter.IntVar()
pmdg_update = tkinter.IntVar()
fenix_update = tkinter.IntVar()
tkinter.Checkbutton(root, text="MSFS Native Navdata", variable=msfs_native_update).pack()
tkinter.Checkbutton(root, text="PMDG 737 Navdata", variable=pmdg_update).pack()
tkinter.Checkbutton(root, text="Fenix A320 Navdata", variable=fenix_update).pack()
tkinter.Button(root, text="Start Update", command=on_nav_update_select_button_click).pack()
tkinter.Button(root, text="Exit", command=sys.exit).pack()
tkinter.Label(root).pack()
root.mainloop()