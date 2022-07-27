import numpy as np
from numpy.linalg import norm

from tinybot.trainer import Model


__all__ = ["Similarity"]


class Similarity(Model):
    def __init__(self) -> None:
        """
            Model to perform semantic similarity
        """
        self.indexed_question_vectors = []
        self.ans_mapping = {}


    def __load_dataset(self, dataset, bert_encoder):

        data_dict = dataset.get_training_dataset("pt", True)
        features = self.get_feature_vectors(data_dict["input_ids"], data_dict["attention_mask"], bert_encoder)
        
        return features, data_dict["labels"]


    def __calculate_similarity_score(self, query):
        
        numerator = np.dot(self.indexed_question_vectors, query)
        denom = norm(self.indexed_question_vectors, axis=1)*norm(query)

        return numerator/denom


    def train(self, dataset, bert_encoder):
        self.ans_mapping = dataset._map_idx_to_label
        encoded_faq, _ = self.__load_dataset(dataset, bert_encoder)
        self.indexed_question_vectors = encoded_faq
    

    def predict(self, query, tokenizer, bert_encoder, threshold):
        tokens = query.tokenize(tokenizer, "pt", True)
        features = self.get_feature_vectors(tokens["input_ids"], tokens["attention_mask"], bert_encoder)

        # features is of shape [1x768]
        features = np.squeeze(features, 0) #[768]

        similarity_score = self.__calculate_similarity_score(features)

        idx = np.argmax(similarity_score)
        
        if similarity_score[idx] > threshold:
            return self.ans_mapping[idx], similarity_score[idx]
        
        return "no match", 0



