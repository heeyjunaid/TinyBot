from typing import List

__all__ = ["Queries"]


class Queries:
    def __init__(self, queries : List[str] ) -> None:
        """
            class representing query
        """
        self.queries = queries

    def tokenize(self, tokenizer, return_tensors : str, padding : bool = True):
        """ Tokenize query based using given tokenizer.
            if tokenizer is not given it just split string into list of words
        """
        if tokenizer is not None:
            if not return_tensors:
                return tokenizer(self.queries, padding = padding)

            if return_tensors == "pt":
                return tokenizer(self.queries, return_tensors = return_tensors, padding = padding)
            else:
                raise Exception("Only PyTorch type of tensor can be returned.")
                    
        return {"tokens" : q.split() for q in self.queries}

    def __len__(self) -> int:
        return len(self.queries)
    
    def __repr__(self) -> str:
        return "\n".join(self.queries)

    