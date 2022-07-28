
__all__ = ["BlockBase"]


class BlockBase:
    def __init__(self, type, response, rich_response) -> None:
        """ Base class for all the blocks
        """
        self.type = type
        self.response = response
        self.rich_response = rich_response
        self.stop_traversing = False  # flag to control the flow

    def __compile_rich_response(self, rich_response):
        """Print rich response on CMD
            #TODO: use color coded response 
        """
        compiled_responses = []

        for type, content in rich_response.items():
            if type == "quick_replies":
                if len(content) > 0:
                    res = "["+ "] [".join(content) +"]"
                    compiled_responses.append(f" \t   {res}")
            # TODO: Add support for other rich responses
        
        return compiled_responses
            

    def compile_response(self, agent_name):
        # TODO: response formating
        compiled_responses = []
        compiled_responses.append(f"{agent_name} \t >> {self.response}")

        compiled_responses += self.__compile_rich_response(self.rich_response)

        return compiled_responses
    