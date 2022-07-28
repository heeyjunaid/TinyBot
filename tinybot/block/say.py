from tinybot.block import BlockBase


__all__ = ["SayBlock"]

class SayBlock(BlockBase):
    def __init__(self, response, rich_repsonse = {}, slot_to_detect = [], context = {}) -> None:
        super().__init__("say", response, rich_repsonse, context)