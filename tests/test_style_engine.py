import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from style_engine import StyleEngine

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")


def make_engine():
    return StyleEngine(CONFIG_PATH)


def test_loads_config():
    engine = make_engine()
    assert "spacing" in engine.config
    assert "fonts" in engine.config
    assert "font_sizes" in engine.config
    assert "colors" in engine.config
    assert "outline_styles" in engine.config


def test_default_spacing_mode_is_compact():
    engine = make_engine()
    assert engine.spacing_mode == "compact"


def test_set_spacing_mode():
    engine = make_engine()
    engine.set_spacing_mode("normal")
    assert engine.spacing_mode == "normal"


def test_paragraph_style_contains_font():
    engine = make_engine()
    style = engine.style_for_paragraph()
    assert "Helvetica" in style
    assert "12px" in style
    assert "#333333" in style


def test_heading_style_varies_by_level():
    engine = make_engine()
    h1 = engine.style_for_heading(1)
    h3 = engine.style_for_heading(3)
    assert "26px" in h1
    assert "16px" in h3
    assert "Helvetica" in h1
    assert "#2c3e50" in h1


def test_spacing_changes_paragraph_margin():
    engine = make_engine()
    compact = engine.style_for_paragraph()
    engine.set_spacing_mode("normal")
    normal = engine.style_for_paragraph()
    # compact uses "1px 0", normal uses "4px 0"
    assert "1px 0" in compact
    assert "4px 0" in normal


def test_code_inline_style():
    engine = make_engine()
    style = engine.style_for_code_inline()
    assert "Fira Code" in style or "Consolas" in style
    assert "#f4f4f4" in style


def test_code_block_style():
    engine = make_engine()
    style = engine.style_for_code_block()
    assert "border" in style
    assert "#f4f4f4" in style


def test_link_style():
    engine = make_engine()
    style = engine.style_for_link()
    assert "#2980b9" in style
    assert "underline" in style


def test_blockquote_style():
    engine = make_engine()
    style = engine.style_for_blockquote()
    assert "border-left" in style
    assert "#666666" in style


def test_table_cell_head():
    engine = make_engine()
    head_style = engine.style_for_table_cell(head=True)
    body_style = engine.style_for_table_cell(head=False)
    assert "font-weight: bold" in head_style
    assert "font-weight: bold" not in body_style


def test_table_cell_align():
    engine = make_engine()
    style = engine.style_for_table_cell(align="center")
    assert "text-align: center" in style


def test_strikethrough_style():
    engine = make_engine()
    style = engine.style_for_strikethrough()
    assert "line-through" in style


def test_underline_style():
    engine = make_engine()
    style = engine.style_for_underline()
    assert "underline" in style


def test_outline_styles():
    engine = make_engine()
    styles = engine.outline_styles
    assert styles == [
        "upper-roman",
        "upper-alpha",
        "decimal",
        "lower-alpha",
        "lower-roman",
    ]


def test_hr_style():
    engine = make_engine()
    style = engine.style_for_hr()
    assert "border" in style


def test_list_style():
    engine = make_engine()
    style = engine.style_for_list()
    assert "list-style-type: none" in style


def test_list_item_style():
    engine = make_engine()
    style = engine.style_for_list_item()
    assert "Helvetica" in style
