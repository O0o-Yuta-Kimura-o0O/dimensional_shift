#!/usr/bin/env python3
"""Export the paper's documented Typst subset to Markdown without rewording prose.

The two Typst bodies are authoritative. Equations use shared IDs with explicitly
reviewed Typst/LaTeX representations. This is intentionally not a general parser.
"""
import argparse
import json
from pathlib import Path
import re

LANGUAGES = {'ja': 'dimensional_shift', 'en': 'dimensional_shift_en'}
START = '// BEGIN PAPER CONTENT'
END = '// END PAPER CONTENT'
INLINE = re.compile(r'#m\("([a-zA-Z0-9_]+)"\)')
DISPLAY = re.compile(r'^#eq\("([a-zA-Z0-9_]+)"\)$')
LINK = re.compile(r'#link\("([^"\n]+)"\)\[([^\]\n]+)\]')
BOLD = re.compile(r'(?<!\*)\*([^*\n]+)\*(?!\*)')


def get_body(source):
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError('Expected exactly one pair of paper body markers')
    return source.split(START, 1)[1].split(END, 1)[0].strip()


def export_text(source, lang, config, formulas):
    body = get_body(source)
    title = config['titles'][lang].replace('\n', ' ')
    author = ('木村祐太・GPT-6 Astra（AI）' if lang == 'ja'
              else '木村祐太 (Yuta Kimura) · GPT-6 Astra (AI)')
    lines = [f'# {title}', '', config['subtitles'][lang], '', author, '',
             f"{config['date']} · {config['version']}", '']
    section_number = 0
    equation_number = 0
    display_ids = []
    all_ids = []
    for original in body.splitlines():
        line = original.strip()
        if line == '#pagebreak()':
            continue
        if line.startswith('//'):
            raise ValueError('Comments inside the paper body are not supported')
        display = DISPLAY.fullmatch(line)
        if display:
            key = display.group(1)
            equation_number += 1
            display_ids.append(key)
            all_ids.append(key)
            lines.extend(['', '$$', formulas[key]['latex'] + rf'\tag{{{equation_number}}}', '$$', ''])
            continue
        if line.startswith('== '):
            line = '## ' + line[3:]
        elif line.startswith('= '):
            section_number += 1
            line = f'## {section_number}. ' + line[2:]
        else:
            line = BOLD.sub(lambda m: '**' + m.group(1) + '**', line)
        line = LINK.sub(lambda m: f'[{m.group(2)}]({m.group(1)})', line)
        def inline(match):
            key = match.group(1)
            all_ids.append(key)
            return '$' + formulas[key]['latex'] + '$'
        line = INLINE.sub(inline, line)
        if re.search(r'#(?:m|eq|link|pagebreak)\b', line):
            raise ValueError(f'Unprocessed macro: {original}')
        if '#' in line and not line.startswith('## '):
            raise ValueError(f'Unsupported Typst code in body: {original}')
        lines.append(line)
    result = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip() + '\n'
    return result, display_ids, all_ids


def export_all(root):
    root = Path(root)
    current = root / 'output/current'
    config = json.loads((current / 'paper_config.json').read_text(encoding='utf-8'))
    formulas = json.loads((current / 'equations.json').read_text(encoding='utf-8'))
    outputs = {}
    for lang, stem in LANGUAGES.items():
        source = (current / f'{stem}.typ').read_text(encoding='utf-8')
        outputs[lang] = export_text(source, lang, config, formulas)
    if outputs['ja'][1] != outputs['en'][1]:
        raise ValueError('Display equation IDs/order differ between language editions')
    if outputs['ja'][2] != outputs['en'][2]:
        raise ValueError('Inline or display equation IDs/order differ between language editions')
    for lang, stem in LANGUAGES.items():
        (current / f'{stem}.md').write_text(outputs[lang][0], encoding='utf-8')
    return [current / f'{stem}.md' for stem in LANGUAGES.values()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    for path in export_all(Path(__file__).resolve().parents[1]):
        print(f'Exported {path}')


if __name__ == '__main__':
    main()
