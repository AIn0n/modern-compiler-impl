from enum import StrEnum
from dataclasses import dataclass
from typing import Mapping, Optional

from parsers.base_parser import RuleType
from parsers.commons import swap_with_next


class LRActionEnum(StrEnum):
    REDUCE = "r"
    GOTO = "g"
    SHIFT = "s"
    ACCEPT = "a"


@dataclass(slots=True, frozen=True)
class LRAction:
    type_: LRActionEnum
    to: int

    def __str__(self) -> str:
        if self.type_ == LRActionEnum.ACCEPT:
            return "a"
        return f"{self.type_.value}{self.to}"

    @staticmethod
    def reduce(n: int) -> LRAction:
        return LRAction(LRActionEnum.REDUCE, n)

    @staticmethod
    def shift(n: int) -> LRAction:
        return LRAction(LRActionEnum.SHIFT, n)

    @staticmethod
    def accept() -> LRAction:
        return LRAction(LRActionEnum.ACCEPT, -1)

    @staticmethod
    def goto(n: int) -> LRAction:
        return LRAction(LRActionEnum.GOTO, n)


@dataclass(slots=True, frozen=True)
class LRItem:
    rule: RuleType
    dot_idx: int

    def peek_after_dot(self) -> Optional[str]:
        """
        Get the first symbol (next to) after the dot. This method is beneficial
        for closure in LR parser. Return None if there's no symbol after the dot.
        """
        next_idx = self.dot_idx + 1
        return None if next_idx >= len(self.rule.rhs) else self.rule.rhs[next_idx]

    def advance_dot(self) -> LRItem:
        """
        Return the copy of the class, with dot moved one position to the right.
        """
        # swap dot with next element after it
        new_rhs = swap_with_next(self.rule.rhs, self.dot_idx)

        return LRItem(
            rule=RuleType(lhs=self.rule.lhs, rhs=new_rhs), dot_idx=self.dot_idx + 1
        )

    def is_dot_at_end(self) -> bool:
        return self.dot_idx == len(self.rule.rhs) - 1

    def to_rule(self) -> RuleType:
        """
        Get simple rule from given item - just by removing the dot.
        """
        return RuleType(
            lhs=self.rule.lhs, rhs=tuple(el for el in self.rule.rhs if el != ".")
        )

    @staticmethod
    def from_rule(rule: RuleType) -> LRItem:
        """
        Turn rule into LR item, by default setting the dot at the first position
        on left-hand side.
        """
        return LRItem(rule=RuleType(rule.lhs, tuple([".", *rule.rhs])), dot_idx=0)

    def __str__(self) -> str:
        return str(self.rule)


LRState = frozenset[LRItem]
LRParsingTable = dict[int, dict[str, set[LRAction]]]


@dataclass(slots=True, frozen=True)
class IndexedLREdge:
    """
    Stores connections between states: from and to states, in form of indexes, and
    symbol on connection.
    """

    from_: int
    to: int
    symbol: str


@dataclass(slots=True, frozen=True)
class LREdge:
    """
    Stores states from and to indexes and symbol on the given edge. Also can store
    whole LRState inside, but it seems to be bad idea during parsing table building.
    """

    from_: LRState
    to: LRState
    symbol: str

    def convert_to_indexed(self, lookup: Mapping[LRState, int]) -> IndexedLREdge:
        """
        Convert states in edge from whole objects to indexes.
        """
        return IndexedLREdge(
            from_=lookup[self.from_], to=lookup[self.to], symbol=self.symbol
        )
