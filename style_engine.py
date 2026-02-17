import os
from typing import Optional

import yaml


class StyleEngine:
    def __init__(self, config_path: Optional[str] = None) -> None:
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.spacing_mode = "compact"

    def set_spacing_mode(self, mode: str) -> None:
        self.spacing_mode = mode

    def _spacing(self, key: str) -> str:
        return self.config["spacing"][self.spacing_mode][key]

    def _font(self, key: str) -> str:
        return self.config["fonts"][key]

    def _font_size(self, key: str) -> str:
        return self.config["font_sizes"][key]

    def _color(self, key: str) -> str:
        return self.config["colors"][key]

    def style_for_paragraph(self) -> str:
        return (
            f"margin: {self._spacing('paragraph_margin')}; "
            f"font-family: {self._font('body')}; "
            f"font-size: {self._font_size('body')}; "
            f"color: {self._color('body')}; "
            f"line-height: 1.4;"
        )

    def style_for_heading(self, level: int) -> str:
        style = (
            f"margin: {self._spacing('heading_margin')}; "
            f"font-family: {self._font('heading')}; "
            f"font-size: {self._font_size(f'h{level}')}; "
            f"color: {self._color('heading')}; "
            f"font-weight: bold; "
            f"line-height: 1.3;"
        )
        align = self.config.get("heading_align", {}).get(f"h{level}")
        if align:
            style += f" text-align: {align};"
        return style

    def style_for_list(self) -> str:
        return (
            f"margin: {self._spacing('list_margin')}; "
            f"padding: 0; "
            f"list-style-type: none;"
        )

    def style_for_list_item(self) -> str:
        return (
            f"margin: {self._spacing('list_item_margin')}; "
            f"font-family: {self._font('body')}; "
            f"font-size: {self._font_size('body')}; "
            f"color: {self._color('body')}; "
            f"line-height: 1.4;"
        )

    def style_for_code_inline(self) -> str:
        return (
            f"font-family: {self._font('code')}; "
            f"font-size: {self._font_size('code')}; "
            f"background-color: {self._color('code_bg')}; "
            f"padding: 1px 4px; "
            f"border-radius: 3px;"
        )

    def style_for_code_block(self) -> str:
        return (
            f"margin: {self._spacing('code_block_margin')}; "
            f"padding: {self._spacing('code_block_padding')}; "
            f"font-family: {self._font('code')}; "
            f"font-size: {self._font_size('code')}; "
            f"background-color: {self._color('code_bg')}; "
            f"border: 1px solid {self._color('code_border')}; "
            f"border-radius: 4px; "
            f"white-space: pre; "
            f"overflow-x: auto;"
        )

    def style_for_link(self) -> str:
        return f"color: {self._color('link')}; text-decoration: underline;"

    def style_for_blockquote(self) -> str:
        return (
            f"margin: {self._spacing('blockquote_margin')}; "
            f"padding: 4px 12px; "
            f"border-left: 3px solid {self._color('blockquote_border')}; "
            f"color: {self._color('blockquote_text')};"
        )

    def style_for_hr(self) -> str:
        return (
            f"border: none; "
            f"border-top: 1px solid {self._color('hr')}; "
            f"margin: 8px 0;"
        )

    def style_for_table(self) -> str:
        return (
            f"border-collapse: collapse; "
            f"margin: {self._spacing('paragraph_margin')}; "
            f"font-family: {self._font('body')}; "
            f"font-size: {self._font_size('body')};"
        )

    def style_for_table_cell(self, head: bool = False, align: Optional[str] = None) -> str:
        style = (
            f"border: 1px solid {self._color('table_border')}; "
            f"padding: 4px 8px; "
            f"font-family: {self._font('body')}; "
            f"font-size: {self._font_size('body')}; "
            f"color: {self._color('body')};"
        )
        if head:
            style += (
                f" background-color: {self._color('table_header_bg')};"
                f" font-weight: bold;"
            )
        if align:
            style += f" text-align: {align};"
        return style

    def style_for_strikethrough(self) -> str:
        return f"text-decoration: line-through; color: {self._color('strikethrough')};"

    def style_for_underline(self) -> str:
        return "text-decoration: underline;"

    def style_for_outline_marker(self) -> str:
        return "font-weight: bold; margin-right: 4px;"

    @property
    def outline_styles(self) -> list:
        return self.config["outline_styles"]
