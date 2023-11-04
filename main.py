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

    print("Decompressing file. Please wait... (It may be taking a long time. Please be patience...)")

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
else:
    sys.exit()

tkinter.Tk().withdraw()
if tkinter.messagebox.askokcancel('Navigraph Navdata Installer for PMDG 737NG','To use this installer, you need to download the latest AIRAC Navdata from SimPlaza. Select the archive file you downloaded in next dialog.') == True:
    pmdg_nav_rar = filedialog.askopenfilename(filetypes=[('RAR Archive file','*.rar')], initialdir=os.path.abspath('.'), title="Select the latest Navigraph AIRAC archive file.(Navdata Installers)")
    
    pmdg_nav_output_ph1 = r".\pmdg_nav_output_ph1"
    pmdg_nav_output_ph2 = r".\pmdg_nav_output_ph2"
    pmdg_nav_NavData = pmdg_nav_output_ph2 + r".\NavData"
    pmdg_nav_SidStars = pmdg_nav_output_ph2 + r".\SidStars"
    pmdg_config_route_736 = msfs_community + r".\pmdg-aircraft-736\Config"
    pmdg_config_route_737 = msfs_community + r".\pmdg-aircraft-737\Config"
    pmdg_config_route_738 = msfs_community + r".\pmdg-aircraft-738\Config"
    pmdg_config_route_739 = msfs_community + r".\pmdg-aircraft-739\Config"

    print("Decompressing file. Please wait... (It may be taking a long time. Please be patience...)")
    
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
    
    print("Installing Navdata...")
    if os.path.exists(msfs_community + r".\pmdg-aircraft-736"):
        print("PMDG B736 Found" + (msfs_community + r".\pmdg-aircraft-736"))
        shutil.rmtree(pmdg_config_route_736 + r".\NavData")
        
        if os.path.exists(pmdg_config_route_736 + r".\SidStars"):
            shutil.rmtree(pmdg_config_route_736 + r".\SidStars")
        elif os.path.exists(pmdg_config_route_736 + r".\SIDSTARS"):
            shutil.rmtree(pmdg_config_route_736 + r".\SIDSTARS")
        
        shutil.move(pmdg_nav_NavData, pmdg_config_route_736)
        shutil.move(pmdg_nav_SidStars, pmdg_config_route_736)
    else:
        print("PMDG B736 Not found in your community folder. We will skip this nav update.")
    
    if os.path.exists(msfs_community + r".\pmdg-aircraft-737"):
        print("PMDG B737 Found" + (msfs_community + r".\pmdg-aircraft-737"))
        shutil.rmtree(pmdg_config_route_737 + r".\NavData")
        
        if os.path.exists(pmdg_config_route_737 + r".\SidStars"):
            shutil.rmtree(pmdg_config_route_737 + r".\SidStars")
        elif os.path.exists(pmdg_config_route_737 + r".\SIDSTARS"):
            shutil.rmtree(pmdg_config_route_737 + r".\SIDSTARS")
        
        shutil.move(pmdg_nav_NavData, pmdg_config_route_737)
        shutil.move(pmdg_nav_SidStars, pmdg_config_route_737)
    else:
        print("PMDG B737 Not found in your community folder. We will skip this nav update.")
    
    if os.path.exists(msfs_community + r".\pmdg-aircraft-738"):
        print("PMDG B738 Found" + (msfs_community + r".\pmdg-aircraft-738"))
        shutil.rmtree(pmdg_config_route_738 + r".\NavData")
        
        if os.path.exists(pmdg_config_route_738 + r".\SidStars"):
            shutil.rmtree(pmdg_config_route_738 + r".\SidStars")
        elif os.path.exists(pmdg_config_route_738 + r".\SIDSTARS"):
            shutil.rmtree(pmdg_config_route_738 + r".\SIDSTARS")
        
        shutil.move(pmdg_nav_NavData, pmdg_config_route_738)
        shutil.move(pmdg_nav_SidStars, pmdg_config_route_738)
    else:
        print("PMDG B738 Not found in your community folder. We will skip this nav update.")
    
    if os.path.exists(msfs_community + r".\pmdg-aircraft-739"):
        print("PMDG B739 Found" + (msfs_community + r".\pmdg-aircraft-739"))
        shutil.rmtree(pmdg_config_route_739 + r".\NavData")
        
        if os.path.exists(pmdg_config_route_739 + r".\SidStars"):
            shutil.rmtree(pmdg_config_route_739 + r".\SidStars")
        elif os.path.exists(pmdg_config_route_739 + r".\SIDSTARS"):
            shutil.rmtree(pmdg_config_route_739 + r".\SIDSTARS")
        
        shutil.move(pmdg_nav_NavData, pmdg_config_route_739)
        shutil.move(pmdg_nav_SidStars, pmdg_config_route_739)
    else:
        print("PMDG B739 Not found in your community folder. We will skip this nav update.")