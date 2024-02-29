import datetime
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
            print("UserCfg.opt found: " + msfs_opt_file + " (MS Store Version)")
            get_msfs_installed_path(msfs_opt_file)
    elif glob.glob(r'C:\Users\*\AppData\Roaming\Microsoft Flight Simulator\UserCfg.opt'):
        for msfs_opt_file in glob.glob(r'C:\Users\*\AppData\Roaming\Microsoft Flight Simulator\UserCfg.opt'):
            print("UserCfg.opt found: " + msfs_opt_file + " (Steam Version)")
            get_msfs_installed_path(msfs_opt_file)
    else:
        tkinter.Tk().withdraw()
        tkinter.messagebox.showerror('Navigraph Navdata Installer','Cannot find the file "UserCfg.opt". Please select the MSFS folder contains "UserCfg.opt" file in next dialog.')
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
    check_nav_version(MSFSpath)
    return MSFSpath

def check_nav_version(MSFSpath):
    msfs_community = MSFSpath + r"\Community"
    #MSFS Native Navdata Version Check
    if os.path.exists(msfs_community + r"\navigraph-navdata-base"):
        cycle_file_path = msfs_community + r"\navigraph-navdata-base\ContentInfo\navigraph-navdata\cycle.json"
        with open(cycle_file_path) as f:
            lines = f.read().split(',')
        
        #Get current AIRAC Version of MSFS Native navdata
        get_msfs_current_airac_fromlist = lines[3]
        msfs_current_airac_number = get_msfs_current_airac_fromlist[9:13]
        get_msfs_current_airac_rev_fromlist = lines[4]
        msfs_current_airac_rev_number = get_msfs_current_airac_rev_fromlist[11:12]
        msfs_native_nav_version_raw_txt = "AIRAC Cycle " + msfs_current_airac_number + " rev." + msfs_current_airac_rev_number
        
        #Get current AIRAC Start date
        get_airac_start_date_fromlist = lines[5]
        raw_airac_start_date = get_airac_start_date_fromlist[13:21]
        current_airac_start_year = raw_airac_start_date[:4]
        current_airac_start_month = raw_airac_start_date[4:6]
        current_airac_start_day = raw_airac_start_date[6:]
        current_airac_start_time = datetime.date(year=int(current_airac_start_year), month=int(current_airac_start_month), day=int(current_airac_start_day))

        #Get current AIRAC End date
        get_airac_end_date_fromlist = lines[6]
        raw_airac_end_date = get_airac_end_date_fromlist[11:19]
        current_airac_end_year = raw_airac_end_date[:4]
        current_airac_end_month = raw_airac_end_date[4:6]
        current_airac_end_day = raw_airac_end_date[6:]
        current_airac_end_time = datetime.date(year=int(current_airac_end_year), month=int(current_airac_end_month), day=int(current_airac_end_day))
        
        #Check airac validation
        current_date = datetime.date.today()
        if current_date >= current_airac_start_time:
            if current_date <= current_airac_end_time:
                print("MSFS Native navdata version = " + msfs_native_nav_version_raw_txt + " (Valid)")
                msfs_native_nav_version.config(text=msfs_native_nav_version_raw_txt, fg="green")
            else:
                print("MSFS Native navdata version = " + msfs_native_nav_version_raw_txt + " (Invalid)")
                msfs_native_nav_version.config(text=msfs_native_nav_version_raw_txt + " (Outdated)", fg="red")
        else:
            print("MSFS Native navdata version = " + msfs_native_nav_version_raw_txt + " (Invalid)")
            msfs_native_nav_version.config(text=msfs_native_nav_version_raw_txt + " (Outdated)", fg="red")
    else:
        msfs_native_nav_version.config(text="Navdata not detected", fg="red")
    
    #PMDG 737 Navdata Version Check (All varient)
    if os.path.exists(msfs_community + r"\pmdg-aircraft-739"):
        check_nav_version_pmdg(msfs_community, r"\pmdg-aircraft-739")
    elif os.path.exists(msfs_community + r"\pmdg-aircraft-738"):
        check_nav_version_pmdg(msfs_community, r"\pmdg-aircraft-738")
    elif os.path.exists(msfs_community + r"\pmdg-aircraft-737"):
        check_nav_version_pmdg(msfs_community, r"\pmdg-aircraft-737")
    elif os.path.exists(msfs_community + r"\pmdg-aircraft-736"):
        check_nav_version_pmdg(msfs_community, r"\pmdg-aircraft-736")
    else:
        pmdg_nav_version.config(text="Navdata not detected", fg="red")
    
    #Fenix A320 Navdata Version Check
    fenix_nav_install_path = r"C:\ProgramData\Fenix\Navdata"
    if os.path.isfile(msfs_community + r"\fnx-aircraft-320\SimObjects\Airplanes\FNX_320_CFM\aircraft.cfg"):
        if os.path.exists(fenix_nav_install_path):
            with open(fenix_nav_install_path + r"\cycle_info.txt") as f:
                lines = f.read().splitlines()

            get_line_fenix_airac_cycle = lines[0]
            get_line_fenix_airac_rev = lines[1]
            get_line_fenix_airac_valid_date = lines[2]

            fenix_airac_cycle_number = get_line_fenix_airac_cycle[17:21] #AIRAC Cycle Number
            fenix_airac_rev_number = get_line_fenix_airac_rev[17:18] #AIRAC Cycle Revision Number
            fenix_airac_valid_date = get_line_fenix_airac_valid_date[17:42] #AIRAC Cycle Valid date

            fenix_airac_valid_start_year = fenix_airac_valid_date[7:11]

            fenix_airac_valid_start_month_raw = fenix_airac_valid_date[3:6]
            if fenix_airac_valid_start_month_raw == "JAN":
                fenix_airac_valid_start_month = fenix_airac_valid_start_month_raw.replace("JAN", "01")
            elif fenix_airac_valid_start_month_raw == "FEB":
                fenix_airac_valid_start_month = fenix_airac_valid_start_month_raw.replace("FEB", "02")
            elif fenix_airac_valid_start_month_raw == "MAR":
                fenix_airac_valid_start_month = fenix_airac_valid_start_month_raw.replace("MAR", "03")
            elif fenix_airac_valid_start_month_raw == "APR":
                fenix_airac_valid_start_month = fenix_airac_valid_start_month_raw.replace("APR", "04")
            elif fenix_airac_valid_start_month_raw == "MAY":
                fenix_airac_valid_start_month = fenix_airac_valid_start_month_raw.replace("MAY", "05")
            elif fenix_airac_valid_start_month_raw == "JUN":
                fenix_airac_valid_start_month = fenix_airac_valid_start_month_raw.replace("JUN", "06")
            elif fenix_airac_valid_start_month_raw == "JUL":
                fenix_airac_valid_start_month = fenix_airac_valid_start_month_raw.replace("JUL", "07")
            elif fenix_airac_valid_start_month_raw == "AUG":
                fenix_airac_valid_start_month = fenix_airac_valid_start_month_raw.replace("AUG", "08")
            elif fenix_airac_valid_start_month_raw == "SEP":
                fenix_airac_valid_start_month = fenix_airac_valid_start_month_raw.replace("SEP", "09")
            elif fenix_airac_valid_start_month_raw == "OCT":
                fenix_airac_valid_start_month = fenix_airac_valid_start_month_raw.replace("OCT", "10")
            elif fenix_airac_valid_start_month_raw == "NOV":
                fenix_airac_valid_start_month = fenix_airac_valid_start_month_raw.replace("NOV", "11")
            elif fenix_airac_valid_start_month_raw == "DEC":
                fenix_airac_valid_start_month = fenix_airac_valid_start_month_raw.replace("DEC", "12")

            fenix_airac_valid_start_day = fenix_airac_valid_date[:2]

            fenix_airac_valid_end_year = fenix_airac_valid_date[21:]

            fenix_airac_valid_end_month_raw = fenix_airac_valid_date[17:20]
            if fenix_airac_valid_end_month_raw == "JAN":
                fenix_airac_valid_end_month = fenix_airac_valid_end_month_raw.replace("JAN", "01")
            elif fenix_airac_valid_end_month_raw == "FEB":
                fenix_airac_valid_end_month = fenix_airac_valid_end_month_raw.replace("FEB", "02")
            elif fenix_airac_valid_end_month_raw == "MAR":
                fenix_airac_valid_end_month = fenix_airac_valid_end_month_raw.replace("MAR", "03")
            elif fenix_airac_valid_end_month_raw == "APR":
                fenix_airac_valid_end_month = fenix_airac_valid_end_month_raw.replace("APR", "04")
            elif fenix_airac_valid_end_month_raw == "MAY":
                fenix_airac_valid_end_month = fenix_airac_valid_end_month_raw.replace("MAY", "05")
            elif fenix_airac_valid_end_month_raw == "JUN":
                fenix_airac_valid_end_month = fenix_airac_valid_end_month_raw.replace("JUN", "06")
            elif fenix_airac_valid_end_month_raw == "JUL":
                fenix_airac_valid_end_month = fenix_airac_valid_end_month_raw.replace("JUL", "07")
            elif fenix_airac_valid_end_month_raw == "AUG":
                fenix_airac_valid_end_month = fenix_airac_valid_end_month_raw.replace("AUG", "08")
            elif fenix_airac_valid_end_month_raw == "SEP":
                fenix_airac_valid_end_month = fenix_airac_valid_end_month_raw.replace("SEP", "09")
            elif fenix_airac_valid_end_month_raw == "OCT":
                fenix_airac_valid_end_month = fenix_airac_valid_end_month_raw.replace("OCT", "10")
            elif fenix_airac_valid_end_month_raw == "NOV":
                fenix_airac_valid_end_month = fenix_airac_valid_end_month_raw.replace("NOV", "11")
            elif fenix_airac_valid_end_month_raw == "DEC":
                fenix_airac_valid_end_month = fenix_airac_valid_end_month_raw.replace("DEC", "12")

            fenix_airac_valid_end_day = fenix_airac_valid_date[14:16]

            fenix_current_airac_start_time = datetime.date(year=int(fenix_airac_valid_start_year), month=int(fenix_airac_valid_start_month), day=int(fenix_airac_valid_start_day))
            fenix_current_airac_end_time = datetime.date(year=int(fenix_airac_valid_end_year), month=int(fenix_airac_valid_end_month), day=int(fenix_airac_valid_end_day))

            current_date = datetime.date.today()
            if current_date >= fenix_current_airac_start_time:
                if current_date <= fenix_current_airac_end_time:
                    print("Fenix A320 navdata version = AIRAC Cycle " + fenix_airac_cycle_number + " rev." + fenix_airac_rev_number + " (Valid)")
                    fenix_nav_version.config(text="AIRAC Cycle " + fenix_airac_cycle_number + " rev." + fenix_airac_rev_number, fg="green")
                else:
                    print("Fenix A320 navdata version = AIRAC Cycle " + fenix_airac_cycle_number + " rev." + fenix_airac_rev_number + " (Invalid)")
                    fenix_nav_version.config(text="AIRAC Cycle " + fenix_airac_cycle_number + " rev." + fenix_airac_rev_number + " (Outdated)", fg="red")
            else:
                print("Fenix A320 navdata version = AIRAC Cycle " + fenix_airac_cycle_number + " rev." + fenix_airac_rev_number + " (Invalid)")
                fenix_nav_version.config(text="AIRAC Cycle " + fenix_airac_cycle_number + " rev." + fenix_airac_rev_number + " (Outdated)", fg="red")
        else:
            fenix_nav_version.config(text="Navdata not detected", fg="red")
    else:
        fenix_nav_version.config(text="Navdata not detected", fg="red")

