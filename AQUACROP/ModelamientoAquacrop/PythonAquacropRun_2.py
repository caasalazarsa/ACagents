#!/usr/bin/env python
# coding=utf-8
"""
Created on Thu Aug 23 14:27:31 2018

@author: precision
"""

import subprocess
import shutil
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import os
import io
import sys
from random import randrange
from datetime import datetime,timedelta



switcher = {
        1: 0,
        2: 31,
        3: 59.25,
        4: 90.25,
        5: 120.25,
        6: 151.25,
        7: 181.25,
        8: 212.25,
        9: 243.25,
        10: 273.25,
        11: 304.25,
        12: 334.25
    }


def EditModel(agentid, crop, startdate, cropdays,irrdays):
    finaldate=startdate + timedelta(cropdays)
    path='../ACApp/DATA/Default.PRO'
    path1='../ACApp/DATA/Default_Test.PRO'
    #path2='/home/caasalazarsa/Documentos/PRUEBAS_TESIS/AquaCropV61Nr02052018/DATA/Default_Out.PRO'
    path2='../ACPlug/LIST/Default.PRO'
    shutil.copyfile(path, path1)
    i=0
    p = os.path.abspath('..')
    filedata = open(path1,"r+",encoding="cp1252")

    output = open(path2,"w+",encoding="cp1252",newline='\r\n')
    i=0
    h=0
    h=randrange(6)
    for line in filedata:
        line=str(line)
        a = line.split( )
        #print(line,'\n')
        if not a:
            print("Line is empty")
            output.write(line)
        else:
            #print(i,line,'\n') 
            #print(i,a[0],'\n')
            if i==2:
##  34414         : First day of simulation period
               year=startdate.year
               month=startdate.month
               day=startdate.day

               nummonth=switcher.get(month,"no hay")
               number=int((year-1901)*365.25+nummonth+day)
               line2='  '+str(number)+'         : First day of simulation period - '+startdate.strftime("%d %B %Y")+' '
               print(line2+'\n')
               output.write(line2+'\n') 
            elif i==3:
##  34481         : Last day of simulation period
               year=finaldate.year
               month=finaldate.month
               day=finaldate.day

               nummonth=switcher.get(month,"no hay")
               number=int((year-1901)*365.25+nummonth+day)
               line2='  '+str(number)+'         : First day of simulation period - '+finaldate.strftime("%d %B %Y")+' '
               print(line2+'\n')
               output.write(line2+'\n') 
            elif i==4:
##  34414         : First day of cropping period
               year=startdate.year
               month=startdate.month
               day=startdate.day

               nummonth=switcher.get(month,"no hay")
               number=int((year-1901)*365.25+nummonth+day)
               line2='  '+str(number)+'         : First day of simulation period - '+startdate.strftime("%d %B %Y")+' '
               print(line2+'\n')
               output.write(line2+'\n') 
            elif i==5:
