from spade import agent

class DummyAgent(agent.Agent):
    def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))

dummy = DummyAgent("agent1@localhost", "agent123")
dummy.start()
dummy.web.start(hostname="127.0.0.1", port="10000")

dummy.stop()
