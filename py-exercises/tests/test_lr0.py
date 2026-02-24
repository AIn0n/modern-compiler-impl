from parsers.lr0 import LR0Parser, LRItem
from parsers.example_grammars import GRAMMAR_3_20


def test_closure_given_grammar_3_20_should_return_valid_set_for_first_rule():
    # figure 3.21, page 62
    expected_items = [
        LRItem(rule=("S'", (".", "S", "$")), dot_idx=0),
        LRItem(rule=("S", (".", "(", "L", ")")), dot_idx=0),
        LRItem(rule=("S", (".", "x")), dot_idx=0),
    ]

    p = LR0Parser()
    p.add_rules(*GRAMMAR_3_20)

    given_items = p.closure(set([LRItem.from_rule(p.get_start_rule())]))

    assert len(expected_items) == len(given_items)

    for item in expected_items:
        assert item in given_items


def test_goto_given_grammar_3_20_returns_valid_set():
    # same as above, figure 3.21, page 62
    # fmt: off
    expected_items = [
        LRItem(
            rule=("S", ("(", ".", "L", ")")),
            dot_idx=1
        ),
        LRItem(
            rule=("L", (".", "S")),
            dot_idx=0
        ),
        LRItem(
            rule=("L", (".", "L", ",", "S")),
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
    # fmt: on

    p = LR0Parser()
    p.add_rules(*GRAMMAR_3_20)

    first_closure = p.closure(set([LRItem.from_rule(p.get_start_rule())]))
    given_items = p.goto(first_closure, "(")

    for item in expected_items:
        assert item in given_items

    assert len(expected_items) == len(given_items)


def test_lr0_for_grammar_3_20_returns_9_unique_states():
    p = LR0Parser()
    p.add_rules(*GRAMMAR_3_20)

    p.compute_states_and_edges()

    assert len(p.states) == 9


def test_lr0_for_grammar_3_20_returns_12_state_edges():
    p = LR0Parser()
    p.add_rules(*GRAMMAR_3_20)

    p.compute_states_and_edges()

    assert len(p.edges) == 12
