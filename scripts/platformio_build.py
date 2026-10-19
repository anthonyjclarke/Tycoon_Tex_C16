"""PlatformIO adapter for the same audited source build as build.sh."""

import subprocess
import sys
from pathlib import Path

from SCons.Script import Default, DefaultEnvironment

env = DefaultEnvironment()
root = Path(env.subst('$PROJECT_DIR'))
build = Path(env.subst('$BUILD_DIR'))
dependencies = list((root / 'scripts').glob('*.py')) + list((root / 'config').glob('*'))
dependencies += [p for p in (root / 'Original Source Recovered').rglob('*')
                 if p.is_file() and p.suffix.lower() not in ('.jpg', '.log') and p.name != '.DS_Store']


def assemble(source, target, env):
    subprocess.run([sys.executable, str(root / 'scripts/restore_c16.py'),
                    '--build-dir', str(build)], check=True, cwd=str(root))


def launch(source, target, env):
    subprocess.run([sys.executable, str(root / 'scripts/run_vice.py'),
                    str(build / 'tycoon-tex.prg')], check=True, cwd=str(root))


program = env.Command(str(build / 'tycoon-tex.prg'), [str(p) for p in dependencies],
                      env.VerboseAction(assemble, 'Assembling and checking original Tycoon Tex source'))
env.Replace(PROGNAME='tycoon-tex', PROGPATH=str(build / 'tycoon-tex.prg'))
env.Alias('buildprog', program)
env.AddCustomTarget('upload', program, env.VerboseAction(launch, 'Launching Tycoon Tex in VICE'),
                    title='Run in VICE', description='Run on an emulated 16 KB PAL C16')
Default(program)
