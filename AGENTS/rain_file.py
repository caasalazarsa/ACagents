
import subprocess
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def save_presc():
    path1 = '../AQUACROP/ACPlug/DATA/PluAuburn.PLU'
    pathrain = 'clima_boyaca_2018.txt'
    path2 = '../AQUACROP/ACPlug/DATA/Boyaca.PLU'
    shutil.copyfile(path1, path2)
    i = 0
    p = os.path.abspath('..')

    filedata = open(path1, "r+", encoding="cp1252")

    raindata = open(pathrain, "r+", encoding="cp1252")

    output = open(path2, "w+", encoding="cp1252", newline='\r\n')

    a = ["", "", ""]
    for line in filedata:
        line = str(line)

        if not a:
            print("Line is empty")
            output.write(line)
        else:
            output.write(line)

    for line in raindata:
        line =str(line)
        line = line.replace(',','.')
        output.write(line)



    output.close()

    pass

save_presc()