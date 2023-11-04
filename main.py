import glob
import os
import shutil
import sys
import tkinter
import tkinter.messagebox
from tkinter import filedialog

import rarfile


msfs_native_nav_output = r".\msfs_native_nav_output" #引数定義（ナビデータ一時展開先フォルダー）

#↓ナビデータ一時解凍先フォルダーが存在する場合は削除↓
if os.path.exists(msfs_native_nav_output):
    shutil.rmtree(msfs_native_nav_output)

#↓Communityフォルダー選択ダイアログ↓
tkinter.Tk().withdraw()
if tkinter.messagebox.askokcancel('Navigraph Navdata Installer for MSFS','Select the MSFS Community folder in next dialog.') == False:
    sys.exit()

msfs_community = filedialog.askdirectory(initialdir=os.path.abspath('.'), title="Select the MSFS Community folder")

#↓MSFS2020本体専用ナビデータRARファイル選択ダイアログ↓
tkinter.Tk().withdraw()
if tkinter.messagebox.askokcancel('Navigraph Navdata Installer for MSFS','To use this installer, you need to download the latest AIRAC Navdata from SimPlaza. Select the archive file you downloaded in next dialog.') == True:
    msfs_native_nav_rar = filedialog.askopenfilename(filetypes=[('RAR Archive file','*.rar')], initialdir=os.path.abspath('.'), title="Select the latest Navigraph AIRAC archive file.(MSFS Native)")

    print("Decompressing file. Please wait...")

    rarfile.UNRAR_TOOL=r".\UnRAR.exe"#解凍ツール選択（同フォルダに格納済み）

    rf = rarfile.RarFile(msfs_native_nav_rar)#ナビデータ解凍
    rf.extractall("msfs_native_nav_output")

    print("Decompression complete.")

    print("Installing Navdata...")#Communityフォルダーにすでにナビデータが存在する場合は削除
    if os.path.exists(msfs_community + r".\navigraph-navdata"):
        shutil.rmtree(msfs_community + r".\navigraph-navdata")

    if os.path.exists(msfs_community + r".\navigraph-navdata-base"):
        shutil.rmtree(msfs_community + r".\navigraph-navdata-base")

    shutil.move(r".\msfs_native_nav_output\navigraph-navdata", msfs_community)#Communityフォルダーにディレクトリを移動
    shutil.move(r".\msfs_native_nav_output\navigraph-navdata-base", msfs_community)

    print('Copying "Content.xml"...')#「UserCfg.opt」ファイルがあるディレクトリを検索（MSストア版とSteam版）
    if glob.glob(r'C:\Users\*\AppData\Local\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache\UserCfg.opt'):
        for msfs_package in glob.glob(r'C:\Users\*\AppData\Local\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache\Content.xml'):
            print(msfs_package)
    elif glob.glob(r'C:\Users\*\AppData\Roaming\Microsoft Flight Simulator\UserCfg.opt'):
        for msfs_package in glob.glob(r'C:\Users\*\AppData\Roaming\Microsoft Flight Simulator\Content.xml'):
            print(msfs_package)
    else:
        tkinter.Tk().withdraw()
        tkinter.messagebox.showinfo('Navigraph Navdata Installer','Cannot find the file "UserCfg.opt". Please select the folder contains "UserCfg.opt" file in next dialog.')
        msfs_package = filedialog.askdirectory(initialdir=os.path.abspath('.'), title='Please select the folder contains "UserCfg.opt" file.')

    shutil.move(r'.\msfs_native_nav_output\Content.xml', msfs_package)#「Content.xml」ファイルをコピー
    shutil.rmtree(msfs_native_nav_output)#ナビデータ一時解凍先フォルダーを消去
    print("Install complete.")
elif tkinter.messagebox.askokcancel('Navigraph Navdata Installer for PMDG 737NG','To use this installer, you need to download the latest AIRAC Navdata from SimPlaza. Select the archive file you downloaded in next dialog.') == True:
    pmdg_nav_rar = filedialog.askopenfilename(filetypes=[('RAR Archive file','*.rar')], initialdir=os.path.abspath('.'), title="Select the latest Navigraph AIRAC archive file.(Navdata Installers)")
    
    print("Decompressing file. Please wait...")
    
    rarfile.UNRAR_TOOL=r".\UnRAR.exe"

    rf2 = rarfile.RarFile(pmdg_nav_rar)
    rf2.extractall("pmdg_nav_output_ph1")

    rf3 = rarfile.RarFile(r".\pmdg_nav_output_ph1\Navigraph AIRAC 2310\pmdg_737_msfs_2310.rar")
    rf3.extractall("pmdg_nav_output_ph2")
    
    shutil.rmtree(r".\pmdg_nav_output_ph1")
    
    print("Decompression complete.")
    
    print("Installing Navdata...")
    if os.path.exists(msfs_community + r".\pmdg-aircraft-736"):
        shutil.rmtree(msfs_community + r".\pmdg-aircraft-736\Config\NavData")
        shutil.rmtree(msfs_community + r".\pmdg-aircraft-736\Config\SidStars")
    
    if os.path.exists(msfs_community + r".\pmdg-aircraft-737"):
        shutil.rmtree(msfs_community + r".\pmdg-aircraft-737\Config\NavData")
        shutil.rmtree(msfs_community + r".\pmdg-aircraft-737\Config\SidStars")
    
    if os.path.exists(msfs_community + r".\pmdg-aircraft-738"):
        shutil.rmtree(msfs_community + r".\pmdg-aircraft-738\Config\NavData")
        shutil.rmtree(msfs_community + r".\pmdg-aircraft-738\Config\SidStars")
    
    if os.path.exists(msfs_community + r".\pmdg-aircraft-739"):
        shutil.rmtree(msfs_community + r".\pmdg-aircraft-739\Config\NavData")
        shutil.rmtree(msfs_community + r".\pmdg-aircraft-739\Config\SidStars")