class OutlineFormatter:
    def __init__(self, styles: list[str]) -> None:
        self.styles = styles

    def format_marker(self, depth: int, number: int) -> str:
        style = self.styles[depth % len(self.styles)]
        return self._convert(number, style) + "."

    def _convert(self, number: int, style: str) -> str:
        if style == "upper-roman":
            return self._to_roman(number).upper()
        elif style == "lower-roman":
            return self._to_roman(number).lower()
        elif style == "upper-alpha":
            return self._to_alpha(number).upper()
        elif style == "lower-alpha":
            return self._to_alpha(number).lower()
        elif style == "decimal":
            return str(number)
        return str(number)

    @staticmethod
    def _to_roman(num: int) -> str:
        values = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
        ]
        result = ""
        for value, numeral in values:
            while num >= value:
                result += numeral
                num -= value
        return result

    @staticmethod
    def _to_alpha(num: int) -> str:
        result = ""
        while num > 0:
            num -= 1
            result = chr(ord("A") + num % 26) + result
            num //= 26
        return result
