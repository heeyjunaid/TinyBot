import os
import torch
import pickle

__all__ = ["Model"]


class Model:
    def __init__(self) -> None:
        pass

    @torch.no_grad()
    def get_feature_vectors(self, input_ids, attention_mask, bert_encode):
        last_hidden_state = bert_encode(input_ids, attention_mask = attention_mask)

        # using encoded vector of [cls] class as it capture context of sentence
        feature_vector = last_hidden_state[0][:, 0, :].numpy()
        return feature_vector
    
    def train(self, dataset, bert_encoder):
        pass

    def save(self, model_path):
        print(f"saving model to {model_path} ...")
        
        with open(model_path, 'wb') as m:
            pickle.dump(self, m)

        print(f"model saving completed.")

    def load(self, model_path):
        print(f"loading model from {model_path} ...")
        
        with open(model_path, 'wb') as m:
            self = pickle.dump(self, m)
        
        print(f"model loading completed.")

    def predict(self, query):
        pass
    