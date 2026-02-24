from dataclasses import dataclass
from typing import Optional

from parsers.base_parser import ParserPrintStyler, BaseParser, RuleType
from parsers.example_grammars import GRAMMAR_3_20


def swap_with_next(c: tuple, i: int) -> tuple:
    """
    swap tuple i element with the next one, return new tuple
    """
    j = i + 1
    *begin, i_val = c[:j]
    j_val, *end = c[j:]
    return (*begin, j_val, i_val, *end)


@dataclass(slots=True, frozen=True)
class LRItem:
    rule: RuleType
    dot_idx: int

    def peek_after_dot(self) -> Optional[str]:
        """
        Get the first symbol (next to) after the dot. This method is beneficial
        for closure in LR parser. Return None if there's no symbol after the dot.
        """
        next_idx = self.dot_idx + 1
        return None if next_idx >= len(self.rule.rhs) else self.rule.rhs[next_idx]

    def advance_dot(self) -> LRItem:
        """
        Return the copy of the class, with dot moved one position to the right.
        """
        # swap dot with next element after it
        new_rhs = swap_with_next(self.rule.rhs, self.dot_idx)

        return LRItem(
            rule=RuleType(lhs=self.rule.lhs, rhs=new_rhs), dot_idx=self.dot_idx + 1
        )

    @staticmethod
    def from_rule(rule: RuleType) -> LRItem:
        """
        Turn rule into LR item, by default setting the dot at the first position
        on left-hand side.
        """
        return LRItem(rule=RuleType(rule.lhs, tuple([".", *rule.rhs])), dot_idx=0)


LRState = frozenset[LRItem]


@dataclass(slots=True, frozen=True)
class LREdge:
    # TODO: probably it should be done using some sort of hashes, or in some other
    #       way if should explicitly reference LR state (set of LRItems)
    from_: LRState
    to: LRState
    symbol: str


class LR0Parser(BaseParser):
    def __init__(self, styling: ParserPrintStyler | None = None, end_symbol: str = "$"):
        super().__init__(styling=styling)
        self.eol = end_symbol
        self.states: set[LRState] = set()
        self.edges: set[LREdge] = set()

    def get_start_rule(self) -> RuleType:
        """
        start rule for production of LR(0) will be the rule, where you have end
        symbol at the end, by default let it be dollar sign, exactly like in the
        book
        """
        start = [el for el in self.rules if el.rhs[-1] == self.eol]
        # idk if that's valid or not,
        # it seems logical that grammar should not have two rules ending with
        # End of File, but who knows
        assert len(start) == 1

        return start[0]

    def closure(self, i: LRState) -> LRState:
        while True:
            new_i: set[LRItem] = set(i)
            for el in i:
                # closure works only for in cases where next to dot (at X position)
                # is non terminal element. Thanks to this statement we will not
                # unnecessarily scan thru rules
                x: Optional[str] = el.peek_after_dot()
                if x is None or x in self.terminals:
                    continue
                for rule in self.rules:
                    # check lhs
                    if rule.lhs != x:
                        continue
                    new_i.add(LRItem.from_rule(rule))
            # break when I does not change
            if len(new_i) == len(i):
                break
            i = frozenset(new_i)
        return frozenset(i)

    def goto(self, i: LRState, x: str) -> LRState:
        # from page 60-61
        j = frozenset(el.advance_dot() for el in i if el.peek_after_dot() == x)
        return self.closure(j)

    def compute_states_and_edges(self) -> None:
        # first state is just starting rule (one with terminal symbol at end)
        # converted into LR item - rule with dot representing current position
        # at given rule
        start_rule = self.get_start_rule()
        # state collection
        t: set[LRState] = set([self.closure(frozenset([LRItem.from_rule(start_rule)]))])
        # edges collection
        e: set[LREdge] = set()
        while True:
            sizes = len(e) + len(t)
            new_e = set()
            new_t: set[LRState] = set()
            for i in t:
                for item in i:
                    x = item.peek_after_dot()
                    # However, for the symbol $ we do not compute Goto(I, $); instead we will
                    # make an accept action
                    if x is None or x == self.eol:
                        continue
                    j = self.goto(i, x)
                    new_t.add(j)
                    new_e.add(LREdge(from_=i, to=j, symbol=x))
            t.update(new_t)
            e.update(new_e)

            if sizes == len(e) + len(t):
                break

        self.states = t
        self.edges = e


if __name__ == "__main__":
    p = LR0Parser()
    p.add_rules(*GRAMMAR_3_20)

    p.compute_states_and_edges()
    for state in p.states:
        print("=== STATE ===")
        for el in state:
            print(el)
