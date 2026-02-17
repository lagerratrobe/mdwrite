import os
import sys
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from converter import convert

SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "sample.md")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")


def read_sample():
    with open(SAMPLE_PATH) as f:
        return f.read()


def test_convert_produces_html():
    html = convert(read_sample(), config_path=CONFIG_PATH)
    assert "<!DOCTYPE html>" in html
    assert "<html>" in html
    assert "</html>" in html


def test_convert_has_body():
    html = convert(read_sample(), config_path=CONFIG_PATH)
    assert "<body>" in html
    assert "</body>" in html


def test_convert_title():
    html = convert("# Hello", config_path=CONFIG_PATH, title="My Doc")
    assert "<title>My Doc</title>" in html


def test_convert_default_title():
    html = convert("# Hello", config_path=CONFIG_PATH)
    assert "<title>Document</title>" in html


def test_convert_no_style_blocks():
    html = convert(read_sample(), config_path=CONFIG_PATH)
    assert "<style>" not in html


def test_convert_no_css_classes_in_content():
    html = convert(read_sample(), config_path=CONFIG_PATH)
    body_start = html.index("<body>")
    body_end = html.index("</body>")
    body = html[body_start:body_end]
    assert 'class="' not in body


def test_convert_all_elements_present():
    html = convert(read_sample(), config_path=CONFIG_PATH)
    # Headings
    assert "<h1 style=" in html
    assert "<h2 style=" in html
    # Paragraphs
    assert "<p style=" in html
    # Bold and italic
    assert "<strong>" in html
    assert "<em>" in html
    # Code
    assert "<code" in html
    # Links
    assert '<a href=' in html
    # Lists
    assert "<ol style=" in html
    assert "<ul style=" in html
    assert "<li style=" in html
    # Blockquote
    assert "<blockquote style=" in html
    # Table
    assert "<table style=" in html
    # HR
    assert "<hr style=" in html


def test_convert_outline_markers():
    html = convert(read_sample(), config_path=CONFIG_PATH)
    # The sample has nested ordered lists - check outline markers
    assert "I." in html
    assert "A." in html


def test_convert_strikethrough():
    html = convert(read_sample(), config_path=CONFIG_PATH)
    assert "<del style=" in html


def test_convert_underline():
    html = convert(read_sample(), config_path=CONFIG_PATH)
    assert "<u style=" in html


def test_convert_inline_code():
    html = convert(read_sample(), config_path=CONFIG_PATH)
    assert '<code style="' in html


def test_convert_spacing_toggle():
    html = convert(read_sample(), config_path=CONFIG_PATH)
    # The sample has <!-- compact --> and <!-- normal --> toggles
    # They should not appear in the output
    assert "<!-- compact -->" not in html
    assert "<!-- normal -->" not in html


def test_cli_writes_file():
    """Test that the CLI entry point works end-to-end."""
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        html = convert(read_sample(), config_path=CONFIG_PATH)
        with open(tmp_path, "w") as f:
            f.write(html)
        with open(tmp_path) as f:
            content = f.read()
        assert "<!DOCTYPE html>" in content
        assert "<body>" in content
    finally:
        os.unlink(tmp_path)
