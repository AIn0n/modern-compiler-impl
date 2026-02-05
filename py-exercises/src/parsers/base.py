from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from typing import MutableMapping
from tabulate import tabulate


@dataclass(frozen=True, slots=True)
class ParserPrintStyler:
    epsilon: str = "ε"
    hor_line: str = "─"
    pipe_wne: str = "┬"
    pipe_nes: str = "├"
    pipe_ne: str = "└"


class BaseParser:
    def __init__(self, styling: ParserPrintStyler = None) -> None:
        if styling is None:
            styling = ParserPrintStyler()
        self.rules = []
        self.styling = styling

        self.nullables = set()
        self.first: MutableMapping[str, set[str]] = defaultdict(set)
        self.follow: MutableMapping[str, set[str]] = defaultdict(set)

    def add_rule(self, rule: str) -> None:
        lhs, rhs = rule.split("->")
        rhs_list = rhs.strip().split()
        self.rules.append(tuple([lhs.strip(), rhs_list]))

    def add_rules(self, *rules) -> None:
        for rule in rules:
            self.add_rule(rule)

    def _rule_to_str(self, rules: list[str]) -> str:
        return " ".join(rules) if len(rules) else self.styling.epsilon

    def get_all_nonterminals(self) -> set[str]:
        # just get all right hand side symbols
        return set([lhs for lhs, _ in self.rules])

    def get_all_terminals(self) -> set[str]:
        all_rhs_symbols = set(chain.from_iterable([rhs for _, rhs in self.rules]))
        # everything from the rules, except right hands side
        return all_rhs_symbols - self.get_all_nonterminals()

    def _is_sequence_nullable(self, seq: list[str]) -> bool:
        if len(seq) == 0:
            return True
        return all(map(lambda x: x in self.nullables, seq))

    def count_first_follow_nullables(self) -> int:
        return sum(
            map(len, [self.nullables, *self.follow.values(), *self.first.values()])
        )

    def compute_first_follow_nullable(self, one_iteration: bool = False) -> None:
        self.nullables = set()
        self.follow = defaultdict(set)
        self.first = defaultdict(set)

        for terminal in self.get_all_terminals():
            self.first[terminal] = set([terminal])

        while True:
            changed = self.count_first_follow_nullables()
            for x, y in self.rules:
                k = len(y)
                if self._is_sequence_nullable(y):
                    self.nullables.add(x)
                for i in range(k):
                    if self._is_sequence_nullable(y[0:i]):
                        self.first[x] = self.first[x].union(self.first[y[i]])
                    if self._is_sequence_nullable(y[i + 1 :]):
                        self.follow[y[i]] = self.follow[y[i]].union(self.follow[x])
                    for j in range(i + 1, k):
                        if self._is_sequence_nullable(y[i + 1 : j]):
                            self.follow[y[i]] = self.follow[y[i]].union(
                                self.first[y[j]]
                            )
            if one_iteration or (changed == self.count_first_follow_nullables()):
                break

    def build_parsing_table(self):
        terminals = enumerate(self.get_all_terminals())
        self.table = defaultdict(lambda: defaultdict(list))

        for x, y in self.rules:
            for t in self.first[x]:
                self.table[x][t].append((x, y))
            if x in self.nullables:
                for terminal in terminals:
                    self.table[x][terminal].append((x,y))
        tabulate()

    def __str__(self) -> str:
        rules_dict = defaultdict(list)
        for lhs, rhs in self.rules:
            rules_dict[lhs].append(rhs)

        left_pad = max(map(len, rules_dict.keys())) + 1
        offset_sym = self.styling.hor_line
        res = ""
        offset = left_pad * " "
        for k, v in rules_dict.items():
            prefix = f"{k:{offset_sym}<{left_pad}}"
            if len(v) == 1:
                res += f"{prefix}{offset_sym * 2} {self._rule_to_str(v[0])}\n"
                continue

            first, *rest, last = v
            res += f"{prefix}{self.styling.pipe_wne}{offset_sym} {self._rule_to_str(first)}\n"

            for rule in rest:
                res += f"{offset}{self.styling.pipe_nes}{offset_sym} {self._rule_to_str(rule)}\n"

            res += f"{offset}{self.styling.pipe_ne}{offset_sym} {self._rule_to_str(last)}\n"

        return res


if __name__ == "__main__":
    # Example from grammar 3.12
    p = BaseParser()
    p.add_rules(
        "Z -> d",
        "Z -> X Y Z",
        "Y -> ",
        "Y -> c",
        "X -> Y",
        "X -> a",
    )
    p.compute_first_follow_nullable(one_iteration=False)
    non_terminals = p.get_all_nonterminals()
    print(f"{non_terminals=}")
    print(f"nullables = {p.nullables}")
    interesting_first = {k: v for k, v in p.first.items() if k in non_terminals}
    print(f"first = {interesting_first}")
    interesting_follows = {k: v for k, v in p.follow.items() if k in non_terminals}
    print(f"{interesting_follows=}")
    p.build_parsing_table()
