"""
    Code to train intent classification model
"""
import numpy as np
from sklearn.linear_model import LogisticRegression

from tinybot.trainer import Model
from tinybot.config import Config
from tinybot.dataset import parse_intents_to_classification_dataset




class IntentClassifier(Model):
    def __init__(self, classifier_head) -> None:
        self.classifier = classifier_head
        self.clr_head = self.__get_classification_head(classifier_head)
        self.label_mapping = {}

    def __get_classification_head(self, classifier):
        all_classifier_heads = {
            "logistics-regression" : LogisticRegression(max_iter=Config.max_training_iter)
        } 

        return all_classifier_heads.get(classifier)


    def __load_dataset(self, dataset, bert_encoder):

        data_dict = dataset.get_training_dataset("pt", True)
        features = self.get_feature_vectors(data_dict["input_ids"], data_dict["attention_mask"], bert_encoder)
        
        return features, data_dict["labels"]


    def train(self, dataset, bert_encoder):
        self.label_mapping = dataset._map_idx_to_label
        dataset = self.__load_dataset(dataset, bert_encoder)
        self.clr_head.fit(dataset[0], dataset[1])


    def predict(self, query, tokenizer, bert_encoder):
        tokens = query.tokenize(tokenizer, "pt", True)
        features = self.get_feature_vectors(tokens["input_ids"], tokens["attention_mask"], bert_encoder)

        preds = self.clr_head.predict_proba(features)
        idx = np.argmax(preds)
        return self.label_mapping[idx], preds[0][idx]   # return class and probablity