import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour, TimeoutBehaviour
from spade.message import Message
from spade.template import Template
import numpy as np





class ReceiverAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("RecvBehav running")

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
                self.agent.received.append(float(msg.body))
            else:
                print("Did not received any message after 10 seconds")


            # stop agent from behaviour
            #self.agent.stop()

    def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        self.received=[]
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)




if __name__ == "__main__":
    receiveragent = ReceiverAgent("agent2@localhost", "agent234")
    receiveragent.start()
    time.sleep(2) # wait for receiver agent to be prepared. In next sections we'll use presence notification.

    while receiveragent.is_alive():
        try:
            time.sleep(1)            
        except KeyboardInterrupt:
            print(receiveragent.received)
            receiveragent.stop()
            break
    print("Agents finished")
