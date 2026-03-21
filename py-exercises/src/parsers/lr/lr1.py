from dataclasses import dataclass

from parsers.base_parser import BaseParser, ParserPrintStyler, RuleType

@dataclass(slots=True, frozen=True)
class LR1Item:
    """
    A bit different than item from LR0 - it have additional info about lookahead.
    Also here, I will probably manage to solve better the dot - rather than using
    real symbol inside the rule, I will store it only as a index, indicating
    position inside the right-hand side of the rule. I can always add it
    during the printing.
    """
    rule: RuleType
    dot_pos: int
    lookahead: str


class LR1Parser(BaseParser):
    def __init__(self, styling: ParserPrintStyler):
        super().__init__(styling=styling)
