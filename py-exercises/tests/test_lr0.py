from parsers.lr0 import LR0Parser, LRItem
from parsers.example_grammars import GRAMMAR_3_20

def test_closure_given_grammar_3_20_should_return_valid_set_for_first_rule():
    # figure 3.21, page 62
    expected_items = [
        LRItem(
            rule=("S'", (".", "S", "$")),
            dot_idx=0
        ),
        LRItem(
            rule=("S", (".", "(", "L", ")")),
            dot_idx=0
        ),
        LRItem(
            rule=("S", (".", "x")),
            dot_idx=0
        ),
    ]

    p = LR0Parser()
    p.add_rules(*GRAMMAR_3_20)

    given_items = p.closure(set([LRItem.from_rule(p.get_start_rule())]))

    for item in expected_items:
        assert item in given_items