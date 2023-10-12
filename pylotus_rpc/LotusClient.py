from pylotus_rpc.methods import state

class LotusClient:

    def __init__(self, connector):
        self.connector = connector
        self.State = self.State(connector)

    class State:

        def __init__(self, connector):
            self.connector = connector

        def get_chain_head(self):
            return state._get_chain_head(self.connector)
