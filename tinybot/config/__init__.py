"""All config required by tiny-bot"""

import dataclasses


__all__ = ["Config"]


@dataclasses.dataclass
class Config:
    bert_model = "bert-base-uncased"
    classifier_head = "logistics-regression"
    model_caching_dir = "models"
    max_training_iter = 200 # max training iteration for ML model