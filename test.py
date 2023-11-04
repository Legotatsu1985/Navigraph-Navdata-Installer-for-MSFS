
import glob
import os
import shutil
import sys
import tkinter
import tkinter.messagebox
from tkinter import filedialog

import rarfile

pmdg_nav_output_ph1 = r".\pmdg_nav_output_ph1"
pmdg_nav_output_ph2 = r".\pmdg_nav_output_ph2"

if os.path.exists(pmdg_nav_output_ph1):
    shutil.rmtree(pmdg_nav_output_ph1)

if os.path.exists(pmdg_nav_output_ph2):
    shutil.rmtree(pmdg_nav_output_ph2)

msfs_community = filedialog.askdirectory(initialdir=os.path.abspath('.'), title="Select the MSFS Community folder")

tkinter.messagebox.askokcancel('Navigraph Navdata Installer for PMDG 737NG','To use this installer, you need to download the latest AIRAC Navdata from SimPlaza. Select the archive file you downloaded in next dialog.')
pmdg_nav_rar = filedialog.askopenfilename(filetypes=[('RAR Archive file','*.rar')], initialdir=os.path.abspath('.'), title="Select the latest Navigraph AIRAC archive file.(Navdata Installers)")

print("Decompressing file. Please wait...")

rarfile.UNRAR_TOOL=r".\UnRAR.exe"

rf2 = rarfile.RarFile(pmdg_nav_rar)
rf2.extractall("pmdg_nav_output_ph1")

for pmdg_nav_final_output in glob.glob(r".\pmdg_nav_output_ph1\Navigraph AIRAC *\pmdg_737_msfs_*.rar"):
    print(pmdg_nav_final_output)

rf3 = rarfile.RarFile(pmdg_nav_final_output)
rf3.extractall("pmdg_nav_output_ph2")

shutil.rmtree(pmdg_nav_output_ph1)

print("Decompression complete.")