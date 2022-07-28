import os
from transformers import BertModel, BertTokenizer

from tinybot.config import Config
from tinybot.dataset import Queries
from tinybot.trainer import IntentClassifier, Similarity
from tinybot.block import AskBlock, SayBlock


class StateBase:
    def __init__(self, agent_name, flows, nlu_settings, intent_classifier_path, similarity_model_path) -> None:
        # parse flow
        self.agent_name = agent_name
        self.flows = flows
        self.nlu_settings = nlu_settings
        self.intent_classifier = None
        self.similarity_matcher = None
        self.start_flow_name = None
        self.flow_idx_maping = {}
        self.intent_flow_mapping = {}

        self.current_intent = None
        self.current_slots = {}
        self.current_flow = None
        self.current_block = None
        self.previous_flow = None
        self.previous_block = None

        # loading bert models
        self.tokenizer = BertTokenizer.from_pretrained(Config.bert_model)
        self.bert_encoder = BertModel.from_pretrained(Config.bert_model)

        self.__parse_yaml_to_state(flows)
        self.__load_ml_models(intent_classifier_path, similarity_model_path)

        self.block_type_mapping = {
            "say" : SayBlock,
            "ask" : AskBlock
        }
        

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
    

    def __load_ml_models(self, intent_classifier_path, similarity_model_path):
        if os.path.exists(intent_classifier_path):
            self.intent_classifier = IntentClassifier(Config.classifier_head)
            self.intent_classifier.load(intent_classifier_path)
        else:
            print(f"skipping intent classifier loading path, as the model path {intent_classifier_path} does not exists")

        if os.path.exists(similarity_model_path):
            self.similarity_matcher = Similarity()
            self.similarity_matcher.load(similarity_model_path)
        else:
            print(f"skipping semantic similarity loading path, as the model path {similarity_model_path} does not exists")


    def __answer_from_kb(self, query):
        if self.similarity_matcher is not None:
            return self.similarity_matcher.predict(query, self.tokenizer, self.bert_encoder, self.nlu_settings["faq_threshold"])

        return "no match", 0
            


    def detect_intent(self, query):
        query = Queries([query])

        if self.intent_classifier is not None:
            pred_, prob_ = self.intent_classifier.predict(query, self.tokenizer, self.bert_encoder)

            if prob_ > self.nlu_settings["classifier_threshold"]:
                return pred_, prob_, False

        pred_, prob_ = self.__answer_from_kb(query)

        if prob_ > 0:
            return pred_, prob_, True
        
        
        return "default_fallback", 1.0, False 
         

    def init_block(self, block_type, response, rich_response = {}, slot_to_detect = [], context = {}):
        """ function will initialize respective block
        """
        return self.block_type_mapping[block_type](response, rich_response, slot_to_detect, context)
        

        


