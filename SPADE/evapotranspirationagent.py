import time
import numpy as np
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class SenderAgent(Agent):



    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="agent2@localhost")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.set_metadata("ontology", "myOntology")  # Set the ontology of the message content
            msg.set_metadata("language", "OWL-S")       # Set the language of the message content
            msg.body = str(self.agent.Kc)                  # Set the message content

            await self.send(msg)
            print("Message sent!")

            # set exit_code for the behaviour
            self.exit_code = "Job Finished!"

            # stop agent from behaviour
            self.agent.stop()

    def setup(self):
        print("SenderAgent started")
        self.b = self.InformBehav()
        self.add_behaviour(self.b)



    def evapotranspirationout(self,Week,Zone):
        self.Occidental=[0.34,0.49,0.55,0.53,0.53,0.5,0.55,0.63,0.68,0.89,0.75,0.75,0.78,0.65,0.62,0.59,0.54,0.55,0.51,0.51,0.53]
        self.Central=[0.41,0.47,0.4,0.42,0.5,0.54,0.73,0.65,0.79,0.93,0.71,0.68,0.75,0.63,0.67,0.7,0.63,0.43,0.33,0.33]
        self.Oriental=[0.36,0.39,0.43,0.43,0.43,0.53,0.59,0.77,0.77,0.8,0.9,0.73,0.66,0.7,0.6,0.34,0.36,0.35,0.55]
        self.Et0=1
        self.Kc=1
        self.Values=[]
        self.State="Desarrollo de hojas"
        if Zone == 0:
           if Week>0 and Week<10 :
                self.State="Desarrollo de hojas"
           if Week>=10 and Week<18 :
                self.State="Bulbificacion"
           if Week>=18 and Week<22 :
                self.State="Maduracion"
           self.Values=self.Occidental

        if Zone == 1:
           if Week>0 and Week<9 :
                self.State="Desarrollo de hojas"
           if Week>=9 and Week<16 :
                self.State="Bulbificacion"
           if Week>=16 and Week<21 :
                self.State="Maduracion"
           self.Values=self.Central

        if Zone == 2:
           if Week>0 and Week<8 :
                self.State="Desarrollo de hojas"
           if Week>=8 and Week<14 :
                self.State="Bulbificacion"
           if Week>=14 and Week<20 :
                self.State="Maduracion"
           self.Values=self.Oriental
	   
        self.Kc=self.Et0*self.Values[Week-1]



		
		




if __name__ == "__main__":
    agent = SenderAgent("agent3@localhost", "agent345")
    agent.evapotranspirationout(13,1)
    print(agent.Kc)
    agent.start()


    while agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            agent.stop()
            break
    print("Agent finished with exit code: {}".format(agent.b.exit_code))

