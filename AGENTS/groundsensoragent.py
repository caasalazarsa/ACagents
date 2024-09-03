import time
import numpy as np
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 14:27:31 2018

@author: precision
"""

import subprocess
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import os
 


import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour, TimeoutBehaviour
from spade.message import Message

import sys
import random


class SenderAgent(Agent):

    neighbors=[]
    neighborvalues={}
    class InformandReceiveBehav(CyclicBehaviour):
        async def run(self):
            #print("InformBehav running")
            for neighbor in self.agent.neighbors:
             msg = Message(to=neighbor)     # Instantiate the message
             msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
             msg.set_metadata("ontology", "myOntology")  # Set the ontology of the message content
             msg.set_metadata("language", "OWL-S")       # Set the language of the message content
             msg.body = str(self.agent.ir)                  # Set the message content

             await self.send(msg)
             #print("Message sent!")

             #print("RecvBehav running")

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
              #print("Message received with content: {}".format(msg.body))
              self.agent.neighborvalues[str(msg.sender)]=float(msg.body)
              #print(self.agent.neighborvalues)
              
              self.agent.consensus()
            else:
                print("Did not received any message after 10 seconds")

    def loadneighbors(self,itself):
        with open('list.txt') as f:
            lines = f.read().splitlines()
            lines.remove(itself)
            self.neighbors=lines
            print(self.neighbors)


    def setup(self):
        print("SenderAgent started")
        self.presc=0
        self.b = self.InformandReceiveBehav()
        self.add_behaviour(self.b)

    def consensus(self):
        if len(self.neighborvalues)!=0:
           dx=-len(self.neighborvalues)*self.ir
           #print(dx)
           for neighbor in self.neighborvalues:
              dx=dx+self.neighborvalues[neighbor]
           self.ir=self.ir+.005*dx

    def getpresc(self,FC,PWP,coef):
        TAW=FC-PWP
        RAW=TAW*coef
        self.presc=-1*(self.ir*(TAW-RAW)-TAW)/100*100
        FC_mm=FC/100*100 #[mm]
        RAW_mm=RAW/100*100
        TAW_mm=TAW/100*100
        print("Field Capacity: "+str(FC_mm))
        print("humidity + presc: "+str(self.moist+self.presc))
        if(abs(self.moist+self.presc-FC_mm)<0.01):
           print("prescripción válida")

        else:
            self.presc=0

        datd=(FC-PWP)/100*100



        
          
        print(self.presc)

    def sensing(self,moist):
        self.moist=moist

    def getwater(self,area):
        presc_cm=self.presc*30*0.1 #[cm/month]
        area_cm2=area*1*10**8#[cm2/month]
        water=presc_cm*area_cm2/1000
        print("Cantidad de agua por mes en L: "+str(water))



if __name__ == "__main__":
    agent = SenderAgent(sys.argv[1], sys.argv[2])
    FC = float(sys.argv[3])
    PWP = float(sys.argv[4])
    coef = float(sys.argv[5])
    area = float(sys.argv[6])#[Ha]
    agent.loadneighbors(sys.argv[1])
    agent.sensing(40)
    agent.ir=random.uniform(.75, 1.25)
    agent.start()

    while agent.is_alive():
        try:
            time.sleep(3)  
            agent.getpresc(FC,PWP,coef)
            agent.getwater(area)
        except KeyboardInterrupt:
            #print(receiveragent.received)
            receiveragent.stop()
            break
    print("Agents finished")