def check_nav_version_pmdg(msfs_community, varient):
    pmdg_path = msfs_community + varient
    if os.path.exists(pmdg_path):
        file_path = pmdg_path + r"\Config\NavData\cycle_info.txt"
        
        with open(file_path) as f:
            lines = f.read().splitlines()

        get_line_pmdg_airac_cycle = lines[0]
        get_line_pmdg_airac_rev = lines[1]
        get_line_pmdg_airac_valid_date = lines[2]

        pmdg_airac_cycle_number = get_line_pmdg_airac_cycle[17:21] #AIRAC Cycle Number
        pmdg_airac_rev_number = get_line_pmdg_airac_rev[17:18] #AIRAC Cycle Revision Number
        pmdg_airac_valid_date = get_line_pmdg_airac_valid_date[17:42] #AIRAC Cycle Valid date

        pmdg_airac_valid_start_year = pmdg_airac_valid_date[7:11]

        pmdg_airac_valid_start_month_raw = pmdg_airac_valid_date[3:6]
        if pmdg_airac_valid_start_month_raw == "JAN":
            pmdg_airac_valid_start_month = pmdg_airac_valid_start_month_raw.replace("JAN", "01")
        elif pmdg_airac_valid_start_month_raw == "FEB":
            pmdg_airac_valid_start_month = pmdg_airac_valid_start_month_raw.replace("FEB", "02")
        elif pmdg_airac_valid_start_month_raw == "MAR":
            pmdg_airac_valid_start_month = pmdg_airac_valid_start_month_raw.replace("MAR", "03")
        elif pmdg_airac_valid_start_month_raw == "APR":
            pmdg_airac_valid_start_month = pmdg_airac_valid_start_month_raw.replace("APR", "04")
        elif pmdg_airac_valid_start_month_raw == "MAY":
            pmdg_airac_valid_start_month = pmdg_airac_valid_start_month_raw.replace("MAY", "05")
        elif pmdg_airac_valid_start_month_raw == "JUN":
            pmdg_airac_valid_start_month = pmdg_airac_valid_start_month_raw.replace("JUN", "06")
        elif pmdg_airac_valid_start_month_raw == "JUL":
            pmdg_airac_valid_start_month = pmdg_airac_valid_start_month_raw.replace("JUL", "07")
        elif pmdg_airac_valid_start_month_raw == "AUG":
            pmdg_airac_valid_start_month = pmdg_airac_valid_start_month_raw.replace("AUG", "08")
        elif pmdg_airac_valid_start_month_raw == "SEP":
            pmdg_airac_valid_start_month = pmdg_airac_valid_start_month_raw.replace("SEP", "09")
        elif pmdg_airac_valid_start_month_raw == "OCT":
            pmdg_airac_valid_start_month = pmdg_airac_valid_start_month_raw.replace("OCT", "10")
        elif pmdg_airac_valid_start_month_raw == "NOV":
            pmdg_airac_valid_start_month = pmdg_airac_valid_start_month_raw.replace("NOV", "11")
        elif pmdg_airac_valid_start_month_raw == "DEC":
            pmdg_airac_valid_start_month = pmdg_airac_valid_start_month_raw.replace("DEC", "12")

        pmdg_airac_valid_start_day = pmdg_airac_valid_date[:2]

        pmdg_airac_valid_end_year = pmdg_airac_valid_date[21:]

        pmdg_airac_valid_end_month_raw = pmdg_airac_valid_date[17:20]
        if pmdg_airac_valid_end_month_raw == "JAN":
            pmdg_airac_valid_end_month = pmdg_airac_valid_end_month_raw.replace("JAN", "01")
        elif pmdg_airac_valid_end_month_raw == "FEB":
            pmdg_airac_valid_end_month = pmdg_airac_valid_end_month_raw.replace("FEB", "02")
        elif pmdg_airac_valid_end_month_raw == "MAR":
            pmdg_airac_valid_end_month = pmdg_airac_valid_end_month_raw.replace("MAR", "03")
        elif pmdg_airac_valid_end_month_raw == "APR":
            pmdg_airac_valid_end_month = pmdg_airac_valid_end_month_raw.replace("APR", "04")
        elif pmdg_airac_valid_end_month_raw == "MAY":
            pmdg_airac_valid_end_month = pmdg_airac_valid_end_month_raw.replace("MAY", "05")
        elif pmdg_airac_valid_end_month_raw == "JUN":
            pmdg_airac_valid_end_month = pmdg_airac_valid_end_month_raw.replace("JUN", "06")
        elif pmdg_airac_valid_end_month_raw == "JUL":
            pmdg_airac_valid_end_month = pmdg_airac_valid_end_month_raw.replace("JUL", "07")
        elif pmdg_airac_valid_end_month_raw == "AUG":
            pmdg_airac_valid_end_month = pmdg_airac_valid_end_month_raw.replace("AUG", "08")
        elif pmdg_airac_valid_end_month_raw == "SEP":
            pmdg_airac_valid_end_month = pmdg_airac_valid_end_month_raw.replace("SEP", "09")
        elif pmdg_airac_valid_end_month_raw == "OCT":
            pmdg_airac_valid_end_month = pmdg_airac_valid_end_month_raw.replace("OCT", "10")
        elif pmdg_airac_valid_end_month_raw == "NOV":
            pmdg_airac_valid_end_month = pmdg_airac_valid_end_month_raw.replace("NOV", "11")
        elif pmdg_airac_valid_end_month_raw == "DEC":
            pmdg_airac_valid_end_month = pmdg_airac_valid_end_month_raw.replace("DEC", "12")

        pmdg_airac_valid_end_day = pmdg_airac_valid_date[14:16]

        pmdg_current_airac_start_time = datetime.date(year=int(pmdg_airac_valid_start_year), month=int(pmdg_airac_valid_start_month), day=int(pmdg_airac_valid_start_day))
        pmdg_current_airac_end_time = datetime.date(year=int(pmdg_airac_valid_end_year), month=int(pmdg_airac_valid_end_month), day=int(pmdg_airac_valid_end_day))

        current_date = datetime.date.today()
        if current_date >= pmdg_current_airac_start_time:
            if current_date <= pmdg_current_airac_end_time:
                print("PMDG 737 navdata version = AIRAC Cycle " + pmdg_airac_cycle_number + " rev." + pmdg_airac_rev_number + " (Valid)")
                pmdg_nav_version.config(text="AIRAC Cycle " + pmdg_airac_cycle_number + " rev." + pmdg_airac_rev_number,  fg="green")
            else:
                print("PMDG 737 navdata version = AIRAC Cycle " + pmdg_airac_cycle_number + " rev." + pmdg_airac_rev_number + " (Invalid)")
                pmdg_nav_version.config(text="AIRAC Cycle " + pmdg_airac_cycle_number + " rev." + pmdg_airac_rev_number + " (Outdated)", fg="red")
        else:
            print("PMDG 737 navdata version = AIRAC Cycle " + pmdg_airac_cycle_number + " rev." + pmdg_airac_rev_number + " (Invalid)")
            pmdg_nav_version.config(text="AIRAC Cycle " + pmdg_airac_cycle_number + " rev." + pmdg_airac_rev_number + " (Outdated)", fg="red")
    else:
        pmdg_nav_version.config(text="Navdata not detected", fg="red")

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
        msfs_native_nav_output = r".\msfs_native_nav_output" #変数定義（ナビデータ一時展開先フォルダー）
        #↓ナビデータ一時解凍先フォルダーが存在する場合は削除↓
        if os.path.exists(msfs_native_nav_output):
            shutil.rmtree(msfs_native_nav_output)
        
        #「UserCfg.opt」を検索、MSFSインストールパスを入手し、Communityフォルダーを定義
        if glob.glob(r'C:\Users\*\AppData\Local\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache\UserCfg.opt'):
            for msfs_opt_file in glob.glob(r'C:\Users\*\AppData\Local\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache\UserCfg.opt'):
                f = open(msfs_opt_file, "r")
                alltxt = f.readlines()
                f.close()
                MSFSpathL = len(alltxt)
                MSFSpathF = alltxt[MSFSpathL-1].strip()
                MSFSpathH = MSFSpathF.replace("InstalledPackagesPath ", "")
                MSFSpath = MSFSpathH.strip('"')
                msfs_community = MSFSpath + r"\Community"
                print("Community folder path = " + msfs_community)
        elif glob.glob(r'C:\Users\*\AppData\Roaming\Microsoft Flight Simulator\UserCfg.opt'):
            for msfs_opt_file in glob.glob(r'C:\Users\*\AppData\Roaming\Microsoft Flight Simulator\UserCfg.opt'):
                f = open(msfs_opt_file, "r")
                alltxt = f.readlines()
                f.close()
                MSFSpathL = len(alltxt)
                MSFSpathF = alltxt[MSFSpathL-1].strip()
                MSFSpathH = MSFSpathF.replace("InstalledPackagesPath ", "")
                MSFSpath = MSFSpathH.strip('"')
                msfs_community = MSFSpath + r"\Community"
                print("Community folder path = " + msfs_community)
        else:
            tkinter.Tk().withdraw()
            tkinter.messagebox.showerror('Navigraph Navdata Installer','Cannot find the Community folder. Please select your Community folder in next dialog.')
            msfs_community = filedialog.askdirectory(initialdir=os.path.abspath('.'), title='Please select your Community folder.')
        
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
                if os.path.exists(msfs_community + r"\navigraph-navdata"):
                    shutil.rmtree(msfs_community + r"\navigraph-navdata")

                if os.path.exists(msfs_community + r"\navigraph-navdata-base"):
                    shutil.rmtree(msfs_community + r"\navigraph-navdata-base")

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

                if shutil.move(r'.\msfs_native_nav_output\Content.xml', msfs_package):
                    print('"Content.xml copied."')#「Content.xml」ファイルをコピー
                else:
                    print('Could not copy "Content.xml" file to the MSFS folder')
                    tkinter.Tk().withdraw()
                    tkinter.messagebox.showerror(message='Could not copy "Content.xml" to your MSFS folder. Please copy it manually. (This is because "Content.xml" is not existed in your MSFS folder.)')
                
                shutil.rmtree(msfs_native_nav_output)#ナビデータ一時解凍先フォルダーを消去
                print("Install complete.")
            else:
                tkinter.Tk().withdraw()
                tkinter.messagebox.showerror(message="The file you selected is not valid as navdata. Please restart this application and reselect a file.")
                sys.exit()
        else:
            sys.exit()
    else:
        return

