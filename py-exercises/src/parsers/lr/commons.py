from parsers.lr.lr_types import LRState

def state_to_str(state: LRState) -> str:
    res = ""
    for el in state:
        rule = el.rule
        res += f"{rule.lhs} -> " + " ".join(rule.rhs) + "<br>"
    return res