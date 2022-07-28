from tinybot.config import Config
from tinybot.state_manager import StateBase


__all__ = ["StateManager"]


class StateManager(StateBase):
    def __init__(self, agent_name, flows, nlu_settings, intent_classifier_path, similarity_model_path) -> None:
        """ Class Manages state of the TinyBot
        """
        self.current_block_object = None
        self.context = {}
        super().__init__(agent_name, flows, nlu_settings, intent_classifier_path, similarity_model_path)


    def process_query(self, query, event = None):
        """Function to process end user query
        """

        if event is not None:
            self.process_event(event)
            return self.process_flow_and_block()
        
        # detect intent
        intent, _, kb_answer = self.detect_intent(query)

        if kb_answer:
            block = self.init_block("say", intent)
            return block.compile_response(self.agent_name)
        
        slot_detected = False
        if self.current_block_object.type == "ask" and self.current_block_object.question_asked:
            slot_detected = self.current_block_object.detect_slots(query)
            
            if slot_detected:
                self.current_block += 1

        elif intent == "default_fallback":
            block = self.init_block("say", Config.fallback_response)
            return block.compile_response(self.agent_name)
        
        if not slot_detected and self.intent_flow_mapping.get(intent, None) is not None:
            # move to some other flow
            self.current_flow = self.intent_flow_mapping.get(intent)
            self.current_block = 0
        

        # continue previous flow
        return self.process_flow_and_block()

    
    def process_event(self, event):
        if event == "event.welcome":
            self.current_flow = 0
            self.current_block = 0


    
    def process_flow_and_block(self):
        flw = self.flows[self.current_flow]

        while True:
            self.current_block_object = flw["blocks"][self.current_block]
            self.current_block_object = self.init_block(self.current_block_object["type"], self.current_block_object["response"], self.current_block_object.get("rich_response", {}),
                                                        self.current_block_object.get("slot", []),  self.context)

            yield self.current_block_object.compile_response(self.agent_name)

            if self.current_block_object.type == "ask":
                self.current_block_object.question_asked = True
                break 
            
            self.current_block += 1
            
            if not self.current_block < len(flw["blocks"]):
                break

        