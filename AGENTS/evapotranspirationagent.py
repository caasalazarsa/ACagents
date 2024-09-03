# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 14:27:31 2018

@author: caasalazarsa
"""

import time
import numpy as np
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
import subprocess
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour, TimeoutBehaviour
from spade.message import Message
import sys
import random


import signal



class EvapotranspirationAgent(Agent):

    def __init__(self, name, password,crop,day,resilience):
        Agent.__init__(self,name,password)
        self.crop=crop
        self.day=day
        self.area=area
        self.ETc = []
        self.profile=[]
        self.presc =[]
        self.water=0
        self.neighbors=[]
        self.neighborvalues={}
        self.resilience=resilience

  #  class InformandReceiveBehav(CyclicBehaviour):
    class InformBehav(CyclicBehaviour):
        async def run(self):
            #print("InformBehav running")
            for neighbor in self.agent.neighbors:
             msg = Message(to=neighbor)     # Instantiate the message
             msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
             msg.set_metadata("ontology", "myOntology")  # Set the ontology of the message content
             msg.set_metadata("language", "OWL-S")       # Set the language of the message content
             msg.body = str(self.agent.ir)+'/'+str(self.agent.water)                  # Set the message content

             await self.send(msg)
             #print("Message sent!")

             #print("RecvBehav running")

    class RecieveBehav(CyclicBehaviour):
        async def run(self):

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                if "Factor:" not in msg.body:
                    info = msg.body.split('/')
                    self.agent.neighborvalues[str(msg.sender)]=float(info[0])
                    self.agent.consensus()
                else:
                    info = msg.body.split(':')
                    if info[1]=='1':
                        pass
                    else:
                        self.agent.ir=self.agent.ir*self.agent.resilience*float(info[1])
                        print(self.agent.ir)


            else:
                print("Did not received any message after 10 seconds")

    def loadneighbors(self,name):
        with  open('list.txt') as f:
            lines = f.read().splitlines()
            lines.remove(name)
            self.neighbors=lines
            #print(self.neighbors)


    def setup(self):
        print("SenderAgent started")
        #self.b = self.InformandReceiveBehav()
        b = self.InformBehav()
        b2= self.RecieveBehav()
        self.add_behaviour(b)
        self.add_behaviour(b2)


    def evapotranspirationout(self,initial_day,days,Et0_crop_list):
        crop=self.crop
        stages = pd.read_csv('growth_stages.csv')
        factors = pd.read_csv('crop_factors.csv')
        factors_np = factors.loc[factors['cultivo']==crop].to_numpy()
        stages_np = stages.loc[stages['cultivo']==crop].to_numpy()
        profile = np.linspace(factors_np[0][1],factors_np[0][1],stages_np[0][1])
        profile=np.concatenate((profile,np.linspace(factors_np[0][1],factors_np[0][2],stages_np[0][2])))
        profile=np.concatenate((profile,np.linspace(factors_np[0][2],factors_np[0][2],stages_np[0][3])))
        profile = np.concatenate((profile, np.linspace(factors_np[0][2], factors_np[0][3], stages_np[0][4])))
        #print(profile)
        self.profile=profile
        for day in range(days):
            self.ETc.append(Et0_crop_list[day]*profile[day])
        plt.plot(profile)
        plt.title("Ciclo de crecimiento de "+crop)
        plt.xlabel("Días")
        plt.ylabel("Factor de Cultivo Kc")
        plt.ylim(0,1.2)
        plt.show(block=False)
        plt.pause(0.001)
        plt.savefig(sys.argv[1]+'.png')


        return self.ETc

    def consensus(self):
        if len(self.neighborvalues)!=0:
           dx=-len(self.neighborvalues)*self.ir
           #print(dx)
           for neighbor in self.neighborvalues:
              dx=dx+self.neighborvalues[neighbor]
           self.ir=self.ir+.0005*dx

    def getpresc(self,initial_day,days,rainfall,rainfall_flag,Dp,Irr,flag):

        self.presc=[]
        for i in range(days):
            presc=self.ETc[i]-rainfall[i]*int(rainfall_flag)+Dp-Irr
            if flag and (self.ir/self.resilience)<1:
                presc=presc*(self.ir/self.resilience)
            if presc<0:
                self.presc.append(0)
            else:
                self.presc.append(presc)


            #print("Evapotranspiration: "+str(self.Etc))
            #if(self.ir<1):
            #    self.presc[i]=self.presc[i]*self.ir

            #print("presc: "+str(self.presc))
            #if(abs(self.presc[i]+rainfall[i]-self.ETc[i])<0.01):
            #    print("prescripción válida")
        
          
        return self.presc



    def getwater(self):
        area=self.area
        self.water=0
        #for i in range(len(self.presc)):
        presc_LHa=self.presc[10]*10**4 #[L/Ha]
        self.water=self.water+presc_LHa*area

        print("Cantidad de agua para el día 10 en L: "+str(round(self.water,2)))


    def getweights(self,Day):
        
        pass

    def save_presc(self,flag,days=1):

        if days <=0:
            days=1

        path1 = '../AQUACROP/ACApp/DATA/irrigationtemplate.IRR'
        if flag:
            path2 = '../AQUACROP/ACApp/DATA/irrigationprescmod' + self.name + self.crop +str(days)+ 'consensus.IRR'
        else:
            path2 = '../AQUACROP/ACApp/DATA/irrigationprescmod'+self.name+self.crop+str(days)+'.IRR'
        shutil.copyfile(path1, path2)
        i = 0
        p = os.path.abspath('..')

        filedata = open(path1, "r+", encoding="cp1252")

        output = open(path2, "w+", encoding="cp1252", newline='\r\n')

        a=["","",""]
        i=0
        for line in filedata:
            line = str(line)
            i+=1
            if i>=9:
                break
            else:
                output.write(line)

        total=0
        for i in range(len(self.presc)):


            if (i+1)%days==0:

                a[1] = str(round(total+self.presc[i]))
                a[0] = str(i+1 )
                a[2] = "0.5"

                line = "     " + a[0] + "        " + a[1] + "          " + a[2]
                print(line)

                output.write(line+'\n')

                total=0
            else:
                total=total+self.presc[i]

        output.close()

        pass

def get_Et0(Et0_file, initial_day,days):
    file_path='../AQUACROP/ACApp/DATA/'
    filedata = open(file_path+Et0_file, "r+", encoding="cp1252")
    i=0
    Eto_list=[]
    for line in filedata:
        i+=1
        if i>=9:
            Eto_list.append(float(line))
    filedata.close()
    #print(Eto_list)
    Eto_crop_list=[]
    for single_date in (initial_day + timedelta(day) for day in range(days)):
        #Eto_crop_list.append(Eto_list[single_date.timetuple().tm_yday-1])
        Eto_crop_list.append(Eto_list[single_date.month - 1])

    return Eto_crop_list

    
def get_rain(rain_file,initial_day,days):
    file_path = '../AQUACROP/ACApp/DATA/'
    filedata = open(file_path+rain_file, "r+", encoding="cp1252")
    i=0
    rain_list=[]
    for line in filedata:
        i+=1
        if i>=9:
            try:
                rain_list.append(float(line))
            except:
                pass

    filedata.close()
    #print(rain_list)
    rain_crop_list=[]
    for single_date in (initial_day + timedelta(day) for day in range(days)):
        rain_crop_list.append(rain_list[single_date.timetuple().tm_yday-1])

    return rain_crop_list



if __name__ == "__main__":
    global agent
    name= sys.argv[1]
    passwrd= sys.argv[2]
    cropdata = sys.argv[3]
    crop,days,resilience=cropdata.split(',')
    resilience=float(resilience)
    days=int(days)
    area = float(sys.argv[4])  # [Ha]
    initial_day = datetime.strptime(sys.argv[5], '%d-%m-%Y')
    Dp=float(sys.argv[6]) #[mm/day]
    irr=float(sys.argv[7])  # [mm/day]

    Et0_list= get_Et0(sys.argv[8],initial_day,days)
    rainfall_list = get_rain(sys.argv[9],initial_day,days) #[mm/day]
    rainfall_flag = bool(int(sys.argv[10]))
    agent = EvapotranspirationAgent(name,passwrd,crop,area,resilience)

    agent.loadneighbors(name)
    agent.evapotranspirationout(initial_day,days,Et0_list)
    presc=[]



    agent.ir=1
    agent.start()
    while agent.is_alive():
        try:
            time.sleep(3)
            presc = agent.getpresc(initial_day, days, rainfall_list, rainfall_flag, Dp, irr, True)
            agent.getwater()
        except KeyboardInterrupt:
            #print(receiveragent.received)

            agent.save_presc(False,1)
            agent.save_presc(False,5)
            agent.save_presc(False,10)
            presc = agent.getpresc(initial_day, days, rainfall_list, rainfall_flag, Dp, irr, True)
            agent.save_presc(True,1)
            agent.save_presc(True,5)
            agent.save_presc(True,10)
            agent.getwater()
            agent.stop()
            break
    print("Agents finished")






