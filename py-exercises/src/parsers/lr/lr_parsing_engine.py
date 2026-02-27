from .lr0 import LR0Parser


class LREngine:
    def __init__(self, p: LR0Parser) -> None:
        self.indexed_rules = p.indexed_rules
        self.table = p.parsing_table

    def parse(self, tokens: list[str]):
        # stack = []
        # TODO:
        # * learn which state is the first one
        # * finish this
        ...
