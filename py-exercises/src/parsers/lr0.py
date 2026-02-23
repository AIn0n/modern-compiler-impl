from parsers.baseParser import ParserPrintStyler, BaseParser, RuleType
from parsers.example_grammars import GRAMMAR_3_20


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

    def compute_states_and_edges(self):
        t = set(self.closure())


if __name__ == "__main__":
    p = LR0Parser()
    p.add_rules(*GRAMMAR_3_20)
    print(p)
