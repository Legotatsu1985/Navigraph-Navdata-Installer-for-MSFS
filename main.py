import glob
import os
import shutil
import sys
import tkinter
import tkinter.messagebox
from tkinter import filedialog

import rarfile

def on_nav_install_select_button_click():
    checked = [msfs_native_checkbox.get(), pmdg_checkbox.get(), fenix_checkbox.get()]
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
    if tkinter.messagebox.askokcancel("Continue?", install_contents) == True:
        msfs_native_checkbutton["state"] = "disable"
        pmdg_checkbutton["state"] = "disable"
        fenix_checkbutton["state"] = "disable"
        install_button["state"] = "disable"
        exit_button["state"] = "disable"
        msfs_native_install()
        pmdg_install()
        fenix_install()
        tkinter.Tk().withdraw()
        tkinter.messagebox.showinfo("Complete", "All installation complete.")
        sys.exit()
    else:
        return 0

def msfs_native_install():
    if msfs_native_checkbox.get() == 1:
        msfs_native_nav_output = r".\msfs_native_nav_output" #引数定義（ナビデータ一時展開先フォルダー）
        #↓ナビデータ一時解凍先フォルダーが存在する場合は削除↓
        if os.path.exists(msfs_native_nav_output):
            shutil.rmtree(msfs_native_nav_output)
        
        #↓MSFS2020本体専用ナビデータRARファイル選択ダイアログ↓
        tkinter.Tk().withdraw()
        if tkinter.messagebox.askokcancel('Navigraph Navdata Installer for MSFS','To use this installer, you need to download the latest AIRAC Navdata from SimPlaza. Select the archive file you downloaded in next dialog. File example: "navigraph-navdata-msfs2020-airac-cycle-2310-rev-1.rar"') == True:
            msfs_native_nav_rar = filedialog.askopenfilename(filetypes=[('RAR Archive file','*.rar')], initialdir=os.path.abspath('.'), title="Select the latest Navigraph AIRAC archive file.(MSFS Native)")
            msfs_native_nav_rar_basename = os.path.basename(msfs_native_nav_rar)
            if 'navigraph-navdata-msfs2020-airac-cycle-' in msfs_native_nav_rar_basename:
            
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
                    tkinter.messagebox.showerror('Navigraph Navdata Installer','Cannot find the file "UserCfg.opt". Please select the folder contains "UserCfg.opt" file in next dialog.')
                    msfs_package = filedialog.askdirectory(initialdir=os.path.abspath('.'), title='Please select the folder contains "UserCfg.opt" file.')

                shutil.move(r'.\msfs_native_nav_output\Content.xml', msfs_package)#「Content.xml」ファイルをコピー
                shutil.rmtree(msfs_native_nav_output)#ナビデータ一時解凍先フォルダーを消去
                print("Install complete.")
            else:
                tkinter.Tk().withdraw()
                tkinter.messagebox.showerror("The file you selected is not valid as navdata. Please restart this application and reselect a file.")
                sys.exit()
        else:
            sys.exit()
    else:
        return

