"""
    Trainer to train classifier head
"""

from transformers import BertModel, BertTokenizer


from tinybot.config import Config
from tinybot.dataset import Dataset
from tinybot.trainer import IntentClassifier
from tinybot.dataset import parse_intents_to_classification_dataset


__all__ = ["Trainer"]


class Trainer:
    def __init__(self) -> None:
        pass

    def train_intent_classifier(self, intent_dataset, clr_head, save_path):

        sentences, labels = parse_intents_to_classification_dataset(intent_dataset)

        # loading tokenizer and encoder
        tokenizer = BertTokenizer.from_pretrained(Config.bert_model)
        bert_encoder = BertModel.from_pretrained(Config.bert_model)
        
        dataset = Dataset(sentences, labels, tokenizer)

        intent_classifier = IntentClassifier(clr_head)
        intent_classifier.train(dataset, bert_encoder)
        intent_classifier.save(save_path)

        # q1 = Queries(["I want to check my schedule"])
        # q2 = Queries(["can you book a hotel for me?"])
        # q3 = Queries(["hello there"])

        # print("pred ", intent_classifier.predict(q1, tokenizer, bert_encoder))
        # print("pred ", intent_classifier.predict(q2, tokenizer, bert_encoder))
        # print("pred ", intent_classifier.predict(q3, tokenizer, bert_encoder))


        return intent_classifier