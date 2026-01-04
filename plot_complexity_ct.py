"""Measure ct.py components over a range of input sizes and plot results.

Generates CSV `complexity_results.csv` and plots `complexity_times.png` and
`complexity_times_loglog.png` in the workspace.
"""
import time
import tracemalloc
import statistics
import csv
import json
import os
from typing import List, Tuple

import ct


def make_javanese(n: int) -> str:
    unit = "ꦲꦏꦸꦩꦔꦤ꧀ꦱꦼꦒ "
    if n <= 0:
        return ""
    reps = max(1, n // max(1, len(unit)))
    s = (unit * reps).strip()
    return s[:n]


def measure(func, sizes: List[int], repeats: int = 5):
    results = []
    for n in sizes:
        times = []
        mems = []
        text = make_javanese(n)
        for _ in range(repeats):
            tracemalloc.start()
            t0 = time.perf_counter()
            try:
                func(text)
            except Exception:
                # on error record inf time
                t0 = None
            t1 = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            if t0 is None:
                times.append(float('inf'))
            else:
                times.append(t1 - t0)
            mems.append(peak / 1024.0)

        results.append((n, statistics.median(times), statistics.median(mems)))
    return results


def wrapper_tokenize(text: str):
    lexer = ct.Lexer(text)
    while True:
        tok = lexer.get_next_token()
        if tok.type == ct.TokenType.EOF:
            break


def wrapper_validate(text: str):
    reporter = ct.ErrorReporter(text)
    v = ct.OrthographyValidator(text, reporter, debug=False)
    v.validate()


def wrapper_parse(text: str):
    lexer = ct.Lexer(text)
    parser = ct.Parser(lexer, debug=False, reporter=ct.ErrorReporter(text))
    parser.parse()


def wrapper_translate(text: str):
    import sys, io
    tr = ct.Translator(debug=False)
    old = sys.stdout
    sys.stdout = io.StringIO()
    try:
        tr.translate(text, show_analysis=False)
    finally:
        sys.stdout = old


def save_csv(path: str, data: dict):
    # data: {name: [(n,time,mem), ...]}
    rows = []
    names = sorted(data.keys())
    sizes = [r[0] for r in data[names[0]]]
    header = ['size']
    for name in names:
        header += [f'{name}_time', f'{name}_mem_kb']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i, n in enumerate(sizes):
            row = [n]
            for name in names:
                row += [data[name][i][1], data[name][i][2]]
            writer.writerow(row)


def save_html_plot(path: str, data: dict):
    # Embed JSON data and use Chart.js from CDN to render a log-log plot
    payload = {}
    for k, vals in data.items():
        payload[k] = { 'sizes': [v[0] for v in vals], 'times': [v[1] for v in vals], 'mems': [v[2] for v in vals] }

    payload_json = json.dumps(payload)

    html = (
        '<!doctype html>\n'
        '<html>\n'
        '<head>\n'
        '  <meta charset="utf-8">\n'
        '  <title>ct.py Complexity Plot</title>\n'
        '  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n'
        '  <style>body{font-family:Arial,Helvetica,sans-serif;padding:20px}</style>\n'
        '</head>\n'
        '<body>\n'
        '  <h2>ct.py Component Timings</h2>\n'
        '  <canvas id="chart" width="1000" height="500"></canvas>\n'
        '  <script>\n'
        '    const data = ' + payload_json + ';\n'
        '    const ctx = document.getElementById("chart").getContext("2d");\n'
        '    const datasets = Object.keys(data).map((k, i) => ({\n'
        '      label: k,\n'
        '      data: data[k].sizes.map((s, idx) => ({x: s, y: data[k].times[idx]})),\n'
        '      borderWidth: 2,\n'
        '      fill: false,\n'
        '      pointRadius: 4\n'
        '    }));\n'
        '    new Chart(ctx, {\n'
        '      type: "line",\n'
        '      data: { datasets },\n'
        '      options: {\n'
        '        scales: {\n'
        "          x: { type: 'logarithmic', title: { display: true, text: 'input size (chars)' } },\n"
        "          y: { type: 'logarithmic', title: { display: true, text: 'median time (s)' } }\n"
        '        },\n'
        '        plugins: { legend: { position: "bottom" } }\n'
        '      }\n'
        '    });\n'
        '  </script>\n'
        '</body>\n'
        '</html>\n'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


def plot_times(*args, **kwargs):
    # matplotlib plotting removed; HTML/Chart.js is used instead
    raise NotImplementedError('Use save_html_plot to generate interactive plots')


def main():
    sizes = [100, 200, 400, 800, 1600, 3200, 6400]
    repeats = 5

    print('Measuring tokenization...')
    t_token = measure(wrapper_tokenize, sizes, repeats=repeats)
    print('Measuring validation...')
    t_validate = measure(wrapper_validate, sizes, repeats=repeats)
    print('Measuring parsing...')
    t_parse = measure(wrapper_parse, sizes, repeats=3)
    print('Measuring translation (may be slower)...')
    t_translate = measure(wrapper_translate, sizes, repeats=2)

    results = {
        'tokenize': t_token,
        'validate': t_validate,
        'parse': t_parse,
        'translate': t_translate,
    }

    out_csv = 'complexity_results.csv'
    save_csv(out_csv, results)
    print(f'Wrote {out_csv}')

    out_html = 'complexity_plot.html'
    save_html_plot(out_html, results)
    print(f'Saved {out_html} (open in a browser)')

    with open('complexity_results.json', 'w', encoding='utf-8') as f:
        json.dump({k: v for k, v in results.items()}, f, default=lambda o: o, indent=2)


if __name__ == '__main__':
    main()
