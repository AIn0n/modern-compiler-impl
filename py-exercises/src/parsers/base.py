from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from typing import MutableMapping


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
        self.rules = defaultdict(list)
        self.styling = styling
        self.nullables = set()
        self.first: MutableMapping[str, set[str]] = defaultdict(set)
        self.follow: MutableMapping[str, set[str]] = defaultdict(set)

    def add_rule(self, rule: str) -> None:
        lhs, rhs = rule.split("->")
        rhs_list = rhs.strip().split()
        self.rules[lhs.strip()].append(rhs_list)

    def _rule_to_str(self, rules: list[str]) -> str:
        return " ".join(rules) if len(rules) else self.styling.epsilon

    def get_all_nonterminals(self) -> set[str]:
        # just get all right hand side symbols
        return set(self.rules.keys())

    def get_all_terminals(self) -> set[str]:
        all_rhs_symbols = set(
            chain.from_iterable([el for rule in self.rules.values() for el in rule])
        )
        # everything from the rules, except right hands side
        return all_rhs_symbols - self.get_all_nonterminals()

    def _is_sequence_nullable(self, seq: list[str]) -> bool:
        if len(seq) == 0:
            return True
        return all(map(lambda x: x in self.nullables, seq))

    def compute_first_follow_nullable(self) -> None:
        self.nullables = set()
        self.first = {z: set([z]) for z in self.get_all_terminals()}
        self.follow = defaultdict(set)
        changed = True
        while changed:
            changed = False
            # TODO: change the structure of the rules in memory - rather than map do just flat list
            for x, y in self.rules.items():
                k = len(y)
                if self._is_sequence_nullable(y):
                    self.nullables.add(x)
                    changed = True
                for i in range(k):
                    for j in range(i + 1, k):
                        if self._is_sequence_nullable(y[0:i]):
                            self.first[x] = self.first[x].union(self.follow[y[i]])
                            changed = True
                        if self._is_sequence_nullable(y[i + 1 :]):
                            self.follow[y[i]] = self.follow[y[i]].union(self.follow[x])
                            changed = True
                        if self._is_sequence_nullable(y[i + 1 : j]):
                            self.follow[y[i]] = self.follow[y[i]].union(
                                self.first(y[j])
                            )
                            changed = True

    def __str__(self) -> str:
        left_pad = max(map(len, self.rules.keys())) + 1
        offset_sym = self.styling.hor_line
        res = ""
        offset = left_pad * " "
        for k, v in self.rules.items():
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
    p = BaseParser()
    p.add_rule("S` -> S &")
    p.add_rule("S -> ")
    p.add_rule("S -> X S")
    p.add_rule(r"B -> \ begin { WORD }")
    p.add_rule(r"E -> \ end { WORD }")
    p.add_rule("X -> B S E")
    p.add_rule("X -> { S }")
    p.add_rule("X -> WORD")
    p.add_rule("X -> begin")
    p.add_rule("X -> end")
    p.add_rule(r"X -> \ WORD")

    print(p)
    print(f"All nonterminals: {p.get_all_nonterminals()}")
    print(f"All terminals: {p.get_all_terminals()}")
    p.compute_first_follow_nullable()
