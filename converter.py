import argparse
import sys
from pathlib import Path
from typing import Optional

import mistune
from mistune.plugins.formatting import strikethrough
from mistune.plugins.table import table

from plugins import plugin_underline
from renderer import StyledRenderer
from style_engine import StyleEngine

HTML_WRAPPER = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
</head>
<body>
{body}
</body>
</html>"""


def convert(md_text: str, config_path: Optional[str] = None, title: str = "Document") -> str:
    style_engine = StyleEngine(config_path)
    renderer = StyledRenderer(style_engine)
    md = mistune.create_markdown(
        renderer=renderer,
        plugins=[strikethrough, table, plugin_underline],
    )
    body = md(md_text)
    return HTML_WRAPPER.format(title=title, body=body)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mdwrite",
        description="Convert Markdown to styled HTML optimized for Outlook/Word paste.",
    )
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument(
        "-o", "--output",
        help="Output HTML file (default: <input>.html)",
    )
    parser.add_argument(
        "-c", "--config",
        help="Path to config.yaml (default: built-in config)",
    )
    parser.add_argument(
        "-t", "--title",
        default="Document",
        help="HTML document title (default: Document)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    md_text = input_path.read_text(encoding="utf-8")

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".html")

    html = convert(md_text, config_path=args.config, title=args.title)
    output_path.write_text(html, encoding="utf-8")
    print(f"Wrote {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
