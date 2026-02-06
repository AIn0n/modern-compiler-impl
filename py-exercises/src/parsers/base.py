from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from typing import MutableMapping
from functools import cached_property

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
        self.rules: list[tuple[str, set[str]]] = []
        self.styling = styling

        self.nullables = set()
        self.first: MutableMapping[str, set[str]] = defaultdict(set)
        self.follow: MutableMapping[str, set[str]] = defaultdict(set)

    @cached_property
    def non_terminals(self) -> list[str]:
        return set([lhs for lhs, _ in self.rules])

    @cached_property
    def terminals(self) -> list[str]:
        all_rhs_symbols = set(chain.from_iterable([rhs for _, rhs in self.rules]))
        # everything from the rules, except right hands side
        return all_rhs_symbols - self.non_terminals

    def add_rule(self, rule: str) -> None:
        lhs, rhs = rule.split("->")
        rhs_list = tuple(rhs.strip().split())
        self.rules.append(tuple([lhs.strip(), rhs_list]))

    def add_rules(self, *rules) -> None:
        for rule in rules:
            self.add_rule(rule)

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

        for terminal in self.terminals:
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

    def first_rhs(self, y: list[str]) -> set[str]:
        if len(y) == 0:
            return set()
        if y[0] in self.nullables:
            return self.first[y[0]].union(self.first_rhs(y[1:]))
        return self.first[y[0]]

    def nullable_rhs(self, y: list[str]) -> bool:
        return (not len(y)) or all(map(lambda x: x in self.nullables, y))

    @cached_property
    def parsing_table(self):
        self.compute_first_follow_nullable()

        table = defaultdict(lambda: defaultdict(set))

        for x, y in self.rules:
            for t in self.first_rhs(y):
                table[x][t].add((x, y))
            if not self.nullable_rhs(y):
                continue
            for t in self.follow[x]:
                table[x][t].add((x, y))
        return table

    def _rhs2str(self, rules: list[str]) -> str:
        return " ".join(rules) if len(rules) else self.styling.epsilon

    def _table_cell2str(self, x: str, t: str) -> str:
        res = ""
        if t not in self.parsing_table[x]:
            return res
        for el in self.parsing_table[x][t]:
            _, y = el
            res += f"{x} -> {self._rhs2str(y)}\n"
        return res

    def get_tabulate(self, fmt: str = "github") -> str:
        rows = sorted(self.non_terminals)
        cols = sorted(list(self.terminals))

        list_table = []
        for row in rows:
            list_table.append([row] + [self._table_cell2str(row, col) for col in cols])

        return tabulate(list_table, headers=[""] + cols, tablefmt=fmt)

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
                res += f"{prefix}{offset_sym * 2} {self._rhs2str(v[0])}\n"
                continue

            first, *rest, last = v
            res += (
                f"{prefix}{self.styling.pipe_wne}{offset_sym} {self._rhs2str(first)}\n"
            )

            for rule in rest:
                res += f"{offset}{self.styling.pipe_nes}{offset_sym} {self._rhs2str(rule)}\n"

            res += f"{offset}{self.styling.pipe_ne}{offset_sym} {self._rhs2str(last)}\n"

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
    non_terminals = p.non_terminals
    print(f"{non_terminals=}")
    print(f"{p.nullables=}")
    interesting_first = {k: v for k, v in p.first.items() if k in non_terminals}
    print(f"first = {interesting_first}")
    interesting_follows = {k: v for k, v in p.follow.items() if k in non_terminals}
    print(f"{interesting_follows=}")
    p.parsing_table
    print(f"{p.get_tabulate(fmt='simple_grid')}")
