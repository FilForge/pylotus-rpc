from src.methods import state

class LotusClient:

    def __init__(self, connector):
        self.connector = connector
        self.State = self.State(connector)

    class State:

        def __init__(self, connector):
            self.connector = connector

        def getChainHead(self):
            return state.get_chain_head(self.connector)
