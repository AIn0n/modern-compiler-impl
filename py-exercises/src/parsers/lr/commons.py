from parsers.lr.lr_types import LRState


def state_to_str(state: LRState, linebreak: str | None = None) -> str:
    if linebreak is None:
        linebreak = "<br>"
    res = ""
    for el in state:
        res += str(el) + linebreak
    return res
