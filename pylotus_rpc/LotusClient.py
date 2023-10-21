from pylotus_rpc.methods import state

class LotusClient:

    def __init__(self, connector):
        self.connector = connector
        self.State = self.State(connector)

    class State:

        def __init__(self, connector):
            self.connector = connector

        def account_key(self, address, tipset=None):
            return state._account_key(self.connector, address, tipset)
        
        def get_chain_head(self):
            return state._get_chain_head(self.connector)
        
        def list_actors(self, tipset):
            return state._list_state_actors(self.connector, tipset)
        
        def get_actor(self, actor_id, tipset=None):
            return state._get_actor(self.connector, actor_id, tipset)
        

                                    
