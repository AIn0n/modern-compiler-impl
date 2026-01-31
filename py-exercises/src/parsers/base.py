from collections import defaultdict
from dataclasses import dataclass
from itertools import chain

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

    def add_rule(self, rule: str) -> None:
        lhs, rhs = rule.split("->")
        rhs_list = rhs.strip().split()
        self.rules[lhs.strip()].append(rhs_list)

    def _rule_to_str(self, rules: list[str]) -> str:
        return " ".join(rules) if len(rules) else self.styling.epsilon

    def get_nullables(self) -> list[str]:
        return [k for k, v in self.rules.items() if not all(map(len, v))]

    def get_all_nonterminals(self) -> set[str]:
        return set(self.rules.keys())

    def get_all_terminals(self) -> set[str]:
        all_rhs_symbols = set(chain.from_iterable([el for rule in self.rules.values() for el in rule]))
        return all_rhs_symbols - self.get_all_nonterminals()
        

    def __str__(self) -> str:
        left_pad = max(map(len, self.rules.keys())) + 1
        offset_sym = self.styling.hor_line
        res = ""
        for k, v in self.rules.items():
            prefix = f"{k:{offset_sym}<{left_pad}}"
            if len(v) == 1:
                res += f"{prefix}{offset_sym * 2} {self._rule_to_str(v[0])}\n"
                continue

            first, *rest, last = v
            res += f"{prefix}{self.styling.pipe_wne}{offset_sym} {self._rule_to_str(first)}\n"

            offset = left_pad * " "
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
    p.add_rule("X -> \ WORD")
    
    print(p)
    print(f"All nullables symbols: {p.get_nullables()}")
    print(f"All nonterminals: {p.get_all_nonterminals()}")
    print(f"All terminals: {p.get_all_terminals()}")