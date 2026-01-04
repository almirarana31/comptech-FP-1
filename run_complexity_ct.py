"""Run empirical complexity measurements on ct.py components.

This script uses `complexity_counter.measure_complexity` to analyze several
functions from `ct.py`: tokenization (Lexer), parsing (Parser), orthography
validation, and full translation (Translator.translate).
"""
from complexity_counter import measure_complexity

import ct


def make_javanese(n: int) -> str:
    # repeat a small Javanese phrase to reach ~n characters
    unit = "ꦲꦏꦸꦩꦔꦤ꧀ꦱꦼꦒ "  # ~10-12 chars
    if n <= 0:
        return ""
    reps = max(1, n // max(1, len(unit)))
    s = (unit * reps).strip()
    # trim or pad to length approx n
    return s[:n]


def input_gen_text(n: int):
    return (make_javanese(n),), {}


@measure_complexity(input_gen=input_gen_text, sizes=(200, 500, 1000, 2000, 4000), repeats=3)
def bench_tokenize(text: str):
    lexer = ct.Lexer(text)
    while True:
        tok = lexer.get_next_token()
        if tok.type == ct.TokenType.EOF:
            break


@measure_complexity(input_gen=input_gen_text, sizes=(200, 500, 1000, 2000, 4000), repeats=3)
def bench_validate(text: str):
    reporter = ct.ErrorReporter(text)
    v = ct.OrthographyValidator(text, reporter, debug=False)
    v.validate()


@measure_complexity(input_gen=input_gen_text, sizes=(200, 500, 1000, 2000), repeats=2)
def bench_parse(text: str):
    lexer = ct.Lexer(text)
    parser = ct.Parser(lexer, debug=False, reporter=ct.ErrorReporter(text))
    parser.parse()


@measure_complexity(input_gen=input_gen_text, sizes=(100, 200, 400, 800), repeats=2)
def bench_translate(text: str):
    tr = ct.Translator(debug=False)
    tr.translate(text, show_analysis=False)


def main():
    print("Running benchmarks on ct.py components...\n")

    print("Tokenization:")
    t0 = bench_tokenize.analyze()
    print(t0)

    print("\nOrthography validation:")
    t1 = bench_validate.analyze()
    print(t1)

    print("\nParsing:")
    t2 = bench_parse.analyze()
    print(t2)

    print("\nTranslation:")
    t3 = bench_translate.analyze()
    print(t3)


if __name__ == '__main__':
    main()
