import time

from spade.agent import Agent
from spade.message import Message
from spade.behaviour import FSMBehaviour, State

STATE_ONE = "STATE_ONE"
STATE_TWO = "STATE_TWO"
STATE_THREE = "STATE_THREE"


class ExampleFSMBehaviour(FSMBehaviour):
    async def on_start(self):
        print(f"FSM starting at initial state {self.current_state}")

    async def on_end(self):
        print(f"FSM finished at state {self.current_state}")
        self.agent.stop()


class StateOne(State):
    async def run(self):
        print("I'm at state one (initial state)")
        msg = Message(to="agent1@localhost")
        msg.body = "msg_from_state_one_to_state_three"
        await self.send(msg)
        self.set_next_state(STATE_TWO)


class StateTwo(State):
    async def run(self):
        print("I'm at state two")
        self.set_next_state(STATE_THREE)


class StateThree(State):
    async def run(self):
        print("I'm at state three (final state)")
        msg = await self.receive(timeout=5)
        print(f"State Three received message {msg.body}")
        # no final state is setted, since this is a final state


class FSMAgent(Agent):
    def setup(self):
        fsm = ExampleFSMBehaviour()
        fsm.add_state(name=STATE_ONE, state=StateOne(), initial=True)
        fsm.add_state(name=STATE_TWO, state=StateTwo())
        fsm.add_state(name=STATE_THREE, state=StateThree())
        fsm.add_transition(source=STATE_ONE, dest=STATE_TWO)
        fsm.add_transition(source=STATE_TWO, dest=STATE_THREE)
        self.add_behaviour(fsm)


if __name__ == "__main__":
    fsmagent = FSMAgent("agent1@localhost", "agent123")
    fsmagent.start()

    while fsmagent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            fsmagent.stop()
            break
    print("Agent finished")
