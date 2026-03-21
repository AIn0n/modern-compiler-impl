from dataclasses import dataclass

from parsers.base_parser import ParserPrintStyler, RuleType
from parsers.lr.lr0 import LR0Parser

@dataclass(slots=True, frozen=True)
class LR1Item:
    """
    A bit different than item from LR0 - it have additional info about lookahead.
    Also here, I will probably manage to solve better the dot - rather than using
    real symbol inside the rule, I will store it only as a index, indicating
    position inside the right-hand side of the rule. I can always add it
    during the printing.
    """
    rule: RuleType
    # Assume 0 dot_pos is dot on the beginning of rhs
    # R -> . A B C
    # dot_pos = 0
    # R -> A . B C
    # dot_pos = 1
    # and so on...
    dot_pos: int
    lookahead: str

    def peek_after_dot(self) -> str | None:
        if self.dot_pos >= len(self.rule.rhs):
            return None
        return self.rule.rhs[self.dot_pos]

    def advance_dot(self) -> LR1Item:
        return LR1Item(rule=self.rule, dot_pos=self.dot_pos + 1, lookahead=self.lookahead)


LR1State = frozenset[LR1Item]


class LR1Parser(LR0Parser):
    def __init__(self, styling: ParserPrintStyler | None = None, end_symbol: str = "$"):
        super().__init__(styling=styling, end_symbol=end_symbol)

    def goto(self, i: LR1State, x: str) -> LR1State:
        j = frozenset([el.advance_dot() for el in i if el.peek_after_dot() == x])
        return self.closure(j)
    
    def closure(self, i: LR1State) -> LR1State:
        while True:
            new_i: set[LR1Item] = set(i)
            for item in i:
                x: str | None = item.peek_after_dot()
                if x is None or x in self.terminals:
                    continue
                for rule in self.rules:
                    ...