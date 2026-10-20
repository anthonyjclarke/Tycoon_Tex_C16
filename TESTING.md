# Testing

## Regression Tests

```sh
python3 -m unittest discover -s test -p 'test_*.py' -v
```

The tests need Python 3.9+ and cc65. They build in a temporary directory, so the normal output and preserved inputs are left alone. All eight pass at the 20 October 2026 checkpoint.

They check the complete PRG's known hash and header, every byte recorded in `OBJ`, the exact reserved-buffer omission, fresh-source precedence and fallbacks, terrain and font provenance, unchanged input hashes and historical syntax conversion. They also check that missing, ambiguous or recursive includes, malformed hex records and cyclic disk chains are rejected.

The PRG baseline is a deliberate preservation check. If it fails after a code change I meant to make, the output no longer reproduces this source revision. Don't change the baseline until you've reviewed the byte differences.

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

Compare `build/tycoon-tex.prg`, `build/platformio/c16/tycoon-tex.prg` and `build/platformio/c16_debug/tycoon-tex.prg`. Both PlatformIO environments also generate symbols, a listing, a map and debug data. All three matched at the recorded checkpoint.

The GitHub Actions workflow installs cc65 and PlatformIO, runs the regression tests, builds both environments and checks their bytes against the direct build. The VICE checks need a GUI, so they run locally and aren't part of the workflow.

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

The script needs VICE with PNG screenshot support and a working graphical desktop. It starts from a fresh PAL C16 configuration with 16 KB RAM, turns audio off for automated testing, and applies a cycle limit and a process timeout. Each run writes monitor commands, logs, memory captures, screenshots and `vice-verification.json` to the chosen build directory.

The gameplay check stops just before the original menu `BIT JFIRE` test, sets the existing fire flag and resumes. It confirms the game reaches `LOOP` with `TITLE = 0` and `LIVES = 3`. The title and gameplay screenshots have been checked by eye.

The reference check runs the packed running PRG at its `$100D` decompressor entry and captures memory the first time execution reaches `$1800`. The report lists the 41 memory differences and separates initialized object bytes from font bytes. One scoring operand differs from the source version. [Source and Validation](docs/SOURCE_AND_VALIDATION.md) explains the result. I don't expect full equality with the reference, so the test doesn't require it.

---

## Verification Limits

The automated checks show that the source assembles, that the object listing matches, that the title renders and that gameplay starts. They say nothing about host-key mapping, joystick compatibility, audible sound, scoring over a whole game, level transitions, a full play-through or real hardware. I haven't tested any of those yet.

The keyboard controls and menu behavior come from reading the source. When I add manual-test results, they should stay separate from the scripted evidence, with the machine model, emulator version, input method and game revision recorded.

---

## Developer Analysis and Rule Probes

After building, regenerate the source and symbol index and the indexed graphics atlases with:

```sh
python3 scripts/analyze_codebase.py
```

The exporter checks that every byte of the main assembled region has an owner and records the PRG and image hashes. Its outputs under `docs/analysis/` feed the [codebase analysis](CODEBASE_ANALYSIS.md) and [porting guide](docs/PORTING_GUIDE.md). The static transfer list is not a complete execution graph.

For controlled arithmetic observations, generate the unpacked reference capture first, then run:

```sh
python3 scripts/verify_vice.py
python3 scripts/probe_gameplay_rules.py
```

Five observations cover source and reference scoring across 999, pressure borrowing, and the completion flag at and after a coarse-meter carry. The probe calls the original routines through a small workspace caller with interrupts disabled and decimal mode cleared, asserts the expected state and leaves the game instructions untouched. Reports and monitor logs go to `build/rule-probes/`, and the reviewed [included report](docs/analysis/rule-probes.json) records this checkpoint. These probes are narrow. They don't turn the gameplay-entry check into a full play-through or a concurrency test.
