from typing import List

from tinybot.dataset.query import Queries
from tinybot.dataset.labels import Labels


__all__ = ["Dataset"]


class Dataset(Queries, Labels):
    def __init__(self, sentences : List[str], labels: List[str], tokenizer) -> None:
        self.sentences = sentences
        self.labels = labels
        self.tokenizer = tokenizer

        Queries.__init__(self, self.sentences)
        Labels.__init__(self, self.labels)


    def get_training_dataset(self, return_tensors = "pt", padding = True):
        """
            return
            {
                "input_ids" : [],
                attention_mask : [],
                token_type_ids: []
                labels : []
            }
        """
        dataset = self.tokenize(self.tokenizer, return_tensors, padding)
        dataset["labels"] = [self.label_to_idx(l) for l in self.labels]

        return dataset

    def __repr__(self) -> str:
        return "\n".join(self.sentences)
    
    def __len__(self) -> int:
        return len(self.sentences)