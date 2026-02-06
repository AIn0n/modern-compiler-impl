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
    non_terminals = p.non_terminals
    assert non_terminals == set(["X", "Y", "Z"])
    assert p.nullables == set(["X", "Y"])

    # Literally table from page n 50
    assert p.first["X"] == set(["a", "c"])
    assert p.first["Y"] == set(["c"])
    assert p.first["Z"] == set(["a", "c", "d"])

    assert p.follow["X"] == set(["a", "c", "d"])
    assert p.follow["Y"] == set(["a", "c", "d"])
    assert len(p.follow["Z"]) == 0

def test_ll_parser_on_grammar_3_15():
    p = BaseParser()
    p.add_rules(
        "S -> E $",
        "T -> F T'",
        "E -> T E'",
        "E' -> + T E'",
        "E' -> - T E'",
        "E' ->",
        "T' -> * F T'",
        "T' -> / F T'",
        "T' ->",
        "F -> id",
        "F -> num",
        "F -> ( E )",
    )
    p.compute_first_follow_nullable()

    # Table 3.16

    ## nullables
    assert {"E'", "T'"} == p.nullables

    ## first
    assert {"(", "id", "num"} == p.first["S"]
    assert {"(", "id", "num"} == p.first["E"]
    assert {"(", "id", "num"} == p.first["T"]
    assert {"(", "id", "num"} == p.first["F"]

    assert {"/", "*"} == p.first["T'"]
    assert {"-", "+"} == p.first["E'"]

    ## follows
    assert len(p.follow["S"]) == 0

    assert {")", "$"} == p.follow["E"]
    assert {")", "$"} == p.follow["E'"]

    assert {")", "+", "-", "$"} == p.follow["T"]
    assert {")", "+", "-", "$"} == p.follow["T'"]

    assert {")", "+", "-", "*", "/", "$"} == p.follow["F"]
