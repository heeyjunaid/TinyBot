"""
    Trainer to train classifier head
"""

from transformers import BertModel, BertTokenizer


from tinybot.config import Config
from tinybot.dataset import Dataset
from tinybot.trainer import IntentClassifier, Similarity, similarity
from tinybot.dataset import parse_intents_to_classification_dataset


__all__ = ["Trainer"]


class Trainer:
    def __init__(self) -> None:
        # loading tokenizer and encoder
        self.tokenizer = BertTokenizer.from_pretrained(Config.bert_model)
        self.bert_encoder = BertModel.from_pretrained(Config.bert_model)
        

    def train_intent_classifier(self, intent_dataset, clr_head, save_path):

        sentences, labels = parse_intents_to_classification_dataset(intent_dataset)

        dataset = Dataset(sentences, labels, self.tokenizer)

        intent_classifier = IntentClassifier(clr_head)
        intent_classifier.train(dataset, self.bert_encoder)
        intent_classifier.save(save_path)

        # q1 = Queries(["I want to check my schedule"])
        # q2 = Queries(["can you book a hotel for me?"])
        # q3 = Queries(["hello there"])

        # print("pred ", intent_classifier.predict(q1, tokenizer, bert_encoder))
        # print("pred ", intent_classifier.predict(q2, tokenizer, bert_encoder))
        # print("pred ", intent_classifier.predict(q3, tokenizer, bert_encoder))


        return intent_classifier
    

    def train_semantic_similarity_model(self, faq_pairs, save_path):
        
        questions = list(faq_pairs.keys())
        answers = list(faq_pairs.values())

        dataset = Dataset(questions, answers, self.tokenizer, True)
        
        similarity_matcher = Similarity()
        similarity_matcher.train(dataset, self.bert_encoder)
        similarity_matcher.save(save_path)

        # q1 = Queries(["dialogflow is best"])
        # ans = similarity_matcher.predict(q1, self.tokenizer, self.bert_encoder, 0.9)
        # print(ans)

    def train_contextual_slot_detection_model(self,):
        pass