# Markdown to Styled HTML Converter

## Project Overview

A Python tool that converts Markdown into richly formatted HTML with fine-grained control over appearance and font styling. The output HTML must be copy/paste compatible with rich text email clients (Outlook) and Word documents.

## Core Technology

- **Parser**: `mistune` — chosen for its custom renderer architecture and plugin system, which allows element-level control over HTML output.
- **Configuration**: YAML config file for all styling (fonts, sizes, spacing, colors).
- **Output**: Self-contained HTML with all styles inlined on every element (no `<style>` blocks, no external CSS, no CSS classes).

## Architecture

```
config.yaml           # all styling: fonts, sizes, spacing, colors, outline styles
├── converter.py      # main entry point: MD in → styled HTML out
├── renderer.py       # custom mistune HTMLRenderer subclass, applies inline styles from config
├── plugins.py        # custom inline syntax rules (underline, compact toggle)
├── outline.py        # generates outline markers as literal text (I, A, 1, a, i)
└── style_engine.py   # loads config.yaml, resolves styles per element type
```

## Key Requirements

### 1. Inline Styles Only

All CSS must be applied as `style="..."` attributes directly on each HTML element. This is required because:
- Outlook and Word ignore `<style>` blocks and external stylesheets.
- Inline styles are preserved when copying rendered HTML from a browser and pasting into Outlook or Word.

Do NOT use: CSS classes, `<style>` blocks, CSS variables, flexbox/grid, web fonts, or CSS counters.

### 2. Custom Inline Syntax Extensions

Implement these via mistune's plugin system by registering custom inline rules with regex patterns:

- **Strikethrough**: `~~text~~` → `<del>` or `<s>` with inline style. Mistune has a built-in plugin for this.
- **Underline**: `++text++` → `<u>` or `<span style="text-decoration: underline;">`. Must use a delimiter that doesn't conflict with existing Markdown syntax. Do NOT use `__text__` as it conflicts with bold.

### 3. True Nested Outline Formatting

Standard Markdown list nesting provides no visual distinction between outline levels. This tool must:

- Track nesting depth during list rendering.
- Generate outline markers as **literal text content** in the HTML (e.g., "I.", "A.", "1.", "a.", "i."), NOT via CSS `list-style-type` or CSS counters (these get stripped on paste into Outlook/Word).
- Support configurable outline level styles via config.yaml.

Default outline progression:
1. `upper-roman` (I, II, III)
2. `upper-alpha` (A, B, C)
3. `decimal` (1, 2, 3)
4. `lower-alpha` (a, b, c)
5. `lower-roman` (i, ii, iii)

### 4. Compact Vertical Spacing

Standard Markdown renderers use excessive vertical spacing. This tool must:

- Default to tight spacing globally — minimal margins/padding on paragraphs, headings, list items.
- Support a **spacing toggle** in the Markdown source to switch between "normal" and "compact" profiles. Proposed syntax: `<!-- compact -->` and `<!-- normal -->` comment markers in the source.
- Both spacing profiles are defined in config.yaml.

### 5. Configurable Styling via config.yaml

All visual properties are externalized. The config file structure:

```yaml
spacing:
  normal:
    paragraph_margin: "4px 0"
    heading_margin: "8px 0 4px 0"
    list_item_margin: "2px 0"
  compact:
    paragraph_margin: "1px 0"
    heading_margin: "4px 0 2px 0"
    list_item_margin: "0"

fonts:
  body: "Helvetica, Arial, sans-serif"
  heading: "Georgia, serif"
  code: "Fira Code, Consolas, monospace"

font_sizes:
  h1: "28px"
  h2: "22px"
  h3: "18px"
  h4: "16px"
  h5: "14px"
  h6: "13px"
  body: "14px"
  code: "13px"

colors:
  heading: "#2c3e50"
  body: "#333333"
  code_bg: "#f4f4f4"
  link: "#2980b9"

outline_styles:
  - "upper-roman"
  - "upper-alpha"
  - "decimal"
  - "lower-alpha"
  - "lower-roman"
```

### 6. Copy/Paste Compatibility

The rendered HTML must paste correctly into:

- **Outlook** (desktop and web): Font family, size, weight, color, italic, underline, strikethrough, line-height, margins, lists, tables.
- **Microsoft Word**: Same as above.

**Things that do NOT survive paste** (avoid these):
- CSS classes
- `<style>` blocks
- CSS variables (`var(--x)`)
- Flexbox / Grid
- Web fonts (will fall back to system fonts — always specify system font fallbacks)
- CSS counters (hence outline markers must be literal text)

### 7. Output Format

The tool produces a self-contained HTML file. Workflow:
1. Open the HTML file in a browser.
2. Select all / select portion.
3. Copy.
4. Paste into Outlook or Word — formatting is preserved.

## Future Considerations

- **Direct .docx export**: Could add a `python-docx` export path that maps the same config.yaml styles to Word paragraph/character styles. Not in initial scope.
- **PDF export**: Possible future addition.
- **CLI interface**: Accept input file, output file, and optional config path as arguments.

## Dependencies

- `mistune` — Markdown parsing and rendering
- `pyyaml` — Config file loading

## Coding Conventions

- Clean, modular code — each module has a single responsibility.
- Minimal exception handling — let errors surface naturally during development.
- Type hints on function signatures.
- No unnecessary abstractions — keep it direct and readable.
