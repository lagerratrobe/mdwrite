import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from outline import OutlineFormatter


DEFAULT_STYLES = [
    "upper-roman",
    "upper-alpha",
    "decimal",
    "lower-alpha",
    "lower-roman",
]


def test_upper_roman_basic():
    fmt = OutlineFormatter(DEFAULT_STYLES)
    assert fmt.format_marker(0, 1) == "I."
    assert fmt.format_marker(0, 2) == "II."
    assert fmt.format_marker(0, 3) == "III."
    assert fmt.format_marker(0, 4) == "IV."
    assert fmt.format_marker(0, 5) == "V."


def test_upper_roman_larger():
    fmt = OutlineFormatter(DEFAULT_STYLES)
    assert fmt.format_marker(0, 9) == "IX."
    assert fmt.format_marker(0, 10) == "X."
    assert fmt.format_marker(0, 14) == "XIV."
    assert fmt.format_marker(0, 40) == "XL."
    assert fmt.format_marker(0, 50) == "L."


def test_upper_alpha():
    fmt = OutlineFormatter(DEFAULT_STYLES)
    assert fmt.format_marker(1, 1) == "A."
    assert fmt.format_marker(1, 2) == "B."
    assert fmt.format_marker(1, 3) == "C."
    assert fmt.format_marker(1, 26) == "Z."


def test_decimal():
    fmt = OutlineFormatter(DEFAULT_STYLES)
    assert fmt.format_marker(2, 1) == "1."
    assert fmt.format_marker(2, 5) == "5."
    assert fmt.format_marker(2, 10) == "10."


def test_lower_alpha():
    fmt = OutlineFormatter(DEFAULT_STYLES)
    assert fmt.format_marker(3, 1) == "a."
    assert fmt.format_marker(3, 2) == "b."
    assert fmt.format_marker(3, 26) == "z."


def test_lower_roman():
    fmt = OutlineFormatter(DEFAULT_STYLES)
    assert fmt.format_marker(4, 1) == "i."
    assert fmt.format_marker(4, 2) == "ii."
    assert fmt.format_marker(4, 3) == "iii."
    assert fmt.format_marker(4, 4) == "iv."


def test_depth_wraps_around():
    fmt = OutlineFormatter(DEFAULT_STYLES)
    # Depth 5 should wrap back to upper-roman (index 0)
    assert fmt.format_marker(5, 1) == "I."
    assert fmt.format_marker(6, 1) == "A."


def test_alpha_beyond_26():
    fmt = OutlineFormatter(DEFAULT_STYLES)
    # 27 should be AA
    assert fmt.format_marker(1, 27) == "AA."
    assert fmt.format_marker(1, 28) == "AB."


def test_custom_styles():
    fmt = OutlineFormatter(["decimal", "lower-alpha"])
    assert fmt.format_marker(0, 1) == "1."
    assert fmt.format_marker(1, 1) == "a."
    assert fmt.format_marker(2, 1) == "1."  # wraps
