from typing import List

__all__ = ["Labels"]

class Labels:
    """
        base class for labels
    """
    def __init__(self, labels : List[str], is_kb = False) -> None:
        self._labels = labels if is_kb else set(labels)
        self._map_idx_to_label = {k: v for k, v in enumerate(self._labels)}
        self._map_label_to_idx = {v: k for k, v in self._map_idx_to_label.items()}

    def idx_to_label(self, idx) -> str:
        return self._map_idx_to_label.get(idx, None)

    def label_to_idx(self, label) -> str:
        return self._map_label_to_idx.get(label, None)

    def __len__(self) -> int:
        return len(self._labels)
    
    def __repr__(self) -> str:
        # TODO: print table of key value pair
        return ""