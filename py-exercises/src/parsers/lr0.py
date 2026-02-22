from .baseParser import ParserPrintStyler, BaseParser


class LR0Parser(BaseParser):
    def __init__(self, styling: ParserPrintStyler | None = None):
        super().__init__(styling=styling)
