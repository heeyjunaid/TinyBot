import re


__all__ = ["BlockBase"]


class BlockBase:
    def __init__(self, type, response, rich_response, context = {}) -> None:
        """ Base class for all the blocks
        """
        self.type = type
        self.response = response
        self.rich_response = rich_response
        self.stop_traversing = False  # flag to control the flow
        self.context = context

    def update_context(self, context):
        self.context.update(context)

    def get_context(self):
        return self.context

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

    
    def __format_response(self, response):
        slot_regex = r"\$\{[\S]+\}"
        matched_slots = re.findall(slot_regex, response)
        for slot in matched_slots:
            key = slot[2:-1]
            slot_val = self.context.get(key, None)
            # print(slot, key, slot_val, self.context)
            if slot_val is not None:
                response = response.replace(slot, slot_val)
        
        return response


    def compile_response(self, agent_name):
        # TODO: response formating
        compiled_responses = []
        response = self.__format_response(self.response)
        compiled_responses.append(f"{agent_name} \t >> {response}")

        compiled_responses += self.__compile_rich_response(self.rich_response)

        return compiled_responses
    