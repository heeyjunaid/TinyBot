

"""
    state 
    - Name
    - start flow
"""


class State:
    def __init__(self, agent_name, flows, nlu_settings) -> None:
        # parse flow
        self.agent_name = agent_name
        self.nlu_settings = nlu_settings

        self.start_flow_name = None
        self.flow_idx_maping = {}
        self.intent_flow_mapping = {}

        self.current_intent = None
        self.current_slots = {}
        self.current_flow = None
        self.current_block = None
        self.previous_flow = None
        self.previous_block = None

        self.__parse_yaml_to_state(flows)
        

    def reset_state_after_response(self):
        """ Reset current state after response """
        self.previous_flow = self.current_flow
        self.previous_block = self.current_block
        self.current_intent = None
        self.current_slots = {}
        self.current_flow = None
        self.current_block = None

    
    def update_state_intent(self, intent):
        self.current_intent = intent
    

    def update_state_slots(self, slots):
        for key, val in slots.items():
            self.current_slots[key] = val

    def __parse_yaml_to_state(self, flow):

        for idx, flw in enumerate(flow):
            if flw.get("is_start_flow", False):
                self.start_flow_name = flw["name"]
            
            self.flow_idx_maping[flw["name"]] = idx

            for intent in flw["trigger_intents"]:
                self.intent_flow_mapping[intent] = idx
    

        
