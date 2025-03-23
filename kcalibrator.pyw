#! /usr/bin/env python
#  -*- coding: utf-8 -*-
# author: Victor Shapovalov (@ArtificalSUN, https://github.com/ArtificalSUN), 2022
# Configuration contributed by Foreytor (https://github.com/Foreytor)
# version: 1.0.4-bugfix

"""
This script generates pattern for Linear Advance K-factor calibration for Marlin (and other firmwares)
The pattern consists of a rectangular wall printed with sharp changes in speed and with K-factor increasing from bottom to top
Print the pattern and find the height where it looks the best
Corners should not bulge, flow should be homogeneous with as little influence from speed changes as possible, seam should be barely noticeable
Calculate desired K-factor from this height and parameters you used to generate the pattern
Good luck!
"""

versionstring = "Kcalibrator v1.0.4-bugfix (Victor Shapovalov, 2022)"
import os, sys


import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fldg

import kcalibrator_gui as gui
import kcalibrator_gui_support as gui_support
import kcalibrator_func as kcalibrator
import kcalibrator_settings as settings


def save_config():
    global currentConfig, top
    currentConfig.updatesettings(top)
    currentConfig.save_config(configPath)

def update_and_create():
    global currentConfig, top
    currentConfig.updatesettings(top)
    gcode = kcalibrator.creategcode(currentConfig)
    path = fldg.asksaveasfilename(title = "Save the G-code", filetypes = (("G-code files","*.gcode"),("All files","*.*")), defaultextension = ".gcode", initialfile = "KF_{b}-{e}-{s}_H{t[0]}-B{t[1]}.gcode".format(b=currentConfig.k_start, e=currentConfig.k_end, s=currentConfig.k_step, t=currentConfig.temperature))
    # path = fldg.asksaveasfile(title = "Save the G-code", filetypes = (("G-code files","*.gcode"),("All files","*.*")), defaultextension = ".gcode", initialfile = "KF_{b}-{e}-{s}_H{t[0]}-B{t[1]}.gcode".format(b=currentConfig.k_start, e=currentConfig.k_end, s=currentConfig.k_step, t=currentConfig.temperature))
    with open(path, "w") as out:
        out.writelines(gcode)


configPath = "Kcalibrator.cfg"
currentConfig = settings.SettingClass()
if os.path.exists(configPath):
    try: currentConfig.read_config(configPath)
    except: currentConfig.save_config(configPath)
else:
    currentConfig.save_config(configPath)
defaultConfig = settings.SettingClass()

root = tk.Tk()
print("Running with Python {}".format(sys.version))
print("Tkinter Tcl/Tk version {}".format(root.tk.call("info", "patchlevel")))
gui_support.set_Tk_var()
top = gui.Toplevel(root)
gui_support.init(root, top)

top.attach()
try: top.updateUI(currentConfig)
except IndexError:
    defaultConfig.save_config(configPath)
    currentConfig.read_config(configPath)
    top.updateUI(currentConfig)
top.revalidate_all()
top.btn_SaveConfig.configure(command = save_config)
top.btn_Generate.configure(command = update_and_create)
# top.btn_Calc.configure(command = top.calculate_K)

# root.after(10, top.updateUI)
root.mainloop()
