#!/usr/bin/env python3
"""Generate a source/symbol catalogue and faithful indexed graphics previews.

Read-only analysis of the preservation inputs and a previously built PRG.
This is a static catalogue, not a control-flow or 6502-cycle emulator.
"""

import argparse
import ast
import collections
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

from restore_c16 import ROOT, prepare_sources
from source_converter import OPCODES, flatten, split_comment


def table(headers, rows):
    rows = [[str(c).replace('|', '/') for c in row] for row in [headers] + rows]
    widths = [max(3, max(len(row[i]) for row in rows)) for i in range(len(headers))]
    if max(widths) > 45:
        raise ValueError('Markdown table cell exceeds 45 characters')
    fmt = lambda row: '| ' + ' | '.join(v.ljust(widths[i]) for i, v in enumerate(row)) + ' |'
    return '\n'.join([fmt(rows[0]), fmt(['-' * w for w in widths])] + [fmt(r) for r in rows[1:]])


def parse_line(line):
    code, comment = split_comment(line)
    code = code.strip()
    definition = None
    if code and not code.startswith('.') and not code.startswith('*'):
        first, *rest = code.split(None, 1)
        if first not in OPCODES | {'DPINC', 'DPDEC'} and re.fullmatch(r'[A-Z][A-Z0-9_]*', first):
            definition = first
            code = rest[0] if rest else ''
        else:
            match = re.match(r'^([A-Z][A-Z0-9_]*)\s*=', code)
            if match:
                definition = match[1]
                code = code[len(definition):].lstrip()
    return definition, code, comment.lstrip(';* ')


def listing_owners(path):
    """Use printed PC changes so abbreviated long data lines retain full size."""
    owners = {}
    owner = None
    address = None
    pending = None
    for line in path.read_text().splitlines():
        match = re.match(r'^([0-9A-F]{6})[ r]', line)
        if not match:
            continue
        current = int(match[1], 16)
        if address is not None and current != address:
            if pending and 0 < current-address <= 0x2400:
                for a in range(max(address, 0x1800), min(current, 0x3C00)):
                    owners[a] = pending
            pending = None
        address = current
        source = re.search(r'; SOURCE: (.+):\d+$', line)
        if source:
            owner = source[1]
        if re.fullmatch(r'(?:(?:[0-9A-F]{2}|xx)\s*)+', line[11:23].strip()):
            pending = owner
    return owners


