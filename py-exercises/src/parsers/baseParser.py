from dataclasses import dataclass
from functools import cached_property
from itertools import chain
from collections import defaultdict


@dataclass(frozen=True, slots=True)
class ParserPrintStyler:
    epsilon: str = "ε"
    hor_line: str = "─"
    pipe_wne: str = "┬"
    pipe_nes: str = "├"
    pipe_ne: str = "└"


RuleType = tuple[str, tuple[str, ...]]


class BaseParser:
    """
    Class with the logic for adding new rules, printing the rules, handling the
    printing styling, etc.
    """

    def __init__(self, styling: ParserPrintStyler | None = None) -> None:
        if styling is None:
            styling = ParserPrintStyler()
        self.rules: list[RuleType] = []
        self.styling = styling

    @cached_property
    def non_terminals(self) -> set[str]:
        return set([lhs for lhs, _ in self.rules])

    @cached_property
    def terminals(self) -> set[str]:
        all_rhs_symbols = set(chain.from_iterable([rhs for _, rhs in self.rules]))
        # everything from the rules, except right hands side
        return all_rhs_symbols - self.non_terminals

    def add_rule(self, rule: str) -> None:
        """
        Parse rule from simple string, to tuple, with first element
        non-terminal, and second tuple of strings.
        """
        lhs, rhs = rule.split("->")
        rhs_list = tuple(rhs.strip().split())
        r = (lhs.strip(), rhs_list)
        self.rules.append(r)

    def add_rules(self, *rules) -> None:
        for rule in rules:
            self.add_rule(rule)

    def _rhs2str(self, rules: tuple[str, ...]) -> str:
        return " ".join(rules) if len(rules) else self.styling.epsilon

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
