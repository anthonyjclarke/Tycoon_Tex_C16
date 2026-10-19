# Testing

## Regression Tests

```sh
python3 -m unittest discover -s test -p 'test_*.py' -v
```

The tests require Python 3.9+ and cc65. They build in a temporary directory, leaving the normal output and preserved inputs intact. Eight tests pass at the 20 October 2026 checkpoint.

The checks cover the complete PRG's known hash and header, every byte recorded in `OBJ`, the exact reserved-buffer omission, fresh-source precedence and fallbacks, terrain and font provenance, unchanged input hashes, historical syntax conversion, and rejection of missing/ambiguous/recursive includes, malformed hex records, and cyclic disk chains.

The PRG baseline is a deliberate preservation check. A failure after an intentional code change means the output no longer reproduces this source revision; it is not a reason to change the baseline without reviewing the byte differences.

---

## PlatformIO Agreement

```sh
./build.sh
pio run -e c16 -e c16_debug
```

The direct, release, and debug builds must produce the same SHA-256:

```text
09c9d0e3120e847f63c19b24560d46d08f15a48bfacb6956de01230e15cffbcd
```

Compare `build/tycoon-tex.prg`, `build/platformio/c16/tycoon-tex.prg`, and `build/platformio/c16_debug/tycoon-tex.prg`. Both PlatformIO environments generate symbols, a listing, a map, and debug data. All three paths passed at the recorded checkpoint.

The supplied GitHub Actions workflow installs cc65 and PlatformIO, runs the regression tests, builds both environments, and checks their bytes against the direct build. GUI-dependent VICE checks are performed locally and are not part of that workflow.

---

## VICE Verification

Build first, then run:

```sh
python3 scripts/verify_vice.py
```

For an alternate build directory:

```sh
python3 scripts/verify_vice.py --build-dir build/platformio/c16
```

The script requires VICE with PNG screenshot support and a working graphical desktop. It uses a fresh PAL C16 configuration with 16 KB RAM, disables audio for automated testing, and applies a cycle limit and process timeout. Each invocation generates monitor commands, logs, memory captures, screenshots, and `vice-verification.json` in the chosen build directory.

The gameplay check stops immediately before the original menu `BIT JFIRE` test, sets the existing fire flag, and resumes. It verifies entry into `LOOP` with `TITLE = 0` and `LIVES = 3`. The title and gameplay screenshots have been visually reviewed.

The reference check runs the supplied packed PRG at its `$100D` decompressor entry and captures memory when execution first reaches `$1800`. The report lists the 41 memory differences and separates initialized object bytes from font bytes. One scoring operand differs from the source version. [Source and Validation](docs/SOURCE_AND_VALIDATION.md) explains the result; full reference equality is not an expected test condition.

---

## Verification Limits

The automated checks establish source assembly, object-listing equality, title rendering, and gameplay entry. They do not establish manual host-key mapping, joystick compatibility, audible sound, correct scoring throughout a game, complete level transitions, a full play-through, or operation on physical hardware.

Source inspection documents the keyboard controls and menu behavior. Keep future manual-test observations distinct from the current scripted evidence, and record the machine model, emulator version, input method, and game revision when adding results.
