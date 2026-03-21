from tabulate import tabulate

from typing import Optional
from functools import cached_property

from parsers.base_parser import ParserPrintStyler, BaseParser, RuleType
from parsers.lr.lr_types import (
    LRAction,
    LREdge,
    LRItem,
    LRState,
    IndexedLREdge,
    LRParsingTable,
)


class LR0Parser(BaseParser):
    def __init__(
        self, styling: Optional[ParserPrintStyler] = None, end_symbol: str = "$"
    ):
        super().__init__(styling=styling)
        self.eol = end_symbol
        self.states: dict[int, LRState] = dict()
        self.edges: set[IndexedLREdge] = set()

    @cached_property
    def indexed_rules(self) -> dict[int, RuleType]:
        return {k: v for k, v in enumerate(self.rules)}

    def get_start_rule(self) -> RuleType:
        """
        start rule for production of LR(0) will be the rule, where you have end
        symbol at the end, by default let it be dollar sign, exactly like in the
        book
        """
        start = [el for el in self.rules if len(el.rhs) and el.rhs[-1] == self.eol]
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

    def get_starting_state_idx(self) -> int:
        start_item = LRItem.from_rule(self.get_start_rule())
        for idx, state in self.states.items():
            if start_item in state:
                return idx

        assert False

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

        self.states = {idx: state for idx, state in enumerate(t)}
        lookup = {v: k for k, v in self.states.items()}
        self.edges = set(map(lambda x: x.convert_to_indexed(lookup), e))

    @cached_property
    def symbols(self) -> set[str]:
        return self.terminals | self.non_terminals

    @cached_property
    def parsing_table(self) -> LRParsingTable:
        """
        Returns parsing table for given grammar. Table is row-first, and the
        first dict is representing the states number, dict inside it stores
        symbols and actions mapping.
        """
        self.compute_states_and_edges()

        rule_lookup = {r: i for i, r in self.indexed_rules.items()}
        t: LRParsingTable = {
            i: {sym: set() for sym in self.symbols} for i in self.states.keys()
        }
        for idx, i in self.states.items():
            for item in i:
                if item.is_dot_at_end():
                    rule_idx = rule_lookup[item.to_rule()]
                    for non_term in self.terminals:
                        t[idx][non_term].add(LRAction.reduce(rule_idx))
                if item.peek_after_dot() == self.eol:
                    t[idx][self.eol].add(LRAction.accept())

        for edge in self.edges:
            action = LRAction.shift if edge.symbol in self.terminals else LRAction.goto
            t[edge.from_][edge.symbol].add(action(edge.to))

        return t

    def _table_cell2str(self, c: set[LRAction]) -> str:
        return ", ".join(map(str, c))

    def to_tabulate(self) -> str:
        list_table = []
        # columns in the same order like in book - first terminals
        headers = [*self.terminals, *self.non_terminals]
        for idx, row in self.parsing_table.items():
            r: list[int | str] = [idx]
            for col in headers:
                r.append(self._table_cell2str(row[col]))
            list_table.append(r)

        return tabulate(list_table, headers=[""] + headers, tablefmt="simple_grid")
