
import glob
import os
import shutil
import sys
import tkinter
import tkinter.messagebox
from tkinter import filedialog

import rarfile

f = open(r"C:\Users\Ryota\AppData\Roaming\Microsoft Flight Simulator\UserCfg.opt", "r")
alltxt = f.readlines()
f.close()