def pmdg_install():
    if pmdg_checkbox.get() == 1:
        #「UserCfg.opt」を検索、MSFSインストールパスを入手し、Communityフォルダーを定義
        if glob.glob(r'C:\Users\*\AppData\Local\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache\UserCfg.opt'):
            for msfs_opt_file in glob.glob(r'C:\Users\*\AppData\Local\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache\UserCfg.opt'):
                f = open(msfs_opt_file, "r")
                alltxt = f.readlines()
                f.close()
                MSFSpathL = len(alltxt)
                MSFSpathF = alltxt[MSFSpathL-1].strip()
                MSFSpathH = MSFSpathF.replace("InstalledPackagesPath ", "")
                MSFSpath = MSFSpathH.strip('"')
                msfs_community = MSFSpath + r"\Community"
                print("Community folder path = " + msfs_community)
        elif glob.glob(r'C:\Users\*\AppData\Roaming\Microsoft Flight Simulator\UserCfg.opt'):
            for msfs_opt_file in glob.glob(r'C:\Users\*\AppData\Roaming\Microsoft Flight Simulator\UserCfg.opt'):
                f = open(msfs_opt_file, "r")
                alltxt = f.readlines()
                f.close()
                MSFSpathL = len(alltxt)
                MSFSpathF = alltxt[MSFSpathL-1].strip()
                MSFSpathH = MSFSpathF.replace("InstalledPackagesPath ", "")
                MSFSpath = MSFSpathH.strip('"')
                msfs_community = MSFSpath + r"\Community"
                print("Community folder path = " + msfs_community)
        else:
            tkinter.Tk().withdraw()
            tkinter.messagebox.showerror('Navigraph Navdata Installer','Cannot find the Community folder. Please select your Community folder in next dialog.')
            msfs_community = filedialog.askdirectory(initialdir=os.path.abspath('.'), title='Please select your Community folder.')
        
        tkinter.Tk().withdraw()
        if tkinter.messagebox.askokcancel('Navigraph Navdata Installer for PMDG 737NG','To use this installer, you need to download the latest AIRAC Navdata from SimPlaza. Select the archive file you downloaded in next dialog. File example: "navigraph-navdata-installer-airac-cycle-2310.rar"') == True:
            pmdg_nav_rar = filedialog.askopenfilename(filetypes=[('RAR Archive file','*.rar')], initialdir=os.path.abspath('.'), title="Select the latest Navigraph AIRAC archive file.(Navdata Installers)")
            pmdg_nav_rar_basename = os.path.basename(pmdg_nav_rar)
            if'navigraph-navdata-installers-airac-cycle-' in pmdg_nav_rar_basename:
                
                pmdg_nav_output_ph1 = r".\pmdg_nav_output_ph1" #解凍段階1
                pmdg_nav_output_ph2 = r".\pmdg_nav_output_ph2" #解凍段階2(最終完了)
                pmdg_nav_NavData = pmdg_nav_output_ph2 + r"\NavData" #解凍先NavDataのフルパス
                pmdg_nav_SidStars = pmdg_nav_output_ph2 + r"\SidStars" #解凍先SidStarsのフルパス
                pmdg_config_route_736 = msfs_community + r"\pmdg-aircraft-736\Config"
                pmdg_config_route_737 = msfs_community + r"\pmdg-aircraft-737\Config"
                pmdg_config_route_738 = msfs_community + r"\pmdg-aircraft-738\Config"
                pmdg_config_route_739 = msfs_community + r"\pmdg-aircraft-739\Config"
                
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
                if os.path.exists(msfs_community + r"\pmdg-aircraft-736"):
                    print("PMDG B736 Found",(msfs_community + r"\pmdg-aircraft-736"))
                    shutil.rmtree(pmdg_config_route_736 + r"\NavData")
                
                    if os.path.exists(pmdg_config_route_736 + r"\SidStars"):
                        shutil.rmtree(pmdg_config_route_736 + r"\SidStars")
                    elif os.path.exists(pmdg_config_route_736 + r"\SIDSTARS"):
                        shutil.rmtree(pmdg_config_route_736 + r"\SIDSTARS")
                
                    shutil.copytree(pmdg_nav_NavData, pmdg_config_route_736 + r"\NavData")
                    shutil.copytree(pmdg_nav_SidStars, pmdg_config_route_736 + r"\SidStars")
                else:
                    print("PMDG B736 Not found in your community folder. We will skip this nav update.")
            
                if os.path.exists(msfs_community + r"\pmdg-aircraft-737"):
                    print("PMDG B737 Found",(msfs_community + r"\pmdg-aircraft-737"))
                    shutil.rmtree(pmdg_config_route_737 + r"\NavData")
                
                    if os.path.exists(pmdg_config_route_737 + r"\SidStars"):
                        shutil.rmtree(pmdg_config_route_737 + r"\SidStars")
                    elif os.path.exists(pmdg_config_route_737 + r"\SIDSTARS"):
                        shutil.rmtree(pmdg_config_route_737 + r"\SIDSTARS")
                
                    shutil.copytree(pmdg_nav_NavData, pmdg_config_route_737 + r"\NavData")
                    shutil.copytree(pmdg_nav_SidStars, pmdg_config_route_737 + r"\SidStars")
                else:
                    print("PMDG B737 Not found in your community folder. We will skip this nav update.")
            
                if os.path.exists(msfs_community + r"\pmdg-aircraft-738"):
                    print("PMDG B738 Found",(msfs_community + r"\pmdg-aircraft-738"))
                    shutil.rmtree(pmdg_config_route_738 + r"\NavData")
                
                    if os.path.exists(pmdg_config_route_738 + r"\SidStars"):
                        shutil.rmtree(pmdg_config_route_738 + r"\SidStars")
                    elif os.path.exists(pmdg_config_route_738 + r"\SIDSTARS"):
                        shutil.rmtree(pmdg_config_route_738 + r"\SIDSTARS")
                
                    shutil.copytree(pmdg_nav_NavData, pmdg_config_route_738 + r"\NavData")
                    shutil.copytree(pmdg_nav_SidStars, pmdg_config_route_738 + r"\SidStars")
                else:
                    print("PMDG B738 Not found in your community folder. We will skip this nav update.")
            
                if os.path.exists(msfs_community + r"\pmdg-aircraft-739"):
                    print("PMDG B739 Found",(msfs_community + r"\pmdg-aircraft-739"))
                    shutil.rmtree(pmdg_config_route_739 + r"\NavData")
                
                    if os.path.exists(pmdg_config_route_739 + r"\SidStars"):
                        shutil.rmtree(pmdg_config_route_739 + r"\SidStars")
                    elif os.path.exists(pmdg_config_route_739 + r"\SIDSTARS"):
                        shutil.rmtree(pmdg_config_route_739 + r"\SIDSTARS")
                
                    shutil.copytree(pmdg_nav_NavData, pmdg_config_route_739 + r"\NavData")
                    shutil.copytree(pmdg_nav_SidStars, pmdg_config_route_739 + r"\SidStars")
                else:
                    print("PMDG B739 Not found in your community folder. We will skip this nav update.")
                
                shutil.rmtree(pmdg_nav_output_ph2)
                print("Install complete.")
            else:
                tkinter.Tk().withdraw()
                tkinter.messagebox.showerror(message="The file you selected is not valid for PMDG navdata. Please restart this application and reselect a file.")
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
            if 'navigraph-navdata-installers-airac-cycle-' in fenix_nav_rar_basename:
                #「UserCfg.opt」を検索、MSFSインストールパスを入手し、Communityフォルダーを定義
                if glob.glob(r'C:\Users\*\AppData\Local\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache\UserCfg.opt'):
                    for msfs_opt_file in glob.glob(r'C:\Users\*\AppData\Local\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache\UserCfg.opt'):
                        f = open(msfs_opt_file, "r")
                        alltxt = f.readlines()
                        f.close()
                        MSFSpathL = len(alltxt)
                        MSFSpathF = alltxt[MSFSpathL-1].strip()
                        MSFSpathH = MSFSpathF.replace("InstalledPackagesPath ", "")
                        MSFSpath = MSFSpathH.strip('"')
                        msfs_community = MSFSpath + r"\Community"
                        print("Community folder path = " + msfs_community)
                elif glob.glob(r'C:\Users\*\AppData\Roaming\Microsoft Flight Simulator\UserCfg.opt'):
                    for msfs_opt_file in glob.glob(r'C:\Users\*\AppData\Roaming\Microsoft Flight Simulator\UserCfg.opt'):
                        f = open(msfs_opt_file, "r")
                        alltxt = f.readlines()
                        f.close()
                        MSFSpathL = len(alltxt)
                        MSFSpathF = alltxt[MSFSpathL-1].strip()
                        MSFSpathH = MSFSpathF.replace("InstalledPackagesPath ", "")
                        MSFSpath = MSFSpathH.strip('"')
                        msfs_community = MSFSpath + r"\Community"
                        print("Community folder path = " + msfs_community)
                else:
                    tkinter.Tk().withdraw()
                    tkinter.messagebox.showerror('Navigraph Navdata Installer','Cannot find the Community folder. Please select your Community folder in next dialog.')
                    msfs_community = filedialog.askdirectory(initialdir=os.path.abspath('.'), title='Please select your Community folder.')
                
                if os.path.isfile(msfs_community + r"\fnx-aircraft-320\SimObjects\Airplanes\FNX320\aircraft.cfg"):
                    print("Fenix A320 aircraft installed.")
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
                        if os.path.isfile(fenix_nav_install_path + r"\cycle.json"):
                            os.remove(fenix_nav_install_path + r"\cycle.json")
                            print('Existing "cycle.json" deleted.')
                        shutil.move(fenix_nav_output_ph2 + r"\Navdata\cycle.json", fenix_nav_install_path)
                        print('Copied "cycle.json"')
                        if os.path.isfile(fenix_nav_install_path + r"\cycle_info.txt"):
                            os.remove(fenix_nav_install_path + r"\cycle_info.txt")
                            print('Existing "cycle_info.txt" deleted.')
                        shutil.move(fenix_nav_output_ph2 + r"\Navdata\cycle_info.txt", fenix_nav_install_path)
                        print('Copied "cycle_info.txt"')
                        if os.path.isfile(fenix_nav_install_path + r"\nd.db3"):
                            os.remove(fenix_nav_install_path + r"\nd.db3")
                            print('Existing "nd.db3" deleted.')
                        shutil.move(fenix_nav_output_ph2 + r"\Navdata\nd.db3", fenix_nav_install_path)
                        print('Copied "nd.db3"')
                        shutil.rmtree(fenix_nav_output_ph2)
                        print("Install complete.")
                    else:
                        os.mkdir(fenix_nav_install_path)
                        
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
                        
                        shutil.move(fenix_nav_output_ph2 + r"\Navdata\cycle.json", fenix_nav_install_path)
                        print('Copied "cycle.json"')
                        
                        shutil.move(fenix_nav_output_ph2 + r"\Navdata\cycle_info.txt", fenix_nav_install_path)
                        print('Copied "cycle_info.txt"')
                        
                        shutil.move(fenix_nav_output_ph2 + r"\Navdata\nd.db3", fenix_nav_install_path)
                        print('Copied "nd.db3"')
                        
                        shutil.rmtree(fenix_nav_output_ph2)
                        print("Install complete.")
                else:
                    print("Fenix A320 not installed.")
                    tkinter.Tk().withdraw()
                    tkinter.messagebox.showerror("Is Fenix A320 installed?", 'Could not find the folder "C:\\ProgramData\\Fenix\\Navdata". It seems Fenix A320 is not installed in this computer.')
                    sys.exit()
            else:
                tkinter.Tk().withdraw()
                tkinter.messagebox.showerror(message="The file you selected is not valid for Fenix A320 navdata. Please restart this application and reselect a file.")
                sys.exit()
        else:
            sys.exit()
    else:
        return

