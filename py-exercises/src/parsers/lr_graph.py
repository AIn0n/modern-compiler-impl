from typing import Optional

from mermaid.flowchart import Node, Link, FlowChart  # type: ignore[import-untyped]

from .lr0 import LR0Parser, LRState


def state_to_str(state: LRState) -> str:
    res = ""
    for el in state:
        rule = el.rule
        res += f"{rule.lhs} -> " + " ".join(rule.rhs) + "<br>"
    return res


def lr_parser_to_mermaid(p: LR0Parser, title: Optional[str] = None) -> FlowChart:
    if title is None:
        title = ""
    assert isinstance(p.states, dict)
    nodes = {i: Node(str(i), state_to_str(state)) for i, state in p.states.items()}
    links = []
    for edge in p.edges:
        assert isinstance(edge.from_, int) and isinstance(edge.to, int)
        links.append(
            Link(
                origin=nodes[edge.from_], end=nodes[edge.to], message=f'"{edge.symbol}"'
            )
        )
    return FlowChart(title=title, nodes=list(nodes.values()), links=links)
