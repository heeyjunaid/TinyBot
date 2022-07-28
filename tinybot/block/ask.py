from tinybot.block import BlockBase

__all__ = ["AskBlock"]


class AskBlock(BlockBase):
    def __init__(self, question, response, rich_response) -> None:
        super().__init__(question, response, rich_response)