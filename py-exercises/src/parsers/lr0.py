from parsers.base_parser import ParserPrintStyler, BaseParser, RuleType
from parsers.example_grammars import GRAMMAR_3_20
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class LRItem:
    rule: RuleType
    dot_idx: int

    def next_dot_sym(self) -> str:
        """
        Get the first symbol (next to) after the dot. This method is beneficial
        for closure in LR parser.
        """
        _, lhs = self.rule
        return lhs[self.dot_idx + 1]

    @staticmethod
    def from_rule(rule: RuleType) -> LRItem:
        """
        Turn rule into LR item, by default setting the dot at the first position
        on left-hand side.
        """
        rhs, lhs = rule
        rule_with_dot = (rhs, tuple([".", *lhs]))
        return LRItem(rule=rule_with_dot, dot_idx=0)


class LR0Parser(BaseParser):
    def __init__(self, styling: ParserPrintStyler | None = None, end_symbol: str = "$"):
        super().__init__(styling=styling)
        self.eol = end_symbol

    def get_start_rule(self) -> RuleType:
        """
        start rule for production of LR(0) will be the rule, where you have end
        symbol at the end, by default let it be dollar sign, exactly like in the
        book
        """
        start = [(lhs, rhs) for lhs, rhs in self.rules if rhs[-1] == self.eol]
        # idk if that's valid or not,
        # it seems logical that grammar should not have two rules ending with
        # End of File, but who knows
        assert len(start) == 1

        return start[0]
    
    def closure(self, i: set[LRItem]) -> set[LRItem]:
        while True:
            new_i: set[LRItem] = set(i)
            for el in i:
                # closure works only for in cases where next to dot (at X position)
                # is non terminal element. Thanks to this statement we will not 
                # unnecessarily scan thru rules
                x = el.next_dot_sym()
                if x in self.terminals:
                    continue
                for rule in self.rules:
                    # check rhs
                    # TODO: build class for rule, to easily access rhs and lhs in
                    # named, readable way
                    if rule[0] != x:
                        continue
                    new_i.add(LRItem.from_rule(rule))
            # break when I does not change
            if len(new_i) == len(i):
                break
            i = new_i
        return i


    def compute_states_and_edges(self):
        # state collection
        # first state is just starting rule (one with terminal symbol at end)
        # converted into LR item - rule with dot representing current position
        # at given rule
        start_rule = self.get_start_rule()
        t: set[set[LRItem]] = set(self.closure(set([LRItem.from_rule(start_rule)])))

        # edges collection
        e = set()
        for i in t:
            ...


if __name__ == "__main__":
    p = LR0Parser()
    p.add_rules(*GRAMMAR_3_20)
    
    given_items = p.closure(set([LRItem.from_rule(p.get_start_rule())]))

    print(given_items)
