import re
from typing import TYPE_CHECKING, Match, Optional

from mistune.helpers import PREVENT_BACKSLASH

if TYPE_CHECKING:
    from mistune.core import BaseRenderer, InlineState
    from mistune.inline_parser import InlineParser
    from mistune.markdown import Markdown

_UNDERLINE_END = re.compile(
    r"(?:" + PREVENT_BACKSLASH + r"\\\+|[^\s+])\+\+(?!\+)"
)


def parse_underline(
    inline: "InlineParser", m: Match[str], state: "InlineState"
) -> Optional[int]:
    pos = m.end()
    m1 = _UNDERLINE_END.search(state.src, pos)
    if not m1:
        return None
    end_pos = m1.end()
    text = state.src[pos : end_pos - 2]
    new_state = state.copy()
    new_state.src = text
    children = inline.render(new_state)
    state.append_token({"type": "underline", "children": children})
    return end_pos


def render_underline(renderer: "BaseRenderer", text: str) -> str:
    return "<u>" + text + "</u>"


def plugin_underline(md: "Markdown") -> None:
    md.inline.register(
        "underline",
        r"\+\+(?=[^\s+])",
        parse_underline,
        before="link",
    )
    if md.renderer and md.renderer.NAME == "html":
        md.renderer.register("underline", render_underline)
