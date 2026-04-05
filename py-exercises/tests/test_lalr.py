from parsers.lr.lr_types import are_states_equal_wo_lookahead, LRItem


def test_function_to_compare_states_given_two_equal_states_return_true():
    first = frozenset(
        [
            LRItem.from_rule_str("S' -> S $", dot_pos=0),
            LRItem.from_rule_str("S -> P G", dot_pos=1),
        ]
    )
    second = frozenset(
        [
            LRItem.from_rule_str("S -> P G", dot_pos=1),
            LRItem.from_rule_str("S' -> S $", dot_pos=0),
        ]
    )
    assert are_states_equal_wo_lookahead(first, second) == True


def test_function_to_compare_states_given_two_same_states_with_different_dot_return_false():
    first = frozenset(
        [
            LRItem.from_rule_str("S' -> S $", dot_pos=0),
            LRItem.from_rule_str("S -> P G", dot_pos=1),
        ]
    )
    second = frozenset(
        [
            LRItem.from_rule_str("S -> P G", dot_pos=1),
            LRItem.from_rule_str("S' -> S $", dot_pos=1),
        ]
    )
    assert are_states_equal_wo_lookahead(first, second) == False


def test_given_two_same_states_with_other_lookahead_compare_return_true():
    first = frozenset(
        [
            LRItem.from_rule_str("S' -> S $", dot_pos=0, lookahead="?"),
            LRItem.from_rule_str("S -> P G", dot_pos=1),
        ]
    )
    second = frozenset(
        [
            LRItem.from_rule_str("S' -> S $", dot_pos=0, lookahead="#"),
            LRItem.from_rule_str("S -> P G", dot_pos=1),
        ]
    )
    assert are_states_equal_wo_lookahead(first, second) == True