##  34414         : Last day of cropping period
               year=finaldate.year
               month=finaldate.month
               day=finaldate.day

               nummonth=switcher.get(month,"no hay")
               number=int((year-1901)*365.25+nummonth+day)
               line2='  '+str(number)+'         : First day of simulation period - '+startdate.strftime("%d %B %Y")+' '
               print(line2+'\n')
               output.write(line2+'\n') 
            elif i==28:
               #h=randrange(6)
               #line='   TEST.CLI'
               #line = '   Lima.CLI'
               line = '   (None)'
               output.write(line+'\n')

            elif i==31:
               #h=randrange(6)
               #line='   Bogota.TMP'
               #line = '   Lima.TMP'
               line = '   (None)'
               output.write(line+'\n')

            elif i==34:
               #h=randrange(6)
               #line='   Bogota.ETo'
               #line = '   Lima.ETo'
               line = '   (None)'
               output.write(line+'\n')

            elif i==37:
               #h=randrange(6)
               line='   NoRain.PLU'
               #line = '   Lima.PLU'
               output.write(line+'\n')

            elif i==40:
               line='   MaunaLoa.CO2'
               output.write(line+'\n')
               """h=randrange(6)
               if h==0:
                line='   A2.CO2'
               elif h==1:
                line='   B1.CO2'
               elif h==2:
                line='   B2.CO2'
               elif h==3:
                line='   A1B.CO2'
               elif h==4:
                line='   GlobalAverage.CO2'
               elif h==5:
                line='   RCP2-6.CO2'
               output.write(line+'\n')"""
               


            elif i==43:

               if crop=='maiz':
                line='   CORN_TEST.CRO'
               elif crop=='cebada':
                line='   CEBADA_TEST.CRO'
               elif crop=='lechuga':
                line='   LETTUCE_TEST.CRO'
               elif crop=='cebolla':
                line='   ONION_TEST.CRO'
               elif crop=='uva':
                line='   GRAPES_TEST.CRO'
               elif crop=='tomate':
                line='   TOMATO_TEST.CRO'
               output.write(line+'\n')

            elif i==46:
                if 'agent' not in agentid:
                    line='(None)'
                else:
                    line='irrigationprescmod'+agentid+crop+irrdays+'consensus.IRR'
                    print(line)
                output.write(line+'\n')

            elif i==52:
                line='   DEFAULT.SOL'
                output.write(line+'\n')

            else:
                output.write(line)
            #output.write(line)                      

        i+=1
    output.close()
    filedata.close()
       
       #shutil.copyfile(path2, path3)       

def EditIrrigation():
   path='../ACApp/DATA/Default_Test.PRO'
   path1='../ACApp/DATA/Default_Test_Test.PRO'
   path2='../ACApp/DATA/Defualt_Test_Out.PRO'

   shutil.copyfile(path, path1)
   i=0 
   
   filedata = open(path1,"r")
   output = open(path2,"w")   
   i=0
   for line in filedata:
       a = line.split( )


       
def runModel():
    proc=subprocess.Popen(['wine', '../ACPlug/ACsaV60.exe'])
    stdoutdata, stderrdata = proc.communicate()
    

def readModelOutput():
   path='../ACPlug/OUTP/DefaultPROday.OUT'
   path1='Temporalday.txt'
   path2='ModelOutputday.txt'
   shutil.copyfile(path, path1) 
   with open(path1, 'r',errors='ignore') as fin:
       data = fin.read().splitlines(True)
   with open(path2, 'w') as fout:
       fout.writelines(data[4:])
   fin.close()
   fout.close() 
   

   path3='../ACPlug/OUTP/DefaultPROseason.OUT'
   path4='Temporalseason.txt'
   path5='ModelOutputseason.txt'
   shutil.copyfile(path3, path4) 
   with open(path4, 'r',errors='ignore') as fin1:
       data = fin1.read().splitlines(True)
   with open(path5, 'w') as fout1:
       fout1.writelines(data[4:])
   fin1.close()
   fout1.close() 

   
def Charts(agentid,crop,irrdays):
    filedata = open('ModelOutputday.txt',"r")
    Day=[]
    Month=[]
    WC1=[]
    WC2=[]
    WC3=[]    
    rain = []
    irrigation =[]
    CC=[]
    Etc=[]
    GD=[]
    KC=[]
    Biomass=[]
    Yield=[]
    Z=[]
    i=0
    for line in filedata:
       a = line.split()
       Day.append(float(i))
       WC1.append(float(a[65]))
       WC2.append(float(a[66]))
       WC3.append(float(a[67]))      
       rain.append(float(a[6]))
       irrigation.append(float(a[7]))
       Etc.append(float(a[21]))
       KC.append(float(a[33]))   
       GD.append(float(a[23]))       
       Z.append(float(a[24]))    
       CC.append(float(a[30]))
       Biomass.append(float(a[39]))
       Yield.append(float(a[41]))       
       
       i=i+1
       
    fig = plt.figure()
    title="Simulación de cultivo de "+crop
    if 'agent' not in agentid:
        title=title+" sin riego"
    else:
        title=title + " con irrigación"

    plt.title(title)
    color = 'black'
    ax = fig.add_subplot(511)
