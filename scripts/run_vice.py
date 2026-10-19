#!/usr/bin/env python3
"""Load a saved-address PRG and enter the game on a 16 KB PAL C16."""

import argparse
import subprocess
from pathlib import Path

from restore_c16 import ROOT, REFERENCE, tool


def launch(program, entry=0x1800):
    program = program.resolve(strict=True)
    build = ROOT / 'build/vice'
    build.mkdir(parents=True, exist_ok=True)
    commands = build / 'start.mon'
    commands.write_text(f'load "{program.as_posix()}" 0\ng {entry:x}\n')
    with (build / 'console.log').open('w') as log:
        process = subprocess.Popen([
            tool('xplus4'), '-default', '+saveres', '-model', 'c16pal', '-ramsize', '16',
            '-initbreak', 'ready', '-moncommands', str(commands),
            '-logfile', str(build / 'vice.log'),
        ], cwd=str(ROOT), stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    print(f'VICE started (PID {process.pid}): {program}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('program', nargs='?', type=Path, default=ROOT / 'build/tycoon-tex.prg')
    parser.add_argument('--original', action='store_true', help='Run the supplied packed PRG')
    parser.add_argument('--entry', type=lambda s: int(s, 0), default=0x1800)
    args = parser.parse_args()
    launch(REFERENCE if args.original else args.program, 0x100D if args.original else args.entry)
