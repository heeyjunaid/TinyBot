from tinybot.block import BlockBase

__all__ = ["AskBlock"]


class AskBlock(BlockBase):
    def __init__(self,  response, rich_response) -> None:
        super().__init__("ask", response, rich_response)