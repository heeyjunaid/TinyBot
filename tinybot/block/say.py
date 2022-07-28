from tinybot.block import BlockBase


__all__ = ["SayBlock"]

class SayBlock(BlockBase):
    def __init__(self, response) -> None:
        super().__init__("", response)