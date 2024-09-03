import time
import asyncio
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour, TimeoutBehaviour
from spade.message import Message
from spade.template import Template
import numpy as np
import sys
import matplotlib.pyplot as plt

prev={}
actual={}

class ReceiverAgent(Agent):

    def __init__(self,name,password,factor):
        Agent.__init__(self, name, password)
        self.neighbors=[]
        self.factor=float(factor)


    def loadneighbors(self, itself):
        with open('list.txt') as f:
            lines = f.read().splitlines()
            lines.remove(itself)
            self.neighbors = lines
            print(self.neighbors)


    class RecvBehav(CyclicBehaviour):
        async def run(self):
            #print("RecvBehav running")

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:

                #print("Message received with content: {}, from: {}
                info=msg.body.split('/')
                self.agent.received[str(msg.sender)]=[float(info[0]),float(info[1])]
			
            else:
                print("Did not received any message after 10 seconds")

    class InformBehav(OneShotBehaviour):
        async def run(self):
                await asyncio.sleep(20)
                # print("InformBehav running")
                for neighbor in self.agent.neighbors:
                    msg = Message(to=neighbor)  # Instantiate the message
                    msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                    msg.set_metadata("ontology", "myOntology")  # Set the ontology of the message content
                    msg.set_metadata("language", "OWL-S")  # Set the language of the message content
                    msg.body = "Factor:"+str(self.agent.factor)  # Set the message content

                    await self.send(msg)
                        # print("Message sent!")

                        # print("RecvBehav running")


            # stop agent from behaviour
            #self.agent.stop()

    def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        c = self.InformBehav()
        self.received={}
        template=Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b,template)
        self.add_behaviour(c)




if __name__ == "__main__":

    receiveragent = ReceiverAgent(sys.argv[1],sys.argv[2],sys.argv[3])
    receiveragent.loadneighbors(sys.argv[1])
    receiveragent.start()
    time.sleep(2) # wait for receiver agent to be prepared. In next sections we'll use presence notification.
    fig=plt.figure(1)
    plt.title("Convergencia en los valores de estrés del cultivo")
    plt.ylabel("Estrés")
    plt.xlabel("Tiempo (s)")
    ax=fig.gca()
    plt.ylim(.5,1.5)
    t=0
    prevflag=False
    water=0
    while receiveragent.is_alive():
        try:
             if prevflag==False:
                if receiveragent.received:
                    prev=receiveragent.received.copy()
                    prevflag=True
             else:

                if prev:
                  actual=receiveragent.received.copy()
                  for key in prev.keys():
                    

                    plt.plot([t,t+1],[prev[key][0],actual[key][0]],'C'+str(list(prev.keys()).index(key)),label=key)
                    plt.legend(prev.keys())


                  plt.show(block=False)
                  plt.pause(0.001)
                  water = 0
                  for element in actual.values():
                    water = water + element[1]



                prev=actual.copy()
                t=t+1
             time.sleep(1)
             print("Me pidieron: " + str(water))
            
           
        except KeyboardInterrupt:
            print(receiveragent.received)
            receiveragent.stop()
            break
    plt.savefig(sys.argv[1] + '.png')
    print("Agents finished")