def pmdg_install():
    if pmdg_checkbox.get() == 1:
        tkinter.Tk().withdraw()
        if tkinter.messagebox.askokcancel('Navigraph Navdata Installer for PMDG 737NG','To use this installer, you need to download the latest AIRAC Navdata from SimPlaza. Select the archive file you downloaded in next dialog. File example: "navigraph-navdata-installer-airac-cycle-2310.rar"') == True:
            pmdg_nav_rar = filedialog.askopenfilename(filetypes=[('RAR Archive file','*.rar')], initialdir=os.path.abspath('.'), title="Select the latest Navigraph AIRAC archive file.(Navdata Installers)")
            pmdg_nav_rar_basename = os.path.basename(pmdg_nav_rar)
            if'navigraph-navdata-installers-airac-cycle-' in pmdg_nav_rar_basename:
                
                pmdg_nav_output_ph1 = r".\pmdg_nav_output_ph1" #解凍段階1
                pmdg_nav_output_ph2 = r".\pmdg_nav_output_ph2" #解凍段階2(最終完了)
                pmdg_nav_NavData = pmdg_nav_output_ph2 + r".\NavData" #解凍先NavDataのフルパス
                pmdg_nav_SidStars = pmdg_nav_output_ph2 + r".\SidStars" #解凍先SidStarsのフルパス
                pmdg_config_route_736 = msfs_community + r".\pmdg-aircraft-736\Config"
                pmdg_config_route_737 = msfs_community + r".\pmdg-aircraft-737\Config"
                pmdg_config_route_738 = msfs_community + r".\pmdg-aircraft-738\Config"
                pmdg_config_route_739 = msfs_community + r".\pmdg-aircraft-739\Config"

                print("Decompressing file. Please wait... (It may be taking a long time. Please be patience...)")
            
                if os.path.exists(pmdg_nav_output_ph1):
                    shutil.rmtree(pmdg_nav_output_ph1)

                if os.path.exists(pmdg_nav_output_ph2):
                    shutil.rmtree(pmdg_nav_output_ph2)
                
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
                    print("PMDG B736 Found",(msfs_community + r".\pmdg-aircraft-736"))
                    shutil.rmtree(pmdg_config_route_736 + r".\NavData")
                
                    if os.path.exists(pmdg_config_route_736 + r".\SidStars"):
                        shutil.rmtree(pmdg_config_route_736 + r".\SidStars")
                    elif os.path.exists(pmdg_config_route_736 + r".\SIDSTARS"):
                        shutil.rmtree(pmdg_config_route_736 + r".\SIDSTARS")
                
                    shutil.copytree(pmdg_nav_NavData, pmdg_config_route_736 + r".\NavData")
                    shutil.copytree(pmdg_nav_SidStars, pmdg_config_route_736 + r".\SidStars")
                else:
                    print("PMDG B736 Not found in your community folder. We will skip this nav update.")
            
                if os.path.exists(msfs_community + r".\pmdg-aircraft-737"):
                    print("PMDG B737 Found",(msfs_community + r".\pmdg-aircraft-737"))
                    shutil.rmtree(pmdg_config_route_737 + r".\NavData")
                
                    if os.path.exists(pmdg_config_route_737 + r".\SidStars"):
                        shutil.rmtree(pmdg_config_route_737 + r".\SidStars")
                    elif os.path.exists(pmdg_config_route_737 + r".\SIDSTARS"):
                        shutil.rmtree(pmdg_config_route_737 + r".\SIDSTARS")
                
                    shutil.copytree(pmdg_nav_NavData, pmdg_config_route_737 + r".\NavData")
                    shutil.copytree(pmdg_nav_SidStars, pmdg_config_route_737 + r".\SidStars")
                else:
                    print("PMDG B737 Not found in your community folder. We will skip this nav update.")
            
                if os.path.exists(msfs_community + r".\pmdg-aircraft-738"):
                    print("PMDG B738 Found",(msfs_community + r".\pmdg-aircraft-738"))
                    shutil.rmtree(pmdg_config_route_738 + r".\NavData")
                
                    if os.path.exists(pmdg_config_route_738 + r".\SidStars"):
                        shutil.rmtree(pmdg_config_route_738 + r".\SidStars")
                    elif os.path.exists(pmdg_config_route_738 + r".\SIDSTARS"):
                        shutil.rmtree(pmdg_config_route_738 + r".\SIDSTARS")
                
                    shutil.copytree(pmdg_nav_NavData, pmdg_config_route_738 + r".\NavData")
                    shutil.copytree(pmdg_nav_SidStars, pmdg_config_route_738 + r".\SidStars")
                else:
                    print("PMDG B738 Not found in your community folder. We will skip this nav update.")
            
                if os.path.exists(msfs_community + r".\pmdg-aircraft-739"):
                    print("PMDG B739 Found",(msfs_community + r".\pmdg-aircraft-739"))
                    shutil.rmtree(pmdg_config_route_739 + r".\NavData")
                
                    if os.path.exists(pmdg_config_route_739 + r".\SidStars"):
                        shutil.rmtree(pmdg_config_route_739 + r".\SidStars")
                    elif os.path.exists(pmdg_config_route_739 + r".\SIDSTARS"):
                        shutil.rmtree(pmdg_config_route_739 + r".\SIDSTARS")
                
                    shutil.copytree(pmdg_nav_NavData, pmdg_config_route_739 + r".\NavData")
                    shutil.copytree(pmdg_nav_SidStars, pmdg_config_route_739 + r".\SidStars")
                else:
                    print("PMDG B739 Not found in your community folder. We will skip this nav update.")
                
                shutil.rmtree(pmdg_nav_output_ph2)
                print("Install complete.")
            else:
                tkinter.Tk().withdraw()
                tkinter.messagebox.showerror("The file you selected is not valid for PMDG navdata. Please restart this application and reselect a file.")
                sys.exit()
        else:
            sys.exit()
    else:
        return

