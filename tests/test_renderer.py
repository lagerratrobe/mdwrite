import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import mistune
from mistune.plugins.formatting import strikethrough
from mistune.plugins.table import table

from plugins import plugin_underline
from renderer import StyledRenderer
from style_engine import StyleEngine

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")


def make_md(spacing_mode="compact"):
    engine = StyleEngine(CONFIG_PATH)
    engine.set_spacing_mode(spacing_mode)
    renderer = StyledRenderer(engine)
    return mistune.create_markdown(
        renderer=renderer,
        plugins=[strikethrough, table, plugin_underline],
    )


def test_paragraph_has_inline_style():
    md = make_md()
    result = md("Hello world")
    assert '<p style="' in result
    assert "Helvetica" in result
    assert "Hello world" in result


def test_heading_has_inline_style():
    md = make_md()
    result = md("# Title")
    assert '<h1 style="' in result
    assert "Helvetica" in result
    assert "26px" in result


def test_heading_levels():
    md = make_md()
    for level in range(1, 7):
        result = md(f"{'#' * level} Heading {level}")
        assert f"<h{level} style=" in result


def test_bold():
    md = make_md()
    result = md("**bold**")
    assert "<strong>" in result


def test_italic():
    md = make_md()
    result = md("*italic*")
    assert "<em>" in result


def test_inline_code():
    md = make_md()
    result = md("`code`")
    assert '<code style="' in result
    assert "Fira Code" in result or "Consolas" in result


def test_code_block():
    md = make_md()
    result = md("```\nprint('hi')\n```")
    assert '<div style="' in result
    assert "<pre" in result
    assert "<code>" in result


def test_link_has_style():
    md = make_md()
    result = md("[click](https://example.com)")
    assert '<a href="https://example.com" style="' in result
    assert "#2980b9" in result


def test_image():
    md = make_md()
    result = md("![alt](https://example.com/img.png)")
    assert '<img src="' in result
    assert 'alt="alt"' in result


def test_blockquote():
    md = make_md()
    result = md("> quoted text")
    assert '<blockquote style="' in result
    assert "border-left" in result


def test_hr():
    md = make_md()
    result = md("---")
    assert '<hr style="' in result


def test_unordered_list_has_bullets():
    md = make_md()
    result = md("- Item one\n- Item two")
    assert '<ul style="' in result
    assert '<li style="' in result
    assert "&#8226;" in result


def test_ordered_list_has_outline_markers():
    md = make_md()
    result = md("1. First\n1. Second\n1. Third")
    assert '<ol style="' in result
    assert "I." in result
    assert "II." in result
    assert "III." in result


def test_nested_ordered_list_depth():
    md = make_md()
    result = md("1. Top\n   1. Nested")
    assert "I." in result
    assert "A." in result


def test_deeply_nested_outline():
    md = make_md()
    text = (
        "1. Level 0\n"
        "   1. Level 1\n"
        "      1. Level 2\n"
        "         1. Level 3\n"
        "            1. Level 4\n"
    )
    result = md(text)
    assert "I." in result   # upper-roman
    assert "A." in result   # upper-alpha
    assert "1." in result   # decimal
    assert "a." in result   # lower-alpha
    assert "i." in result   # lower-roman


def test_strikethrough_has_style():
    md = make_md()
    result = md("~~deleted~~")
    assert '<del style="' in result
    assert "line-through" in result


def test_underline_has_style():
    md = make_md()
    result = md("++underlined++")
    assert '<u style="' in result
    assert "underline" in result


def test_table_has_styles():
    md = make_md()
    text = "| A | B |\n|---|---|\n| 1 | 2 |"
    result = md(text)
    assert '<table style="' in result
    assert '<th style="' in result
    assert '<td style="' in result


def test_table_alignment():
    md = make_md()
    text = "| Left | Center | Right |\n|:-----|:------:|------:|\n| a | b | c |"
    result = md(text)
    assert "text-align: left" in result
    assert "text-align: center" in result
    assert "text-align: right" in result


def test_no_css_classes():
    md = make_md()
    result = md("# Hello\n\nParagraph\n\n- List\n\n```\ncode\n```")
    assert 'class="' not in result


def test_no_style_block():
    md = make_md()
    result = md("# Hello\n\nWorld")
    assert "<style>" not in result


def test_spacing_toggle_compact():
    md = make_md("normal")
    result = md("<!-- compact -->\n\nCompact text")
    assert "1px 0" in result


def test_spacing_toggle_normal():
    md = make_md("compact")
    result = md("<!-- normal -->\n\nNormal text")
    assert "4px 0" in result


def test_spacing_toggle_no_visible_output():
    md = make_md()
    result = md("<!-- compact -->")
    assert "<!--" not in result


def test_ordered_list_start_attribute():
    md = make_md()
    result = md("3. Third\n4. Fourth")
    # With start=3, first marker at depth 0 should be III.
    assert "III." in result
    assert "IV." in result
