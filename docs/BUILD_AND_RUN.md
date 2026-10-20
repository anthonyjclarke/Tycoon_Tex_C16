# Build and Run

## Requirements

Python 3.9 or later and cc65 (`ca65`, `ld65`) are all you need to build. VICE (`xplus4`) is for running the game and the emulator checks. The Python build uses only the standard library.

PlatformIO Core and VS Code are optional front ends. I've validated against PlatformIO Core 6.1.19, ca65/ld65 V2.18 and VICE 3.10. The PlatformIO native platform is pinned to `platformio/native@1.2.1`. It supplies the build framework, but the custom builder calls the 6502 assembler, not a host C/C++ compiler.

On macOS:

```sh
brew install cc65 vice
python3 -m pip install platformio==6.1.19
```

If `pio` only exists inside the VS Code PlatformIO extension, use that extension's terminal. The scripts look for cc65 and VICE on `PATH`, then in `/opt/homebrew/bin` and `/usr/local/bin`. On Linux, install your distribution's cc65 and VICE packages. On Windows, put the tools on `PATH` and use the Python commands below.

---

## Direct Build

```sh
python3 scripts/restore_c16.py
```

`./build.sh` and `make` call the same pipeline. You can also pick another output directory:

```sh
python3 scripts/restore_c16.py --build-dir build/custom
```

The build reads the disk image, checks the 2026 extraction and its hashes, maps the legacy filenames through `INDEX`, expands the original `.LIB` order and translates MOS assembler syntax into ca65 syntax. It assembles the original fixed-origin memory layout and checks every emitted object-listing byte before it reports success.

Terrain data is assembled on its own. The surviving `FRAK.BIN` provides the complete upper character set. Separate actor-definition sources are assembled for comparison, but they don't replace this game-ready font. The output doesn't depend on the packed running PRG, which is used only for optional comparison and launch.

### Output Files

The runnable file is `tycoon-tex.prg`. The main assembly is generated as `tycoon.s` with its listing in `tycoon.lst`, and the linker produces `tycoon.labels`, `tycoon.map` and `tycoon.dbg`. `recovered-code.bin` holds the `$1800–$3BF2` region, including the reserved work buffer.

`terrain.s` and `actors.s` are the independently assembled graphics sources. `recovery-manifest.json` records source selection, hashes, normalization, active dependencies and assets. `comparison.json` records the object-listing and character-listing checks. The `disk/` folder has generated, byte-preserving copies of the disk files.

---

## PlatformIO

```sh
pio run -e c16
pio run -e c16_debug
pio run -e c16 -t upload
pio run -e c16 -t clean
```

Release and debug builds use the same pipeline and produce identical program bytes. Both generate the listing and debug symbols, since those make good preservation evidence. Outputs are in `build/platformio/c16/` and `build/platformio/c16_debug/`.

The upload target opens a PAL C16 with 16 KB RAM in VICE. It doesn't send anything to physical hardware. There's no source-level VS Code debug adapter, so debug with the VICE monitor and the generated labels and listings.

### VS Code Tasks

The default build task calls PlatformIO. The other tasks cover the debug build, clean, emulator upload, the direct Python build, launching the original game, the regression tests and VICE verification. The original `.SEQ` files and the generated `.s` files use the `ca65` language mode from the recommended [ca65 extension](https://github.com/tlgkccampbell/code-ca65). Global save-time whitespace cleanup is turned off to protect the historical inputs.

If `pio` isn't found, run the task from a PlatformIO-enabled terminal or use the direct Python build task. If `ca65`, `ld65` or `xplus4` isn't found, install the tool and check its path.

---

## Running the Game

```sh
python3 scripts/run_vice.py
python3 scripts/run_vice.py build/platformio/c16/tycoon-tex.prg
python3 scripts/run_vice.py --original
```

The rebuilt PRG loads at `$1000` and enters at `$1800`. Its first 2 KB are terrain graphics, not BASIC text, so BASIC autostart won't work. The launcher waits for the reset to finish, then uses the monitor to load at the saved address and jump to the entry point.

The original I have is packed and has a BASIC `SYS 4109` stub. `--original` enters its decompressor at `$100D`, and from there it reaches the game at `$1800`. Neither launcher changes the original file.

### Controls

The original `KEY-SCAN` source gives `Z` / `X` for left / right, `;` / `/` for up / down, and Return for fire. `JO/KE SELECTION` maps `J` to joystick and `K` to keyboard on the title page. The menu sets lives, difficulty and sound, and picks play or demo. It starts on Play the Game, with joystick as the control mode.

I took these mappings from the source. The automated test sets the original fire-input flag directly, so it never exercises host keyboard mapping, sound playback or a physical joystick. The cassette instructions on scrapbook page 5 show how the packaging described the controls at the time.

---

## Cleaning and Development

`make clean` removes `build/` and `.pio/`, and leaves the original source, artwork and documentation alone. PlatformIO's clean only removes its own generated targets, so use `make clean` to clear everything generated.

The historical inputs are the source of truth for the build. Read `build/tycoon.s` if you want to see the expanded assembly, but editing generated files changes nothing on the next build. Any deliberate source change will fail the strict object-listing validation. Keep experiments on a separate branch, and revise the validation explicitly if you're producing a derivative version. The default target of this repository stays the surviving source version.