def atlas(path, title, data, start, mode, columns=16):
    """Decode original glyph bits to SVG; colors are index keys, not a TED palette."""
    count = len(data) // 8
    cell_w, cell_h, scale = 60, 70, 5
    height = 75 + ((count+columns-1)//columns)*cell_h
    colors = ['#111827', '#ef4444', '#38bdf8', '#fef08a']
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{columns*cell_w}" height="{height}" viewBox="0 0 {columns*cell_w} {height}">',
           '<rect width="100%" height="100%" fill="#f8fafc"/>',
           f'<text x="12" y="24" font-family="monospace" font-size="16">{html.escape(title)}</text>',
           '<text x="12" y="45" font-family="monospace" font-size="12">Raw glyph bytes; neutral index colors; not final in-game palette.</text>']
    for i in range(count):
        x, y = (i % columns)*cell_w+10, (i//columns)*cell_h+65
        glyph = data[i*8:(i+1)*8]
        for row, byte in enumerate(glyph):
            width = 4 if mode == 'multicolor' else 8
            for col in range(width):
                value = (byte >> (6-col*2)) & 3 if mode == 'multicolor' else (byte >> (7-col)) & 1
                color = colors[value] if mode == 'multicolor' else ['#111827', '#e2e8f0'][value]
                w = scale*2 if mode == 'multicolor' else scale
                out.append(f'<rect x="{x+col*w}" y="{y+row*scale}" width="{w}" height="{scale}" fill="{color}"/>')
        out.append(f'<text x="{x}" y="{y+53}" font-family="monospace" font-size="10">{i:03d} {start+i*8:04X}</text>')
    out.append('</svg>')
    path.write_text('\n'.join(out)+'\n')


def analyze(build, output):
    output.mkdir(parents=True, exist_ok=True)
    sources, manifest = prepare_sources(build / 'analysis-inputs')
    provenance = {r['name']: r for r in manifest['files']}
    labels = {name: int(address, 16) for address, name in re.findall(
        r'^al ([0-9A-Fa-f]+) \.(\w+)$', (build/'tycoon.labels').read_text(), re.M)}
    roots = ['TYCOON-TEX', 'SET#1-CHAR/ASSEM', 'SET#2-CHAR/ASSEM']
    stages = {name: list(dict.fromkeys(row[0] for row in flatten(sources, name))) for name in roots}
    main = set(stages['TYCOON-TEX'])
    owners = listing_owners(build/'tycoon.lst')
    code = (build/'recovered-code.bin').read_bytes()
    if set(owners) != set(range(0x1800, 0x1800+len(code))):
        raise ValueError('Listing ownership does not cover the complete assembled region')
    sizes = collections.Counter(owners.values())
    definitions = {}
    modules = []
    transfers = []
    variables = []
    for name, lines in sources.items():
        instruction_lines = 0
        for number, line in enumerate(lines, 1):
            definition, body, comment = parse_line(line)
            if definition:
                kind = 'equate' if body.startswith('=') else 'label'
                if '*=*+' in body:
                    kind = 'reserved'
                elif body.startswith(('.BYTE', '.WORD')):
                    kind = 'data'
                definitions[definition] = {'symbol': definition, 'module': name, 'line': number,
                                           'address': labels.get(definition) if name in main else None,
                                           'kind': kind, 'comment': comment,
                                           'expression': body[1:].strip() if kind == 'equate' else None}
                if name == 'VARS' and kind == 'reserved':
                    size_text = body.split('*=*+', 1)[1]
                    size = int(size_text[1:], 16) if size_text.startswith('$') else int(size_text)
                    variables.append({'symbol': definition, 'address': labels[definition],
                                      'bytes': size, 'comment': comment, 'source_line': number})
            op = body.split(None, 1)
            if op and op[0] in OPCODES:
                instruction_lines += 1
            if name in main and op and op[0] in {'JSR','JMP','BCC','BCS','BEQ','BMI','BNE','BPL','BVC','BVS'} and len(op)==2:
                transfers.append({'module': name, 'line': number, 'operation': op[0], 'operand': op[1]})
        modules.append({'name': name, 'path': provenance[name]['source'], 'fallback': provenance[name]['fallback'],
                        'raw_bytes': provenance[name]['bytes'],
                        'extracted_copy': provenance[name].get('extracted_copy'), 'logical_lines': len(lines),
                        'instruction_lines': instruction_lines, 'main_region_bytes': sizes[name],
                        'stages': [r for r in roots if name in stages[r]]})
    def constant(expression):
        expression = re.sub(r'\$([0-9A-F]+)', r'0x\1', expression)
        expression = re.sub(r'%([01]+)', r'0b\1', expression)
        def walk(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, int):
                return node.value
            if isinstance(node, ast.Name):
                value=definitions[node.id]['address']
                if value is None:raise ValueError(node.id)
                return value
            if isinstance(node, ast.BinOp):
                left,right=walk(node.left),walk(node.right)
                if isinstance(node.op, ast.Add):return left+right
                if isinstance(node.op, ast.Sub):return left-right
                if isinstance(node.op, ast.Mult):return left*right
            raise ValueError('Unsupported equate expression')
        return walk(ast.parse(expression,mode='eval').body)
    for _ in range(4):
        for definition in definitions.values():
            if definition['kind']=='equate' and definition['address'] is None:
                try:definition['address']=constant(definition['expression'])
                except (KeyError,ValueError,SyntaxError):pass
    # Plain forward labels are classified by their following non-comment statement.
    for definition in definitions.values():
        if definition['kind'] != 'label':
            continue
        for later in sources[definition['module']][definition['line']-1:]:
            _, body, _ = parse_line(later)
            if body:
                definition['kind'] = 'instruction-label' if body.split()[0] in OPCODES else 'data-or-control-label'
                break
    for transfer in transfers:
        target = re.match(r'^([A-Z][A-Z0-9_]*)', transfer['operand'])
        dest = definitions.get(target[1]) if target else None
        transfer['target_module'] = dest['module'] if dest and dest['module'] in main else None
        try:
            transfer['target_address'] = constant(transfer['operand'])
        except (KeyError, ValueError, SyntaxError):
            transfer['target_address'] = None
    symbols = sorted([d for d in definitions.values() if d['module'] in main], key=lambda d: d['symbol'])
    payload = (build/'tycoon-tex.prg').read_bytes()[2:]
    data = {
        'method': 'Static module catalogue and direct symbolic transfers; not a complete call graph or cycle profile',
        'source_image_sha256': manifest['image_sha256'],
        'prg_sha256': hashlib.sha256((build/'tycoon-tex.prg').read_bytes()).hexdigest(),
        'assembly_roots': stages, 'modules': modules, 'symbols': symbols,
        'zero_page_variables': variables, 'direct_transfers': transfers,
        'counts': {'available_source_records': len(sources), 'main_modules': len(main),
                   'active_modules': len(set(n for names in stages.values() for n in names)),
                   'main_logical_lines': sum(len(sources[n]) for n in main),
                   'main_instruction_lines': sum(m['instruction_lines'] for m in modules if m['name'] in main),
                   'main_symbol_definitions': len(symbols), 'direct_transfers': len(transfers),
                   'zero_page_bytes': sum(v['bytes'] for v in variables),
                   'main_region_bytes': sum(sizes.values())}}
    (output/'codebase-index.json').write_text(json.dumps(data, indent=2)+'\n')
    module_map = {m['name']: m for m in modules}
    text = '# Generated Code Reference\n\n## Scope and Method\n\nGenerated by `scripts/analyze_codebase.py` from the verified build and preserved sources. Logical source-line numbers refer to normalized module lines. Main-region spans include code, embedded data, and the reserved road buffer; they are not function sizes. Direct transfers omit fall-through, indirect control, vector dispatch, macro expansion, and runtime operand patches. Symbols may name internal branch points or data rather than callable routines.\n\n'
    text += '---\n\n## Main Modules in Assembly Order\n\n'
    text += table(['Module','Bytes','Lines','Origin'], [(f'`{n}`',sizes[n],len(sources[n]),'1992' if provenance[n]['fallback'] else '2026') for n in stages[roots[0]]])+'\n\n'
    text += '---\n\n## Source Locations\n\n'
    for name in sorted(sources):
        m=module_map[name]
        path = 'Original Source Recovered/2026/TycoonText-C16/'+provenance[name]['extracted_copy'] if not m['fallback'] else m['path']
        text += f"`{name}` – [preserved input](../../{quote(path, safe='/')}); {m['raw_bytes']} raw bytes, {m['logical_lines']} logical lines.\n\n"
    text += '---\n\n## Zero-Page Variables\n\n'
    text += table(['Symbol','Address','Bytes','Source line'],[(f"`{v['symbol']}`",f"`${v['address']:04X}`",v['bytes'],v['source_line']) for v in variables])+'\n\n'
    text += '---\n\n## Symbols by Module\n\n'
    for name in stages[roots[0]]:
        defs=[s for s in symbols if s['module']==name]
        if not defs:continue
        text += f'### {name}\n\n'
        text += table(['Symbol','Address','Line','Kind'],[(f"`{s['symbol']}`", f"`${s['address']:04X}`" if s['address'] is not None else 'equate / no linker label',s['line'],s['kind']) for s in defs])+'\n\n'
    (output/'CODE_REFERENCE.md').write_text(text)
    assets = {'note':'Hex payloads retain raw bytes; multicolor preview colors identify 2-bit indices, not a final palette.',
              'terrain':{'address':0x1000,'glyphs':256,'hex':payload[:2048].hex()},
              'font':{'address':0x3C00,'glyphs':128,'hex':payload[0x2C00:].hex()},'tables':{}}
    for symbol,length in [('ANDATA',192),('ARRCHR',144),('BACHAR',144),('SUCHAR',144),('DWIDTH',112),('SHTCOL',48),('COMPAR',8),('LANDSP',8),('HILLSP',8),('ANIMSP',8),('DECODE',4),('AMOUNT',8),
                          ('YVAL',15),('FALLY',15),('HILY',5),('HILLST',8),
                          ('TIME6',4),('TIM48',3),('TIM5',3),('DESCHR',6),
                          ('ICECHR',6),('PIPCHR',8),('COUNTR',3),('CNTCMP',3),
                          ('HOLECH',12),('HOLEYY',12),('EXSTAT',16),('EXYTBL',21),
                          ('COLTBL',8),('PRESCH',72),('PRATT',32),('OFDAT',6),
                          ('TITTOP',20),('CHSY',12),('CHSCHR',12),('CHSCOL',12),
                          ('DUCHIE',5),('DATTHE',18),('EDDAT',18),('HISTBL',112),
                          ('ARCHAR',8),('ARY',8),('JTCHAR',12),('JTARY',12),
                          ('BALLY',6),('KAMY',6),('BALLST',14),('SUSTAD',16),
                          ('RASVAL',5),('BTD',5),('RWD',5),('SKLTBL',4),('TIMDLY',3),
                          ('ARAB',3),('LV4TO6',6),('LV7TO9',4),('ABLOFS',3)]:
        addr=labels[symbol];raw=payload[addr-0x1000:addr-0x1000+length]
        assets['tables'][symbol]={'address':addr,'bytes':length,'hex':raw.hex()}
    (output/'asset-data.json').write_text(json.dumps(assets,indent=2)+'\n')
    atlas(output/'terrain-multicolor.svg','Terrain bank: character codes 000-255',payload[:2048],0x1000,'multicolor')
    atlas(output/'font-hires.svg','FRAK font: character codes 000-127, 1-bit view',payload[0x2C00:],0x3C00,'hires')
    atlas(output/'font-multicolor.svg','FRAK font: character codes 000-127, 2-bit view',payload[0x2C00:],0x3C00,'multicolor')
    print(json.dumps(data['counts'],indent=2))
    print(f'Wrote {output}')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir',type=Path,default=ROOT/'build')
    parser.add_argument('--output-dir',type=Path,default=ROOT/'docs/analysis')
    args=parser.parse_args()
    analyze(args.build_dir.resolve(),args.output_dir.resolve())
