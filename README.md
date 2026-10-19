# Tycoon Tex C16

Reassemble the surviving **Tycoon Tex** source for the Commodore 16 and Plus/4, using PlatformIO, VS Code, and the cc65 toolchain. Anthony Clarke programmed the game at Micro Projects for Gremlin Graphics in 1985.

![Tycoon Tex artwork](Original%20Artifacts/Tycoon%20Tex%20-%20With%20Text.jpg)

## Verified Build

The project assembles all **9,179 bytes recorded in the original object listing**, with zero differences. A further 24 bytes are reserved for the game's work buffer. The complete PRG is 12,290 bytes, loads at `$1000`, and starts at `$1800` (`SYS 6144`).

The rebuilt game renders its title and enters gameplay on a PAL C16 with 16 KB RAM in VICE. The supplied running version is a compressed, slightly different revision: one instruction operand differs after decompression. This project preserves the source and object-listing version; it does not claim a byte-identical reproduction of that running version. See [Source and Validation](docs/SOURCE_AND_VALIDATION.md) for the comparisons and limits.

![Restored title in VICE](docs/images/restored-title.png)

---

## Build and Run

Install Python 3.9 or later and the cc65 tools (`ca65` and `ld65`). Install VICE (`xplus4`) to run the game. On macOS with Homebrew:

```sh
brew install cc65 vice
./build.sh
python3 scripts/run_vice.py
```

The output is `build/tycoon-tex.prg`. The launcher loads at the saved address and jumps to `$1800` after the C16 finishes resetting. This PRG has no BASIC `RUN` stub.

With PlatformIO Core installed, or from the PlatformIO terminal in VS Code:

```sh
pio run -e c16
pio run -e c16 -t upload
```

The PlatformIO output is `build/platformio/c16/tycoon-tex.prg`. The upload target launches VICE. The `c16_debug` environment retains identical game bytes and emits the same labels, listing, map, and debug information for investigation. VS Code tasks provide direct builds, emulator launch, tests, and verification. See [Build and Run](docs/BUILD_AND_RUN.md).

The source's keyboard mapping is `Z` / `X` for left / right, `;` / `/` for up / down, and **Return** for fire and menu selection. Press `K` on the title screen to select keyboard control; `J` selects joystick control. The menu provides difficulty, lives, sound, play, and demo selections. Host keyboard mapping and physical joystick operation still need manual testing.

---

## Preserved Inputs

`Original Source Recovered/` contains the 2026 disk image and extraction, together with the more complete 1992 text export. The build prefers the fresh disk sources, verifies them against the extracted files, and fills missing modules from the 1992 collection using its original `INDEX` filename mapping. It assembles the terrain graphics from source and loads the surviving `FRAK.BIN` font asset. No executable code or graphics are copied from the supplied running PRG into the rebuild.

`Original Artifacts/` contains the running game, artwork, and a scanned scrapbook. The [Artifact Catalogue](docs/ARTIFACTS.md) includes the Tycoon Tex cassette inlay and identifies the relevant scrapbook pages.

All generated assembly, extracted working copies, and build reports go into `build/`. The original inputs are preserved byte for byte. [Source Inventory](docs/SOURCE_INVENTORY.md) lists the dependencies and fallback files.

---

## History and Recovery Background

Anthony recalls playing Moon Patrol in pubs and elsewhere at the time, and notes Tycoon Tex's resemblance to it. He no longer recalls the precise origin of the concept. The source credits the concept to **Matthew Clarke, Anthony Clarke, and Ian Stewart**, programming to **Micro Projects**, and publication to **Gremlin Graphics Ltd.** See [History and Credits](docs/HISTORY_AND_CREDITS.md).

The source-recovery background, original development setup, and recovery-tool acknowledgements are documented in the companion [Dorks Dilemma C16 repository](https://github.com/anthonyjclarke/Dorks_Dilemma_C16), particularly its [Development History](https://github.com/anthonyjclarke/Dorks_Dilemma_C16/blob/main/docs/DEVELOPMENT_HISTORY.md). This project uses that restoration's build approach without repeating its recovery narrative.

---

## Tests and Sharing

```sh
python3 -m unittest discover -s test -p 'test_*.py' -v
python3 scripts/verify_vice.py
```

Eight regression tests cover the output, object records, source selection, assets, preserved input bytes, include failures, syntax conversion, and corrupt records or disk chains. VICE verification checks title rendering, gameplay entry, and the decompressed reference. Manual keyboard testing, sound playback, level completion, and a full play-through remain pending. See [Testing](TESTING.md).

The repository is prepared for GitHub, with build outputs ignored and original PRGs and artifacts retained. [Sharing on GitHub](docs/SHARING_ON_GITHUB.md) explains the final publication steps. Historical notices remain in place; see [Rights and Preservation](RIGHTS.md).
