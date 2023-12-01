
import glob
import os
import shutil
import sys
import tkinter
import tkinter.messagebox
from tkinter import filedialog

import rarfile

f = open(r"I:\MSFS2020 Data\Game_Packages\Community\navigraph-navdata\manifest.json")
alltxt = f.readlines()
f.close()
navigraph_navdata_version_L = len(alltxt)
navigraph_navdata_version_F = alltxt[navigraph_navdata_version_L-12].strip()
navigraph_navdata_version_H1 = navigraph_navdata_version_F.replace('  "title": ', '')
print(navigraph_navdata_version_H1)