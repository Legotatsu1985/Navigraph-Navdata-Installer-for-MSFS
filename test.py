
import glob
import os
import shutil
import sys
import tkinter
import tkinter.messagebox
from tkinter import filedialog

import rarfile

tkinter.Tk().withdraw()
tkinter.messagebox.askokcancel('Navigraph Navdata Installer for PMDG 737NG','To use this installer, you need to download the latest AIRAC Navdata from SimPlaza. Select the archive file you downloaded in next dialog.')

pmdg_nav_rar = filedialog.askopenfilename(filetypes=[('RAR Archive file','*.rar')], initialdir=os.path.abspath('.'), title="Select the latest Navigraph AIRAC archive file.(Navdata Installers)")
print(pmdg_nav_rar)

