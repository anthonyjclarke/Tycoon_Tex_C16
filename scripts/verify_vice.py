#!/usr/bin/env python3
"""Check title, gameplay entry, and the supplied packed game in PAL C16 VICE."""

import argparse
import json
import re
import subprocess
from pathlib import Path

from restore_c16 import ROOT, REFERENCE, digest, mos_hex, prepare_sources, tool


def run_monitor(build, stem, commands):
    commands_file = build / (stem + '.mon')
    commands_file.write_text(commands)
    log = build / (stem + '-monitor.log')
    log.unlink(missing_ok=True)
    result = subprocess.run([
        tool('xplus4'), '-default', '+saveres', '-model', 'c16pal', '-ramsize', '16',
        '+sound', '-initbreak', 'ready', '-moncommands', str(commands_file),
        '-logfile', str(build / (stem + '-vice.log')), '-monlog', '-monlogname', str(log),
        '-warp', '-limitcycles', '100000000',
    ], cwd=str(ROOT), capture_output=True, timeout=45)
    (build / (stem + '-console.log')).write_bytes(result.stdout + result.stderr)
    result.check_returncode()
    return log.read_text()


def verify(build):
    build = build.resolve()
    labels = {name: int(address, 16) for address, name in re.findall(
        r'^al ([0-9A-Fa-f]+) \.(\w+)$', (build / 'tycoon.labels').read_text(), re.MULTILINE)}
    for name in ('restored-title.png', 'restored-gameplay.png', 'gameplay-memory.bin',
                 'reference-memory.bin'):
        (build / name).unlink(missing_ok=True)
    code = (build / 'recovered-code.bin').read_bytes()
    check = labels['FUNKIT']
    if code[check-0x1800:check-0x1800+3] != bytes((0x24, labels['JFIRE'], 0x10)):
        raise ValueError('Cannot identify the original menu fire test')
    log = run_monitor(build, 'gameplay',
        f'load "{build / "tycoon-tex.prg"}" 0\n'
        f'break {check:x}\ng 1800\n'
        f'screenshot "{build / "restored-title.png"}" 2\n'
        f'> {labels["JFIRE"]:x} 80\ndelete 1\n'
        f'break {labels["LOOP"]:x}\nx\n'
        f'> {labels["JFIRE"]:x} 00\n'
        f'screenshot "{build / "restored-gameplay.png"}" 2\n'
        f'bsave "{build / "gameplay-memory.bin"}" 0 0000 3fff\nquit\n')
    memory = (build / 'gameplay-memory.bin').read_bytes()
    if len(memory) != 0x4000 or memory[labels['TITLE']] != 0 or memory[labels['LIVES']] != 3:
        raise ValueError('Gameplay state is not TITLE=0 / LIVES=3')
    if f'C:${labels["LOOP"]:04x}'.lower() not in log.lower():
        raise ValueError('VICE did not reach the main game loop')
    for name in ('restored-title.png', 'restored-gameplay.png'):
        if not (build / name).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError(f'Missing VICE screenshot: {name}')
    # The supplied BASIC stub contains SYS 4109. Stop at the game's entry
    # before initialization so comparison excludes mutable gameplay state.
    log = run_monitor(build, 'reference',
        f'load "{REFERENCE}" 0\nbreak 1800\ng 100d\n'
        f'bsave "{build / "reference-memory.bin"}" 0 1000 3fff\nquit\n')
    if 'C:$1800'.lower() not in log.lower():
        raise ValueError('Packed reference did not reach $1800')
    reference = (build / 'reference-memory.bin').read_bytes()
    restored = (build / 'tycoon-tex.prg').read_bytes()[2:]
    if len(reference) != len(restored):
        raise ValueError('Unexpected decompressed reference size')
    sources, _ = prepare_sources(build / 'reference-inputs')
    obj = mos_hex(sources['OBJ'])
    differences = [a for a in obj if restored[a-0x1000] != reference[a-0x1000]]
    font_differences = [a for a in range(0x3C00, 0x4000)
                        if restored[a-0x1000] != reference[a-0x1000]]
    all_differences = [a+0x1000 for a, (x, y) in enumerate(zip(restored, reference)) if x != y]
    report = {
        'emulator': 'VICE xplus4', 'model': 'c16pal', 'ram_kib': 16,
        'title_rendered': True, 'gameplay_loop_reached': True, 'title_flag': 0, 'lives': 3,
        'input': 'scripted JFIRE flag at original menu BIT test; no instruction patches',
        'manual_keyboard_sound_and_full_playthrough': 'not verified',
        'reference_sha256': digest(REFERENCE.read_bytes()),
        'reference_compared_at': '$1800 before first game instruction',
        'initialized_code_differences': [
            {'address': f'${a:04X}', 'source': f'${restored[a-0x1000]:02X}',
             'reference': f'${reference[a-0x1000]:02X}'} for a in differences],
        'font_differences': [f'${a:04X}' for a in font_differences],
        'total_memory_differences': len(all_differences),
        'all_memory_differences': [f'${a:04X}' for a in all_differences],
        'byte_identical_to_running_version': not all_differences,
    }
    (build / 'vice-verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, default=ROOT / 'build')
    verify(parser.parse_args().build_dir)
