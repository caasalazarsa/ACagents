import time
import datetime
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, TimeoutBehaviour
from spade.message import Message


class TimeoutSenderAgent(Agent):
    class InformBehav(TimeoutBehaviour):
        async def run(self):
            print(f"TimeoutSenderBehaviour running at {datetime.datetime.now().time()}")
            msg = Message(to="agent2@localhost")  # Instantiate the message
            msg.body = "Hello World"  # Set the message content

            await self.send(msg)

        async def on_end(self):
            self.agent.stop()

    def setup(self):
        print(f"TimeoutSenderAgent started at {datetime.datetime.now().time()}")
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        b = self.InformBehav(start_at=start_at)
        self.add_behaviour(b)


class ReceiverAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 10 seconds")
                self.kill()

        async def on_end(self):
            self.agent.stop()

    def setup(self):
        b = self.RecvBehav()
        self.add_behaviour(b)


if __name__ == "__main__":
    receiveragent = ReceiverAgent("agent2@localhost", "agent234")
    receiveragent.start()
    time.sleep(1) # wait for receiver agent to be prepared. In next sections we'll use presence notification.
    senderagent = TimeoutSenderAgent("agent1@localhost", "agent123")
    senderagent.start()

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break
    print("Agents finished")
