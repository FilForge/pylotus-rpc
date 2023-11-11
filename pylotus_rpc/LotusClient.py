from pylotus_rpc.methods import state
from pylotus_rpc.methods import chain

class LotusClient:

    def __init__(self, connector):
        self.connector = connector
        self.State = self.State(connector)
        self.Chain = self.Chain(connector)

    class Chain:
        
        def __init__(self, connector):
            self.connector = connector

        def get_block(self, cid):
            return chain._get_block(self.connector, cid)

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
        
        def state_call(self, message, tipset=None):
            return state._state_call(self.connector, message, tipset)
        
        def changed_actors(self, cid1, cid2):
            return state._changed_actors(self.connector, cid1, cid2)
        
        def circulating_supply(self, tipset=None):
            return state._circulating_supply(self.connector, tipset)


                                    