#    ax.set_xlim(datemin, datemax)
    ax.set_ylabel('mm', color=color, fontsize=15)
    ax.grid(True)
    fig.set_size_inches(12, 8)
    
    ax.plot(Day, rain,'k',label='Rain')
    ax.plot(Day, irrigation,'c',label='Irrigation')
    ax.plot(Day, Etc,'m',label='ETc')
    #ax.set_title('Time (Days)')  
    legend = ax.legend(loc='upper left', shadow=True, fontsize=8)
    legend.get_frame().set_facecolor('#87CEFA')       
      
    ax = fig.add_subplot(512)
#    ax.set_xlim(datemin, datemax)
    ax.set_ylabel('Ton/ha', color=color, fontsize=15)
    ax.set_xlabel('Time (Days)')  
    ax.grid(True)
    fig.set_size_inches(12, 8)
    ax.plot(Day, Biomass,'r', label='Biomass')
    ax.plot(Day, Yield,'g',label='Yield')
    #ax.set_title('Biomass (ton/ha) and Yield (ton/ha)')  
    legend = ax.legend(loc='upper left', shadow=True, fontsize=8)
    legend.get_frame().set_facecolor('#87CEFA')
       

    ax = fig.add_subplot(513)
#    ax.set_xlim(datemin, datemax)
    ax.set_ylabel('Deg C-day', color=color, fontsize=15)
    ax.set_xlabel('Time (Days)')  
    ax.grid(True)
    fig.set_size_inches(12, 8)
    ax.plot(Day, GD,'b', label='GD')
    #ax.set_title('GD (Deg C - day)')  
    legend = ax.legend(loc='upper left', shadow=True, fontsize=8)
    legend.get_frame().set_facecolor('#87CEFA')

    ax = fig.add_subplot(514)
#    ax.set_xlim(datemin, datemax)
    ax.set_ylabel('% VWC', color=color, fontsize=15)
    ax.set_xlabel('Time (Days)')  
    ax.grid(True)
    fig.set_size_inches(12, 8)
    ax.plot(Day, WC1,'r', label='WC Depth 1')
    ax.plot(Day, WC2,'g', label='WC Depth 2')    
    ax.plot(Day, WC3,'b', label='WC Depth 3')
    #ax.set_title()  
    legend = ax.legend(loc='upper left', shadow=True, fontsize=8)
    legend.get_frame().set_facecolor('#87CEFA')                    

    ax = fig.add_subplot(515)
#    ax.set_xlim(datemin, datemax)
    ax.set_ylabel('CC (%)', color=color, fontsize=15)
    ax.set_xlabel('Time (Days)')  
    ax.grid(True)
    fig.set_size_inches(12, 8)
    ax.plot(Day, CC,'g', label='CC')
    #ax.set_title('CC (%)')  
    legend = ax.legend(loc='upper left', shadow=True, fontsize=8)
    legend.get_frame().set_facecolor('#87CEFA')                       

    Season = open('ModelOutputseason.txt',"r")
    for line in Season:
       a = line.split()
       print ('Total Rain', a[4])
       print ('Total ET0', a[5] )
       print ('Total GD', a[6])
       print ('Total CO2', a[7])
       print ('Total Irrigation',a[8] )
       print ('Total Biomass (ton/ha)',a [29] )
       print ('Total Yield (ton/ha)', a[32] )

    plt.show(block=False)
    plt.pause(0.001)
    title=title.replace(' ','_')
    title=title.replace('ó','o')
    plt.savefig(title+ irrdays + '.png')


agentid=sys.argv[1]
cropdata = sys.argv[2]
irrdays= sys.argv[4]
initial_day = datetime.strptime(sys.argv[3], '%d-%m-%Y')
crop, days = cropdata.split(',')

EditModel(agentid,crop,initial_day,int(days),irrdays)
runModel()                   
readModelOutput()
Charts(agentid,crop,irrdays)
