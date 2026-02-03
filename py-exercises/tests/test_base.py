import pytest
from parsers.base import BaseParser

# Example test for BaseParser

def test_base_parser_initialization():
    parser = BaseParser()
    assert parser is not None


def test_example_grammar_3_12():
    # Example from grammar 3.12
    p = BaseParser()
    p.add_rules(
        "Z -> d",
        "Z -> X Y Z",
        "Y -> ",
        "Y -> c",
        "X -> Y",
        "X -> a",
    )
    p.compute_first_follow_nullable()
    non_terminals = p.get_all_nonterminals()
    assert non_terminals == set(["X", "Y", "Z"])
    assert p.nullables == set(["X", "Y"])
    interesting_first = {k: v for k, v in p.first.items() if k in non_terminals}

    # Literally table from page n 50
    assert p.first["X"] == set(["a", "c"])
    assert p.first["Y"] == set(["c"])
    assert p.first["Z"] == set(["a", "c", "d"])

    assert p.follow["X"] == set(["a", "c", "d"])
    assert p.follow["Y"] == set(["a", "c", "d"])
    assert len(p.follow["Z"]) == 0

