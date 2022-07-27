from tinybot.dataset.dataset import Dataset
from tinybot.dataset.query import Queries 
from tinybot.dataset.labels import Labels 


__all__ = ["parse_intents_to_classification_dataset"]


def parse_intents_to_classification_dataset(intents_dataset):

    sentences = []
    labels = []

    for label, example in intents_dataset.items():
        if example is not None or len(example) > 0:
            sentences += example
            labels += [label]*len(example)

    return sentences, labels
