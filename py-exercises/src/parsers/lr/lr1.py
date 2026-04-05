from functools import cached_property

from parsers.base_parser import ParserPrintStyler
from parsers.lr.lr0 import LR0Parser
from parsers.lr.lr_types import (
    LRParsingTable,
    LRAction,
    LRItem,
    LRState,
    are_states_equal_wo_lookahead,
    IndexedLREdge,
)


class LR1Parser(LR0Parser):
    def __init__(self, styling: ParserPrintStyler | None = None, end_symbol: str = "$"):
        super().__init__(styling=styling, end_symbol=end_symbol)

    def goto(self, i: LRState, x: str) -> LRState:  # type: ignore[override]
        j = frozenset([el.advance_dot() for el in i if el.peek_after_dot() == x])
        return self.closure(j)

    def closure(self, i: LRState) -> LRState:  # type: ignore[override]
        while True:
            new_i: set[LRItem] = set(i)
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
                        new_i.add(LRItem(rule=rule, dot_pos=0, lookahead=w))
            if len(new_i) == len(i):
                break
            i = frozenset(new_i)
        return frozenset(i)

    def get_start_states(self):
        start_rule = self.get_start_rule()
        return set(
            [
                self.closure(
                    frozenset([LRItem(rule=start_rule, dot_pos=0, lookahead=None)])
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
                if item.is_dot_at_end() and item.lookahead is not None:
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

    def to_lalr(self) -> LR1Parser:
        mapping: dict[int, int] = dict()

        len_states = len(self.states)
        for fidx in range(len_states):
            for sidx in range(fidx + 1, len_states):
                if are_states_equal_wo_lookahead(self.states[fidx], self.states[sidx]):
                    mapping[sidx] = fidx

        new_edges = set()
        for edge in self.edges:
            if (new_idx := mapping.get(edge.to)) is not None:
                new_edges.add(IndexedLREdge(from_=edge.from_, to=new_idx, symbol=edge.symbol))
            else:
                new_edges.add(edge)

        self.edges = new_edges
        self.states = {k: v for k, v in self.states.items() if k not in mapping.keys()}

        return self


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