root = tkinter.Tk()
root.title("Navigraph Navdata Installer for MSFS")
root.geometry("350x250")
instruction_label = tkinter.Label(root, justify="center", text='[Select the checkbox you want to install, then press "Install".]')
msfs_native_checkbox = tkinter.IntVar()
pmdg_checkbox = tkinter.IntVar()
fenix_checkbox = tkinter.IntVar()
msfs_native_checkbutton = tkinter.Checkbutton(root, variable=msfs_native_checkbox)
pmdg_checkbutton = tkinter.Checkbutton(root, variable=pmdg_checkbox)
fenix_checkbutton = tkinter.Checkbutton(root, variable=fenix_checkbox)
msfs_native_checkbutton_label = tkinter.Label(root, justify="left", text="MSFS Native Navdata")
pmdg_checkbutton_label = tkinter.Label(root, justify="left", text="PMDG 737 Navdata")
fenix_checkbutton_label = tkinter.Label(root, justify="left", text="Fenix A320 Navdata")
all_navdata_installed_version_info_label = tkinter.Label(root, justify="center", text='[↓ Current navdata version installed ↓]')
msfs_native_nav_version_fixed_label = tkinter.Label(root, justify="left", text="MSFS Native:")
pmdg_nav_version_fixed_label = tkinter.Label(root, justify="left", text="PMDG 737:")
fenix_nav_version_fixed_label = tkinter.Label(root, justify="left", text="Fenix A320:")
msfs_native_nav_version = tkinter.Label(root, justify="left")
pmdg_nav_version = tkinter.Label(root, justify="left")
fenix_nav_version = tkinter.Label(root, justify="left")
install_button = tkinter.Button(root, text="Install", width=15, command=on_nav_install_select_button_click)
exit_button = tkinter.Button(root, text="Exit", width=15, command=sys.exit)
info_label = tkinter.Label(root, text="Made by Legotatsu1985 with Tkinter", fg="blue", anchor=tkinter.S)
version_label = tkinter.Label(root, text="v2.0.0", anchor=tkinter.SE)
#UI配置↓
instruction_label.grid(
    column=0, columnspan=2, row=0
)
msfs_native_checkbutton.grid(
    column=0, row=1, sticky=tkinter.E
)
msfs_native_checkbutton_label.grid(
    column=1, row=1, sticky=tkinter.W
)
pmdg_checkbutton.grid(
    column=0, row=2, sticky=tkinter.E
)
pmdg_checkbutton_label.grid(
    column=1, row=2, sticky=tkinter.W
)
fenix_checkbutton.grid(
    column=0, row=3, sticky=tkinter.E
)
fenix_checkbutton_label.grid(
    column=1, row=3, sticky=tkinter.W
)
all_navdata_installed_version_info_label.grid(
    column=0, columnspan=2, row=4
)
msfs_native_nav_version_fixed_label.grid(
    column=0, row=5, sticky=tkinter.E
)
msfs_native_nav_version.grid(
    column=1, columnspan=2, row=5, sticky=tkinter.W
)
pmdg_nav_version_fixed_label.grid(
    column=0, row=6, sticky=tkinter.E
)
pmdg_nav_version.grid(
    column=1, columnspan=2, row=6, sticky=tkinter.W
)
fenix_nav_version_fixed_label.grid(
    column=0, row=7, sticky=tkinter.E
)
fenix_nav_version.grid(
    column=1, columnspan=2, row=7, sticky=tkinter.W
)
get_msfs_opt_file()
install_button.grid(
    column=0, row=8, sticky=tkinter.E
)
exit_button.grid(
    column=1, row=8, sticky=tkinter.W
)
info_label.grid(
    column=0, columnspan=2, row=9
)
version_label.grid(
    column=0, columnspan=2, row=10
)
root.mainloop()