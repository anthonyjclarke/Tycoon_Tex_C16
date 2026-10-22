#!/usr/bin/env python3
"""Assemble Tycoon Tex from preserved sources, recording every dependency."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from d64_image import D64Image
from source_converter import convert, flatten

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / 'Original Source Recovered'
IMAGE = INPUTS / '2026/TycoonTex-C16.d64'
OLDER = INPUTS / '1992'
EXTRACTED = INPUTS / '2026/TycoonText-C16'
REFERENCE = ROOT / 'Original Artifacts/tycoon_tex.prg'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def tool(name):
    found = shutil.which(name)
    if found:
        return found
    for directory in ('/opt/homebrew/bin', '/usr/local/bin'):
        candidate = Path(directory) / name
        if candidate.is_file():
            return str(candidate)
    raise FileNotFoundError(f'{name} not found; install the cc65/VICE tools described in README.md')


def prepare_sources(build):
    """Prefer fresh disk bytes; INDEX maps legacy PC names back to CBM names."""
    disk = D64Image(IMAGE).files()
    sources, provenance = {}, []
    raw = build / 'disk'
    raw.mkdir(parents=True, exist_ok=True)
    extraction = json.loads((EXTRACTED / 'manifest.json').read_text())
    extracted = {bytes.fromhex(f['petscii_name_hex']).rstrip(b'\xa0').decode('ascii'): f
                 for f in extraction['files']}
    for number, file in enumerate(disk, 1):
        data = file.data
        record = extracted.get(file.name)
        if record is None or data != (EXTRACTED / record['output']).read_bytes():
            raise ValueError(f'Disk and preserved 2026 extraction differ: {file.name}')
        if digest(data) != record['sha256']:
            raise ValueError(f'Extraction hash mismatch: {file.name}')
        (raw / f'{number:03d}_{file.name.replace("/", "~2F")}.{file.kind.lower()}').write_bytes(data)
        provenance.append({'name': file.name, 'source': str(IMAGE.relative_to(ROOT)),
                           'sha256': digest(data), 'bytes': len(data), 'closed': file.closed,
                           'extracted_copy': record['output'], 'fallback': False})
        if file.kind == 'SEQ':
            sources[file.name] = data.decode('ascii').splitlines()
    index = (OLDER / 'INDEX').read_text()
    for name, stem in re.findall(r'^\d+\s+"([^"]+)"\s+SEQ\s+(\S+)\s+TXT', index, re.MULTILINE):
        if name in sources:
            continue
        path = OLDER / (stem + '.SEQ')
        if not path.is_file():
            raise ValueError(f'INDEX refers to missing fallback: {path.name}')
        data = path.read_bytes()
        sources[name] = data.decode('ascii').upper().splitlines()
        provenance.append({'name': name, 'source': str(path.relative_to(ROOT)),
                           'sha256': digest(data), 'bytes': len(data), 'fallback': True,
                           'normalization': 'upper case; universal newlines'})
    manifest = {'image': str(IMAGE.relative_to(ROOT)), 'image_sha256': digest(IMAGE.read_bytes()),
                'index_sha256': digest((OLDER / 'INDEX').read_bytes()), 'files': provenance}
    (build / 'recovery-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return sources, manifest


def mos_hex(lines):
    """Decode MOS Technology hex records, validating checksums and terminator."""
    memory, records, terminal = {}, 0, False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if terminal:
            raise ValueError('Data after MOS hex terminator')
        if not line.startswith(';'):
            raise ValueError(f'Invalid MOS hex record: {line}')
        raw = bytes.fromhex(line[1:])
        if len(raw) < 5:
            raise ValueError('MOS hex record is too short')
        count = raw[0]
        if len(raw) != count + 5 or sum(raw[:-2]) != int.from_bytes(raw[-2:], 'big'):
            raise ValueError('MOS hex length/checksum mismatch')
        address = int.from_bytes(raw[1:3], 'big')
        if not count:
            if address != records:
                raise ValueError('MOS hex record count mismatch')
            terminal = True
            continue
        records += 1
        for offset, byte in enumerate(raw[3:-2]):
            if address + offset in memory:
                raise ValueError('Overlapping MOS hex records')
            memory[address + offset] = byte
    if not terminal:
        raise ValueError('Missing MOS hex terminator')
    return memory


def assemble(build, sources, name, stem, regions):
    """Use one linker region for each original fixed-origin block."""
    assembly = build / (stem + '.s')
    lines = flatten(sources, name)
    assembly.write_text(convert(lines))
    if stem == 'tycoon':
        config = ROOT / 'config/c16.cfg'
        binary = build / 'recovered-code.bin'
    else:
        config = build / (stem + '.cfg')
        binary = build / (stem + '.bin')
        memories, segments = [], []
        for address, size, output in regions:
            seg = f'AT_{address:04X}'
            filename = (build / output).as_posix() if output else ''
            memories.append(f'    M_{address:04X}: start = ${address:04X}, size = ${size:04X}, file = "{filename}";')
            kind = 'zp' if address < 0x100 else ('ro' if output else 'bss')
            segments.append(f'    {seg}: load = M_{address:04X}, type = {kind};')
        config.write_text('MEMORY {\n' + '\n'.join(memories) + '\n}\nSEGMENTS {\n' + '\n'.join(segments) + '\n}\n')
    obj = build / (stem + '.o')
    subprocess.run([tool('ca65'), '-g', '-l', str(build / (stem + '.lst')),
                    '-o', str(obj), str(assembly)], check=True)
    subprocess.run([tool('ld65'), '-C', str(config), '-o', str(binary),
                    '-m', str(build / (stem + '.map')),
                    '-Ln', str(build / (stem + '.labels')), '--dbgfile', str(build / (stem + '.dbg')),
                    str(obj)], check=True)
    return list(dict.fromkeys(name for name, _, _ in lines))


def build_game(build):
    build = build.resolve()
    build.mkdir(parents=True, exist_ok=True)
    sources, manifest = prepare_sources(build)
    used = assemble(build, sources, 'TYCOON-TEX', 'tycoon', [
        (2, 0xFE, None), (0x400, 0x100, None), (0x560, 0x278, None),
        (0x1800, 0x2400, 'recovered-code.bin')])
    code = (build / 'recovered-code.bin').read_bytes()
    terrain_origins = [0x1000, 0x1140, 0x1280, 0x13C0, 0x1500, 0x1640, 0x16B0, 0x1750, 0x17A0]
    actor_origins = [0x3E00, 0x3EE8, 0x3F18, 0x3F98, 0x3FA8]
    memory = bytearray(0x3000)
    assets = []
    for name, stem, origins, limit in [
            ('SET#1-CHAR/ASSEM', 'terrain', terrain_origins, 0x1800),
            ('SET#2-CHAR/ASSEM', 'actors', actor_origins, 0x4000)]:
        regions = [(a, b-a, f'{stem}-{a:04x}.bin') for a, b in zip(origins, origins[1:] + [limit])]
        used += assemble(build, sources, name, stem, regions)
        for address, size, output in regions:
            data = (build / output).read_bytes()
            if stem == 'terrain':
                memory[address-0x1000:address-0x1000+len(data)] = data
            assets.append({'address': f'${address:04X}', 'bytes': len(data), 'source': name,
                           'included_in_prg': stem == 'terrain'})
    charset_path = OLDER / 'FRAK.BIN'
    charset = charset_path.read_bytes()
    if charset[:2] != b'\x00\x3c' or len(charset) != 1026:
        raise ValueError('Unexpected FRAK.BIN layout')
    # The complete FRAK font is the surviving game-ready asset. SET#2 and
    # CHAR#2 are earlier editable actor variants, assembled for comparison.
    memory[0x2C00:0x3000] = charset[2:]
    memory[0x800:0x800+len(code)] = code
    output = build / 'tycoon-tex.prg'
    output.write_bytes(b'\x00\x10' + memory)
    obj = mos_hex(sources['OBJ'])
    differences = [a for a, b in obj.items() if not 0x1800 <= a < 0x1800+len(code) or code[a-0x1800] != b]
    char_reports = {}
    for name in ('CHAR#1', 'CHAR#2'):
        asset = mos_hex(sources[name])
        changes = [a for a, b in asset.items() if memory[a-0x1000] != b]
        char_reports[name] = {'bytes': len(asset), 'differences': len(changes),
                              'first_differences': [f'${a:04X}' for a in changes[:20]]}
    manifest['used_modules'] = list(dict.fromkeys(used))
    manifest['assets'] = [{'source': str(charset_path.relative_to(ROOT)), 'sha256': digest(charset),
                           'address': '$3C00', 'bytes': 1024}] + assets
    (build / 'recovery-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    report = {'load_address': '$1000', 'entry_address': '$1800', 'code_bytes': len(code),
              'output_bytes': output.stat().st_size, 'sha256': digest(output.read_bytes()),
              'object_listing_bytes': len(obj), 'reserved_code_bytes': len(code) - len(obj), 'object_listing_differences': len(differences),
              'first_object_differences': [f'${a:04X}' for a in differences[:30]],
              'character_listing_comparison': char_reports,
              'packed_reference_sha256': digest(REFERENCE.read_bytes()) if REFERENCE.exists() else None,
              'packed_reference_comparison': 'run scripts/verify_vice.py for runtime comparison'}
    (build / 'comparison.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    if differences or min(obj) != 0x1800 or max(obj) + 1 != 0x1800 + len(code):
        raise ValueError('Assembled code differs from original OBJ listing')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, default=ROOT / 'build')
    args = parser.parse_args()
    build_game(args.build_dir)