def fenix_install():
    if fenix_checkbox.get() == 1:
        tkinter.Tk().withdraw()
        if tkinter.messagebox.askokcancel('Navigraph Navdata Installer for Fenix A320','To use this installer, you need to download the latest AIRAC Navdata from SimPlaza. Select the archive file you downloaded in next dialog. File example: "navigraph-navdata-installer-airac-cycle-2310.rar"') == True:
            fenix_nav_rar = filedialog.askopenfilename(filetypes=[('RAR Archive file', '*.rar')], initialdir=os.path.abspath('.'), title="Select the latest Navigraph AIRAC archive file.(Navdata Installers)")
            fenix_nav_rar_basename = os.path.basename(fenix_nav_rar)
            fenix_nav_install_path = r"C:\ProgramData\Fenix\Navdata" #Fenix A320 ナビデータのインストール先フォルダー
            
            GREEN = '\033[33m'
            END = '\033[0m'
            
            if 'navigraph-navdata-installers-airac-cycle-' in fenix_nav_rar_basename:
                if os.path.exists(fenix_nav_install_path):
                    fenix_nav_output_ph1 = r".\fenix_nav_output_ph1" #解凍段階1
                    fenix_nav_output_ph2 = r".\fenix_nav_output_ph2" #解凍段階2(最終完了)
                    
                    print("Decompressing file. Please wait... (It may be taking a long time. Please be patience...)")
                    if os.path.exists(fenix_nav_output_ph1):
                        shutil.rmtree(fenix_nav_output_ph1)
                    if os.path.exists(fenix_nav_output_ph2):
                        shutil.rmtree(fenix_nav_output_ph2)
                    
                    rarfile.UNRAR_TOOL = r".\UnRAR.exe"
                    
                    rarfile.RarFile(fenix_nav_rar).extractall("fenix_nav_output_ph1")
                    
                    for fenix_nav_final_output in glob.glob(r".\fenix_nav_output_ph1\Navigraph AIRAC *\fenix_a320_*.rar"):
                        print(fenix_nav_final_output)
                    
                    rarfile.RarFile(fenix_nav_final_output).extractall("fenix_nav_output_ph2")
                    
                    shutil.rmtree(fenix_nav_output_ph1)
                    
                    print("Decompression complete")
                    
                    print("Installing Navdata...")
                    if os.path.isfile(fenix_nav_install_path + r".\cycle.json"):
                        os.remove(fenix_nav_install_path + r".\cycle.json")
                        print(GREEN + 'Existing "cycle.json" deleted.' + END)
                    shutil.move(fenix_nav_output_ph2 + r".\Navdata\cycle.json", fenix_nav_install_path)
                    print(GREEN + 'Copied "cycle.json"' + END)
                    if os.path.isfile(fenix_nav_install_path + r".\cycle_info.txt"):
                        os.remove(fenix_nav_install_path + r".\cycle_info.txt")
                        print(GREEN + 'Existing "cycle_info.txt" deleted.' + END)
                    shutil.move(fenix_nav_output_ph2 + r".\Navdata\cycle_info.txt", fenix_nav_install_path)
                    print(GREEN + 'Copied "cycle_info.txt"' + END)
                    if os.path.isfile(fenix_nav_install_path + r".\nd.db3"):
                        os.remove(fenix_nav_install_path + r".\nd.db3")
                        print(GREEN + 'Existing "nd.db3" deleted.' + END)
                    shutil.move(fenix_nav_output_ph2 + r".\Navdata\nd.db3", fenix_nav_install_path)
                    print(GREEN + 'Copied "nd.db3"' + END)
                    shutil.rmtree(fenix_nav_output_ph2)
                    print("Install complete.")
                else:
                    tkinter.Tk().withdraw()
                    tkinter.messagebox.showerror("Is the Fenix A320 installed?", 'Could not find the folder "C:\\ProgramData\\Fenix\\Navdata". It seems Fenix A320 is not installed in this computer.')
                    sys.exit()
            else:
                tkinter.Tk().withdraw()
                tkinter.messagebox.showerror("The file you selected is not valid for Fenix A320 navdata. Please restart this application and reselect a file.")
                sys.exit()
        else:
            sys.exit()
    else:
        return

root = tkinter.Tk()
root.title("Navigraph Navdata Installer for MSFS")
root.geometry("500x250")
#↓Communityフォルダー選択ダイアログ↓
tkinter.Tk().withdraw()
if tkinter.messagebox.askokcancel('Navigraph Navdata Installer for MSFS','Select the MSFS Community folder in next dialog.') == True:
    msfs_community = filedialog.askdirectory(initialdir=os.path.abspath('.'), title="Select the MSFS Community folder")
    if msfs_community == "":
        tkinter.Tk().withdraw()
        tkinter.messagebox.showerror("Error!", "An expection has been occured. Please restart the application.")
        sys.exit()
else:
    sys.exit()
tkinter.Label(root, justify="center", text='Slelect the checkbox you want to install, then press "Install".').pack()
tkinter.Label(root, justify="left", text="Your Community folder path: " + msfs_community).pack()
msfs_native_checkbox = tkinter.IntVar()
pmdg_checkbox = tkinter.IntVar()
fenix_checkbox = tkinter.IntVar()
msfs_native_checkbutton = tkinter.Checkbutton(root, text="MSFS Native Navdata", variable=msfs_native_checkbox)
msfs_native_checkbutton.pack()
pmdg_checkbutton = tkinter.Checkbutton(root, text="PMDG 737 Navdata", variable=pmdg_checkbox)
pmdg_checkbutton.pack()
fenix_checkbutton = tkinter.Checkbutton(root, text="Fenix A320 Navdata", variable=fenix_checkbox)
fenix_checkbutton.pack()
install_button = tkinter.Button(root, text="Install", command=on_nav_install_select_button_click)
install_button.pack()
exit_button = tkinter.Button(root, text="Exit", command=sys.exit)
exit_button.pack()
info_label = tkinter.Label(root, text="Made by Legotatsu1985 with Tkinter", fg="blue", anchor=tkinter.S)
info_label.pack()
version_label = tkinter.Label(root, text="v0.1.3", anchor=tkinter.SE)
version_label.pack()
root.mainloop()