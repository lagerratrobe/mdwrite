# mdwrite

Markdown to styled HTML converter. Produces self-contained HTML with all styles inlined on every element, so the output pastes correctly into Outlook and Word with full formatting preserved.

## Installation

Requires Python 3.12+.

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install mistune pyyaml

# (Optional) Install pytest for running tests
pip install pytest
```

## Usage

### Command Line

```bash
python converter.py INPUT.md [-o OUTPUT.html] [-c CONFIG.yaml] [-t TITLE]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `INPUT.md` | Path to the Markdown file to convert |
| `-o`, `--output` | Output HTML path (default: `INPUT.html`) |
| `-c`, `--config` | Path to a custom `config.yaml` (default: built-in) |
| `-t`, `--title` | HTML document title (default: `Document`) |

**Examples:**

```bash
# Basic conversion (outputs report.html)
python converter.py report.md

# Specify output file
python converter.py report.md -o styled_report.html

# Use custom config and title
python converter.py report.md -o out.html -c my_config.yaml -t "Q4 Report"
```

### As a Python Library

```python
from converter import convert

md_text = "# Hello\n\nThis is **bold** and *italic*."
html = convert(md_text)

# With options
html = convert(md_text, config_path="my_config.yaml", title="My Document")
```

### Workflow

1. Write your content in Markdown (`.md` file)
2. Run `python converter.py yourfile.md`
3. Open the generated `.html` file in a browser
4. Select all (Ctrl+A) or select a portion
5. Copy (Ctrl+C)
6. Paste into Outlook or Word -- formatting is preserved

## Markdown Features

### Standard Formatting

```markdown
**bold**    *italic*    ***bold italic***
`inline code`
[link text](https://example.com)
![alt text](image.png)
```

### Strikethrough

```markdown
~~deleted text~~
```

### Underline

Uses `++text++` syntax (double plus signs):

```markdown
++underlined text++
```

### Ordered Lists

By default, ordered lists render with plain decimal numbers (1., 2., 3.) at all nesting depths.

Use `<!-- outline -->` to switch to hierarchical outline markers, and `<!-- numbered -->` to switch back:

```markdown
1. First item (renders as 1.)
2. Second item (renders as 2.)

<!-- outline -->

1. First level (renders as I., II., III.)
   1. Second level (renders as A., B., C.)
      1. Third level (renders as 1., 2., 3.)
         1. Fourth level (renders as a., b., c.)
            1. Fifth level (renders as i., ii., iii.)

<!-- numbered -->

1. Back to plain numbers (renders as 1.)
```

The outline style sequence is configurable in `config.yaml`.

### Spacing Modes

Insert HTML comments to toggle between compact and normal spacing:

```markdown
<!-- compact -->
Tight spacing in this section.

<!-- normal -->
More breathing room in this section.
```

The default mode is compact. Both profiles are defined in `config.yaml`.

### Tables

Standard Markdown tables with alignment:

```markdown
| Left   | Center | Right |
|:-------|:------:|------:|
| a      | b      | c     |
```

### Other Elements

Code blocks, blockquotes, horizontal rules, images, and headings (h1-h6) are all supported with full inline styling.

## Configuration

All visual properties are in `config.yaml`. Edit it to change fonts, sizes, colors, spacing, and outline styles.

Key sections:

- **`spacing.compact`** / **`spacing.normal`** -- margins for paragraphs, headings, lists, etc.
- **`fonts`** -- font families for body, heading, and code
- **`font_sizes`** -- sizes for h1-h6, body, and code
- **`colors`** -- colors for text, headings, links, code backgrounds, etc.
- **`outline_styles`** -- ordered list marker progression (e.g., upper-roman, upper-alpha, decimal)

## Running Tests

```bash
python -m pytest tests/ -v
```

A sample Markdown file exercising all features is at `tests/sample.md`.

## Architecture

```
config.yaml        All styling: fonts, sizes, spacing, colors, outline styles
converter.py        Main entry point: MD in, styled HTML out, CLI interface
renderer.py         Custom mistune HTMLRenderer, applies inline styles from config
plugins.py          Custom inline syntax (++underline++)
outline.py          Generates outline markers as literal text (I, A, 1, a, i)
style_engine.py     Loads config.yaml, resolves styles per element type
tests/
  sample.md         Sample Markdown exercising all features
  test_converter.py Integration tests
  test_renderer.py  Renderer output tests
  test_plugins.py   Underline plugin tests
  test_outline.py   Outline number formatting tests
  test_style_engine.py  Style resolution tests
```
