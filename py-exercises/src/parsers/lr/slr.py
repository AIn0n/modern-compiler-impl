from functools import cached_property

from parsers.lr.lr_types import LRParsingTable, LRAction
from parsers.lr.lr0 import LR0Parser
from parsers.example_grammars import GRAMMAR_3_23


class SLRParser(LR0Parser):
    @cached_property
    def parsing_table(self) -> LRParsingTable:
        """
        Returns parsing table for given grammar. Table is row-first, and the
        first dict is representing the states number, dict inside it stores
        symbols and actions mapping.
        """
        self.compute_states_and_edges()
        self.compute_first_follow_nullable()

        rule_lookup = {r: i for i, r in self.indexed_rules.items()}
        t: LRParsingTable = {
            i: {sym: set() for sym in self.symbols} for i in self.states.keys()
        }
        for idx, i in self.states.items():
            for item in i:
                if item.is_dot_at_end():
                    rule_idx = rule_lookup[item.to_rule()]
                    for non_term in self.follow[item.rule.lhs]:
                        t[idx][non_term].add(LRAction.reduce(rule_idx))
                if item.peek_after_dot() == self.eol:
                    t[idx][self.eol].add(LRAction.accept())

        for edge in self.edges:
            action = LRAction.shift if edge.symbol in self.terminals else LRAction.goto
            t[edge.from_][edge.symbol].add(action(edge.to))

        return t


if __name__ == "__main__":
    p = SLRParser()
    p.add_rules(*GRAMMAR_3_23)
    print(p.to_tabulate())
