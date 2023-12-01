
import glob
import os
import shutil
import sys
import tkinter
import tkinter.messagebox
from tkinter import filedialog

import rarfile

def get_msfs_opt_file():
    if glob.glob(r'C:\Users\*\AppData\Local\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache\UserCfg.opt'):
        for msfs_opt_file in glob.glob(r'C:\Users\*\AppData\Local\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache\UserCfg.opt'):
            print("UserCfg.opt found " + msfs_opt_file + "(MS Store Version)")
            get_msfs_installed_path(msfs_opt_file)
    elif glob.glob(r'C:\Users\*\AppData\Roaming\Microsoft Flight Simulator\UserCfg.opt'):
        for msfs_opt_file in glob.glob(r'C:\Users\*\AppData\Roaming\Microsoft Flight Simulator\UserCfg.opt'):
            print("UserCfg.opt found " + msfs_opt_file + "(Steam Version)")
            get_msfs_installed_path(msfs_opt_file)
    else:
        tkinter.Tk().withdraw()
        tkinter.messagebox.showerror('Navigraph Navdata Installer','Cannot find the file "UserCfg.opt". Please select the folder contains "UserCfg.opt" file in next dialog.')
        msfs_opt_file = filedialog.askdirectory(initialdir=os.path.abspath('.'), title='Please select the folder contains "UserCfg.opt" file.')


def get_msfs_installed_path(msfs_opt_file):
    f = open(msfs_opt_file, "r")
    alltxt = f.readlines()
    f.close()
    MSFSpathL = len(alltxt)
    MSFSpathF = alltxt[MSFSpathL-1].strip()
    MSFSpathH = MSFSpathF.replace("InstalledPackagesPath ", "")
    MSFSpath = MSFSpathH.strip('"')
    print("MSFS Installed Path = " + MSFSpath)
    return MSFSpath

get_msfs_opt_file()