import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import mistune
from plugins import plugin_underline


def make_md():
    return mistune.create_markdown(plugins=[plugin_underline])


def test_basic_underline():
    md = make_md()
    result = md("++hello++")
    assert "<u>" in result
    assert "hello" in result
    assert "</u>" in result


def test_underline_with_other_text():
    md = make_md()
    result = md("This is ++underlined++ text.")
    assert "<u>" in result
    assert "underlined" in result


def test_underline_with_bold_inside():
    md = make_md()
    result = md("++**bold underline**++")
    assert "<u>" in result
    assert "<strong>" in result


def test_no_underline_without_closing():
    md = make_md()
    result = md("++not closed")
    assert "<u>" not in result


def test_no_underline_with_spaces():
    md = make_md()
    # ++ followed by space should not trigger underline
    result = md("++ not underlined ++")
    assert "<u>" not in result


def test_multiple_underlines():
    md = make_md()
    result = md("++first++ and ++second++")
    assert result.count("<u>") == 2
    assert result.count("</u>") == 2
