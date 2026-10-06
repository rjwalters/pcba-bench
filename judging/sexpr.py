"""Minimal KiCad S-expression reader (stdlib only).

The grader deliberately does not depend on any agent-side toolkit, so it
carries its own parser. Lists become Python lists; atoms and strings become
str. Only reading is supported.
"""

from __future__ import annotations

from collections.abc import Iterator

Node = list  # recursive: list[str | Node]


def parse(text: str) -> Node:
    stack: list[list] = [[]]
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == "(":
            stack.append([])
            i += 1
        elif c == ")":
            done = stack.pop()
            stack[-1].append(done)
            i += 1
        elif c.isspace():
            i += 1
        elif c == '"':
            j = i + 1
            buf = []
            while j < n and text[j] != '"':
                if text[j] == "\\" and j + 1 < n:
                    buf.append(text[j + 1])
                    j += 2
                else:
                    buf.append(text[j])
                    j += 1
            stack[-1].append("".join(buf))
            i = j + 1
        else:
            j = i
            while j < n and not text[j].isspace() and text[j] not in '()"':
                j += 1
            stack[-1].append(text[i:j])
            i = j
    if len(stack) != 1 or len(stack[0]) != 1:
        raise ValueError("unbalanced S-expression")
    return stack[0][0]


def head(node) -> str | None:
    return node[0] if isinstance(node, list) and node and isinstance(node[0], str) else None


def children(node: Node, name: str) -> Iterator[Node]:
    for item in node:
        if head(item) == name:
            yield item


def child(node: Node, name: str) -> Node | None:
    return next(children(node, name), None)


def walk(node: Node) -> Iterator[Node]:
    yield node
    for item in node:
        if isinstance(item, list):
            yield from walk(item)


def floats(node: Node | None, count: int) -> tuple[float, ...] | None:
    if node is None or len(node) < count + 1:
        return None
    try:
        return tuple(float(v) for v in node[1 : count + 1])
    except (TypeError, ValueError):
        return None
