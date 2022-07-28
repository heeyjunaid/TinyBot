from numpy import block
from tinybot.state_manager import StateBase


__all__ = ["StateManager"]


class StateManager(StateBase):
    def __init__(self, agent_name, flows, nlu_settings, intent_classifier_path, similarity_model_path) -> None:
        """ Class Manages state of the TinyBot
        """
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

        if intent != "default_fallback" and self.intent_flow_mapping.get(intent, None):
            # start that flow
            pass

        # continue previous flow
        return self.process_flow_and_block()

    
    def process_event(self, event):
        if event == "event.welcome":
            self.current_flow = 0
            self.current_block = 0


    
    def process_flow_and_block(self):
        flw = self.flows[self.current_flow]
        block = flw["blocks"][self.current_block]
        block = self.init_block(block["type"], block["response"], block["rich_response"])

        return block.compile_response(self.agent_name)

        