from .lr0 import LR0Parser
from .slr import SLRParser
from .lr_types import LRAction, LRActionEnum


class LREngine:
    def __init__(self, p: LR0Parser | SLRParser) -> None:
        self.indexed_rules = p.indexed_rules
        self.table = p.parsing_table
        self.start_state: int = p.get_starting_state_idx()

    def parse(self, input_: list[str]) -> dict:
        stack: list[str | dict] = []
        state = self.start_state

        for el in input_:
            actions = self.table[state][el]
            # Given the valid grammar for LR parser, actions should have inside
            # only one action. We check it, if that's true we unpack the value
            # TODO: that's suboptimal, also creating the collection from set
            # seems to me like wild idea in terms of memory

            assert len(actions) == 1, f"{actions=}, {state=}, input={el}"
            action = [*actions][0]

            match action:
                case LRAction(type_=LRActionEnum.ACCEPT):
                    return stack[0]
                case LRAction(type_=LRActionEnum.GOTO, to=n):
                    state = n
                case LRAction(type_=LRActionEnum.REDUCE, to=n):
                    rule = self.indexed_rules[n]
                    reduced = {}
                    for el in reversed(rule.rhs):
                        reduced[el] = stack.pop()
                    stack.append({rule.lhs: reduced})
                case LRAction(type_=LRActionEnum.SHIFT, to=n):
                    state = n
                    stack.append(el)
