import re
from typing import Any, Dict, Optional

import mistune
from mistune.core import BlockState
from mistune.util import escape as escape_text
from mistune.util import safe_entity, striptags

from outline import OutlineFormatter
from style_engine import StyleEngine


class StyledRenderer(mistune.HTMLRenderer):
    def __init__(self, style_engine: StyleEngine) -> None:
        super().__init__(escape=False)
        self.style_engine = style_engine
        self.outline = OutlineFormatter(style_engine.outline_styles)
        self._list_stack: list[dict] = []
        self._list_mode: str = "numbered"  # "numbered" or "outline"

    def render_token(self, token: Dict[str, Any], state: BlockState) -> str:
        if token["type"] == "list":
            ordered = token.get("attrs", {}).get("ordered", False)
            start = token.get("attrs", {}).get("start", 1)
            self._list_stack.append({"ordered": ordered, "counter": start - 1})
            result = super().render_token(token, state)
            self._list_stack.pop()
            return result
        elif token["type"] == "list_item":
            if self._list_stack:
                self._list_stack[-1]["counter"] += 1
            return super().render_token(token, state)
        return super().render_token(token, state)

    def text(self, text: str) -> str:
        return safe_entity(text)

    def emphasis(self, text: str) -> str:
        return "<em>" + text + "</em>"

    def strong(self, text: str) -> str:
        return "<strong>" + text + "</strong>"

    def paragraph(self, text: str) -> str:
        style = self.style_engine.style_for_paragraph()
        return f'<p style="{style}">{text}</p>\n'

    def heading(self, text: str, level: int, **attrs: Any) -> str:
        style = self.style_engine.style_for_heading(level)
        tag = f"h{level}"
        return f'<{tag} style="{style}">{text}</{tag}>\n'

    def codespan(self, text: str) -> str:
        style = self.style_engine.style_for_code_inline()
        return f'<code style="{style}">{escape_text(text)}</code>'

    def block_code(self, code: str, info: Optional[str] = None) -> str:
        style = self.style_engine.style_for_code_block()
        return (
            f'<div style="{style}">'
            f"<pre style=\"margin: 0; font-family: inherit; font-size: inherit; white-space: pre;\">"
            f"<code>{escape_text(code)}</code>"
            f"</pre></div>\n"
        )

    def link(self, text: str, url: str, title: Optional[str] = None) -> str:
        style = self.style_engine.style_for_link()
        s = f'<a href="{self.safe_url(url)}" style="{style}"'
        if title:
            s += f' title="{safe_entity(title)}"'
        return s + ">" + text + "</a>"

    def image(self, text: str, url: str, title: Optional[str] = None) -> str:
        src = self.safe_url(url)
        alt = escape_text(striptags(text))
        s = f'<img src="{src}" alt="{alt}" style="max-width: 100%;"'
        if title:
            s += f' title="{safe_entity(title)}"'
        return s + " />"

    def list(self, text: str, ordered: bool, **attrs: Any) -> str:
        style = self.style_engine.style_for_list()
        tag = "ol" if ordered else "ul"
        return f'<{tag} style="{style}">\n{text}</{tag}>\n'

    def list_item(self, text: str) -> str:
        style = self.style_engine.style_for_list_item()
        marker_html = ""

        if self._list_stack:
            ctx = self._list_stack[-1]
            if ctx["ordered"]:
                counter = ctx["counter"]
                if self._list_mode == "outline":
                    depth = len(self._list_stack) - 1
                    marker = self.outline.format_marker(depth, counter)
                else:
                    marker = f"{counter}."
                marker_style = self.style_engine.style_for_outline_marker()
                marker_html = f'<span style="{marker_style}">{marker}</span> '
            else:
                marker_html = "&#8226; "

        if marker_html:
            p_match = re.match(r"(<p[^>]*>)", text)
            if p_match:
                text = p_match.group(1) + marker_html + text[p_match.end() :]
            else:
                text = marker_html + text

        return f'<li style="{style}">{text}</li>\n'

    def block_quote(self, text: str) -> str:
        style = self.style_engine.style_for_blockquote()
        return f'<blockquote style="{style}">\n{text}</blockquote>\n'

    def thematic_break(self) -> str:
        style = self.style_engine.style_for_hr()
        return f'<hr style="{style}" />\n'

    def block_html(self, html: str) -> str:
        stripped = html.strip()
        if stripped == "<!-- compact -->":
            self.style_engine.set_spacing_mode("compact")
            return ""
        elif stripped == "<!-- normal -->":
            self.style_engine.set_spacing_mode("normal")
            return ""
        elif stripped == "<!-- outline -->":
            self._list_mode = "outline"
            return ""
        elif stripped == "<!-- numbered -->":
            self._list_mode = "numbered"
            return ""
        return html + "\n"

    def inline_html(self, html: str) -> str:
        return html

    def linebreak(self) -> str:
        return "<br />\n"

    def softbreak(self) -> str:
        return "\n"

    def blank_line(self) -> str:
        return ""

    def block_text(self, text: str) -> str:
        return text

    def table(self, text: str) -> str:
        style = self.style_engine.style_for_table()
        return f'<table style="{style}">\n{text}</table>\n'

    def table_head(self, text: str) -> str:
        return "<thead>\n<tr>\n" + text + "</tr>\n</thead>\n"

    def table_body(self, text: str) -> str:
        return "<tbody>\n" + text + "</tbody>\n"

    def table_row(self, text: str) -> str:
        return "<tr>\n" + text + "</tr>\n"

    def table_cell(self, text: str, align: Optional[str] = None, head: bool = False) -> str:
        tag = "th" if head else "td"
        style = self.style_engine.style_for_table_cell(head=head, align=align)
        return f'<{tag} style="{style}">{text}</{tag}>\n'

    def strikethrough(self, text: str) -> str:
        style = self.style_engine.style_for_strikethrough()
        return f'<del style="{style}">{text}</del>'

    def underline(self, text: str) -> str:
        style = self.style_engine.style_for_underline()
        return f'<u style="{style}">{text}</u>'
