from dataclasses import dataclass
from functools import cached_property

from parsers.base_parser import ParserPrintStyler, RuleType
from parsers.lr.lr0 import LR0Parser
from parsers.lr.lr_types import LRParsingTable, LRAction


@dataclass(slots=True, frozen=True)
class LR1Item:
    """
    A bit different than item from LR0 - it have additional info about lookahead.
    Also here, I will probably manage to solve better the dot - rather than using
    real symbol inside the rule, I will store it only as a index, indicating
    position inside the right-hand side of the rule.
    """

    rule: RuleType
    # Assume 0 dot_pos is dot on the beginning of rhs
    # R -> . A B C
    # dot_pos = 0
    # R -> A . B C
    # dot_pos = 1
    # and so on...
    dot_pos: int
    lookahead: str | None

    def peek_after_dot(self) -> str | None:
        if self.dot_pos >= len(self.rule.rhs):
            return None
        return self.rule.rhs[self.dot_pos]

    def advance_dot(self) -> LR1Item:
        return LR1Item(
            rule=self.rule, dot_pos=self.dot_pos + 1, lookahead=self.lookahead
        )

    def is_dot_at_end(self) -> bool:
        return self.dot_pos == len(self.rule.rhs)

    def to_rule(self) -> RuleType:
        return self.rule

    def __str__(self) -> str:
        pre_dot = self.rule.rhs[: self.dot_pos]
        post_dot = self.rule.rhs[self.dot_pos :]

        return (
            f"{self.rule.lhs} -> "
            + " ".join([*pre_dot, ".", *post_dot])
            + f" ({self.lookahead})"
        )


LR1State = frozenset[LR1Item]


class LR1Parser(LR0Parser):
    # TODO: Add compute first follow and nullables into the compute states and edges function
    def __init__(self, styling: ParserPrintStyler | None = None, end_symbol: str = "$"):
        super().__init__(styling=styling, end_symbol=end_symbol)

    def goto(self, i: LR1State, x: str) -> LR1State:  # type: ignore[override]
        j = frozenset([el.advance_dot() for el in i if el.peek_after_dot() == x])
        return self.closure(j)

    def closure(self, i: LR1State) -> LR1State:  # type: ignore[override]
        while True:
            new_i: set[LR1Item] = set(i)
            for item in i:
                x: str | None = item.peek_after_dot()
                if x is None or x in self.terminals:
                    continue
                for rule in self.rules:
                    if rule.lhs != x:
                        continue
                    # omitting X, getting all the elements after it
                    b = item.rule.rhs[item.dot_pos + 1 :]
                    z = item.lookahead
                    col = b if z is None else (*b, z)
                    for w in self.first_rhs(col):
                        new_i.add(LR1Item(rule=rule, dot_pos=0, lookahead=w))
            if len(new_i) == len(i):
                break
            i = frozenset(new_i)
        return frozenset(i)

    def get_start_states(self):
        start_rule = self.get_start_rule()
        return set(
            [
                self.closure(
                    frozenset([LR1Item(rule=start_rule, dot_pos=0, lookahead=None)])
                )
            ]
        )

    @cached_property
    def parsing_table(self) -> LRParsingTable:
        """
        Returns parsing table for given grammar. Table is row-first, and the
        first dict is representing the states number, dict inside it stores
        symbols and actions mapping.
        """
        self.compute_first_follow_nullable()
        self.compute_states_and_edges()

        rule_lookup = {r: i for i, r in self.indexed_rules.items()}
        t: LRParsingTable = self._init_parsing_table()
        for idx, i in self.states.items():
            for item in i:
                if item.is_dot_at_end():
                    # main difference from SLR here - we reduce based on
                    # already computed lookahead values
                    # page 64
                    rule_idx = rule_lookup[item.to_rule()]
                    t[idx][item.lookahead].add(LRAction.reduce(rule_idx))
                if item.peek_after_dot() == self.eol:
                    t[idx][self.eol].add(LRAction.accept())

        for edge in self.edges:
            action = LRAction.shift if edge.symbol in self.terminals else LRAction.goto
            t[edge.from_][edge.symbol].add(action(edge.to))

        return t


if __name__ == "__main__":
    grammar_ex_3_7 = [
        "S -> G $",
        "G -> P",
        "G -> P G",
        "P -> id : R",
        "R -> id R",
        "R -> ",
    ]

    parser = LR1Parser()
    parser.add_rules(*grammar_ex_3_7)
    parser.compute_states_and_edges()
    print(parser.to_tabulate())
