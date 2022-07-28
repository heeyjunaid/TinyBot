import re
from dataclasses import dataclass

from tinybot.trainer import Model


@dataclass
class CommonRegexPattern:
    """ class containing some common regex patterns
    """
    # TODO: Add regex pattern here
    email = r""
    phone_number = r""
    number = r""
    number_sequence = r""


@dataclass
class SystemSlotTypes:
    email = "regex"
    phone_number = "regex"


class SlotDetector(Model):
    def __init__(self) -> None:
        pass

    def __detect_regex_slot(self, query, regex_pattern):
        pass

    def train(self, dataset, bert_encoder):
        return super().train(dataset, bert_encoder)