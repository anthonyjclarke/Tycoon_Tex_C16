# Build and Run

## Requirements

Python 3.9 or later and cc65 (`ca65`, `ld65`) are sufficient to build. VICE (`xplus4`) is needed to run the game or perform emulator verification. The Python build uses only the standard library.

PlatformIO Core and VS Code are optional front ends. The validated local versions are PlatformIO Core 6.1.19, ca65/ld65 V2.18 tool binaries, and VICE 3.10. The PlatformIO native platform is pinned to `platformio/native@1.2.1`; it supplies the build framework, while the custom builder invokes the 6502 assembler rather than a host C/C++ compiler.

On macOS:

```sh
brew install cc65 vice
python3 -m pip install platformio==6.1.19
```

If `pio` is available only through the VS Code PlatformIO extension, use its terminal. The scripts search `PATH`, `/opt/homebrew/bin`, and `/usr/local/bin` for cc65 and VICE. On Linux, install the distribution's cc65 and VICE packages. On Windows, place the tools on `PATH` and use the Python commands below.

---

## Direct Build

```sh
python3 scripts/restore_c16.py
```

`./build.sh` and `make` call the same pipeline. An alternate output directory is supported:

```sh
python3 scripts/restore_c16.py --build-dir build/custom
```

The build reads the disk image, checks the 2026 extraction and hashes, maps legacy filenames through `INDEX`, expands the original `.LIB` order, and translates MOS assembler syntax into ca65 syntax. It assembles the original fixed-origin memory layout and checks every emitted object-listing byte before reporting success.

Terrain data is assembled independently. The surviving `FRAK.BIN` supplies the complete upper character set. Separate actor-definition sources are assembled for comparison, but do not replace this game-ready font. The output does not depend on the packed running PRG; that file is used only for optional comparison and launch.

### Output Files

The runnable file is `tycoon-tex.prg`. The generated main assembly is `tycoon.s`, its listing is `tycoon.lst`, and the linker emits `tycoon.labels`, `tycoon.map`, and `tycoon.dbg`. `recovered-code.bin` contains the `$1800–$3BF2` region, including the reserved work buffer.

`terrain.s` and `actors.s` expose the independently assembled graphics sources. `recovery-manifest.json` records source selection, hashes, normalization, active dependencies, and assets. `comparison.json` records the object-listing and character-listing checks. The `disk/` folder contains generated, byte-preserving copies of the disk files.

---

## PlatformIO

```sh
pio run -e c16
pio run -e c16_debug
pio run -e c16 -t upload
pio run -e c16 -t clean
```

Release and debug builds use the same pipeline and retain identical program bytes. Both generate the listing and debug symbols because those files are useful preservation evidence. Their outputs are in `build/platformio/c16/` and `build/platformio/c16_debug/`.

The upload target opens a PAL C16 with 16 KB RAM in VICE. It does not transfer a program to physical hardware. The project does not include a source-level VS Code debug adapter; use the VICE monitor and generated labels/listings for debugging.

### VS Code Tasks

The default build task calls PlatformIO. Other tasks offer the debug build, clean, emulator upload, direct Python build, original-game launch, regression tests, and VICE verification. The original `.SEQ` files and generated `.s` files use the `ca65` language mode supplied by the recommended [ca65 extension](https://github.com/tlgkccampbell/code-ca65). Global save-time whitespace cleanup is disabled to protect historical inputs.

If `pio` is not found, run the task from a PlatformIO-enabled terminal or use the direct Python build task. If `ca65`, `ld65`, or `xplus4` is not found, install the relevant tools and check their paths.

---

## Running the Game

```sh
python3 scripts/run_vice.py
python3 scripts/run_vice.py build/platformio/c16/tycoon-tex.prg
python3 scripts/run_vice.py --original
```

The rebuilt PRG loads at `$1000` and enters at `$1800`. Its first 2 KB contain terrain graphics, not BASIC text; BASIC autostart is unsuitable. The launcher waits for reset to complete and uses the monitor to load at the saved address and jump to the entry point.

The supplied original is packed and has a BASIC `SYS 4109` stub. `--original` enters its decompressor at `$100D`; it then reaches the game at `$1800`. Neither launcher changes the original file.

### Controls

The original `KEY-SCAN` source documents `Z` / `X` for left / right, `;` / `/` for up / down, and Return for fire. `JO/KE SELECTION` maps `J` to joystick and `K` to keyboard on the title page. The menu controls lives, difficulty, sound, play, and demo selection. The initial selection is Play the Game; the initial control mode is joystick.

These mappings are documented from source. The automated test supplies the original fire-input flag and does not exercise host keyboard mapping, sound playback, or a physical joystick. See the scanned cassette instructions on scrapbook page 5 for the contemporary packaging description.

---

## Cleaning and Development

`make clean` removes `build/` and `.pio/`. Original source, artwork, and documentation remain intact. PlatformIO clean removes its generated targets; use `make clean` for all generated material.

The historical inputs are the build's source of truth. Inspect `build/tycoon.s` to read the expanded assembly; editing generated files has no effect on the next build. Intentional source changes will fail strict object-listing validation. Keep experimental changes in a separate branch and explicitly revise validation if producing a derivative version. This repository's default target remains the surviving source version.
