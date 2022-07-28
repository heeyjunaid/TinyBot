from tinybot.block import BlockBase

__all__ = ["AskBlock"]


class AskBlock(BlockBase):
    def __init__(self,  response, rich_response, slots_to_detect = [], context = {}) -> None:
        self.slots_to_detect = slots_to_detect
        self.question_asked = False
        super().__init__("ask", response, rich_response, context)
    
    def detect_slots(self, query):
        """ Function to detect slot on given query 
        """
        # TODO: Add support for slot detection
        if len(self.slots_to_detect) == 0:
            return False

        for slt in self.slots_to_detect:
            self.context[slt] = query

        return True
        