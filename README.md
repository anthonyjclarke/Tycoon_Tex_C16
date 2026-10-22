# Tycoon Tex C16

![Release v1.0.0](docs/images/badges/release.svg)
![Platform Commodore 16 / Plus/4](docs/images/badges/platform.svg)
![Byte match 9,179 of 9,179](docs/images/badges/byte-match.svg)
![Toolchain cc65](docs/images/badges/toolchain.svg)
![PlatformIO 6.1](docs/images/badges/platformio.svg)
![Emulator VICE 3.10](docs/images/badges/emulator.svg)
![Status preservation](docs/images/badges/status.svg)

This project reassembles the surviving **Tycoon Tex** source for the Commodore 16 and Plus/4 using PlatformIO, VS Code and the cc65 toolchain. I programmed the game at Micro Projects for Gremlin Graphics in 1985.

Open the [complete HTML handbook](docs/TYCOON_TEX.html) for the history, artwork, build guides, validation, code analysis, graphics and reference in one offline document. It's generated from the Markdown files, which stay the source of truth. Run `make docs-html` after editing the docs, or `make docs` to refresh the build and analysis as well. [Maintaining the HTML Documentation](docs/HTML_DOCUMENTATION.md) has the details.

![Tycoon Tex artwork](Original%20Artifacts/Tycoon%20Tex%20-%20With%20Text.jpg)

## Verified Build

The build matches all **9,179 bytes recorded in the original object listing**, with zero differences. Another 24 bytes are reserved for the game's work buffer. The complete PRG is 12,290 bytes, loads at `$1000` and starts at `$1800` (`SYS 6144`).

In VICE, on a PAL C16 with 16 KB RAM, the rebuilt game draws its title and gets into gameplay. The running version I have is a compressed, slightly different revision: after decompression, one instruction operand differs. I've rebuilt the source and object-listing version, so I can't claim a byte-identical copy of the running one. [Source and Validation](docs/SOURCE_AND_VALIDATION.md) has the comparisons and limits.

![Restored title in VICE](docs/images/restored-title.png)

---

## Build and Run

You need Python 3.9 or later and the cc65 tools (`ca65` and `ld65`), plus VICE (`xplus4`) to run the game. On macOS with Homebrew:

```sh
brew install cc65 vice
./build.sh
python3 scripts/run_vice.py
```

The output is `build/tycoon-tex.prg`. After the C16 finishes resetting, the launcher loads it at the saved address and jumps to `$1800`. The PRG has no BASIC `RUN` stub.

With PlatformIO Core installed, or from the PlatformIO terminal in VS Code:

```sh
pio run -e c16
pio run -e c16 -t upload
```

PlatformIO writes to `build/platformio/c16/tycoon-tex.prg`, and the upload target launches VICE. The `c16_debug` environment produces identical game bytes, along with labels, a listing, a map and debug information for digging into problems. VS Code tasks cover direct builds, launching the emulator, tests and verification. More in [Build and Run](docs/BUILD_AND_RUN.md).

In the source, the keyboard is `Z` / `X` for left / right, `;` / `/` for up / down, and **Return** for fire and menu selection. Press `K` on the title screen for keyboard control or `J` for joystick. The menu covers difficulty, lives, sound, play and demo. I still need to test the host keyboard mapping and a physical joystick by hand.

---

## Preserved Inputs

`Original Source Recovered/` holds the 2026 disk image and its extraction, along with the more complete 1992 text export. The build uses the fresh disk sources first and checks them against the extracted files. Anything missing comes from the 1992 collection, through its original `INDEX` filename mapping. Terrain graphics are assembled from source, and the font is the surviving `FRAK.BIN`. Nothing executable or graphical is copied from the running PRG into the rebuild.

`Original Artifacts/` has the running game, the artwork and a scanned scrapbook. The [Artifact Catalogue](docs/ARTIFACTS.md) covers the cassette inlay and points to the relevant scrapbook pages.

Generated assembly, extracted working copies and build reports all go into `build/`, and the original inputs stay byte for byte as they were. The [Source Inventory](docs/SOURCE_INVENTORY.md) lists the dependencies and fallback files.

---

## History and Recovery Background

I remember playing Moon Patrol in pubs and elsewhere at the time, and Tycoon Tex looks a lot like it, but I can't recall exactly where the concept came from. The source credits the concept to **Matthew Clarke, Anthony Clarke, and Ian Stewart**, the programming to **Micro Projects** and the publication to **Gremlin Graphics Ltd.** See [History and Credits](docs/HISTORY_AND_CREDITS.md).

The recovery story, my original development setup and the recovery-tool acknowledgements are in my companion [Dorks Dilemma C16 repository](https://github.com/anthonyjclarke/Dorks_Dilemma_C16), especially its [Development History](https://github.com/anthonyjclarke/Dorks_Dilemma_C16/blob/main/docs/DEVELOPMENT_HISTORY.md). This project reuses that restoration's build approach, so I haven't repeated the story here.

---

## Learning, Modification, and Ports

[Codebase Analysis](CODEBASE_ANALYSIS.md) walks through the game states, raster scheduling, player and hazard rules, collision model, graphics, audio, scoring and the differences between revisions. The [Porting Guide](docs/PORTING_GUIDE.md) keeps the original behavior apart from the architecture I'd propose for new platforms. A [generated code reference](docs/analysis/CODE_REFERENCE.md), [asset data](docs/analysis/asset-data.json) and indexed graphics atlases help with finding your way around the source.

---

## Tests and Sharing

```sh
python3 -m unittest discover -s test -p 'test_*.py' -v
python3 scripts/verify_vice.py
```

Eight regression tests cover the output, object records, source selection, assets, preserved input bytes, include failures, syntax conversion, and corrupt records or disk chains. The VICE check covers title rendering, gameplay entry and the decompressed reference. I still haven't tested the keyboard by hand, listened to the sound, finished a level or played all the way through. See [Testing](TESTING.md).

The repository is set up for GitHub: build outputs are ignored and the original PRGs and artifacts are kept. [Sharing on GitHub](docs/SHARING_ON_GITHUB.md) has the final publication steps. The historical notices are all still in place; see [Rights and Preservation](RIGHTS.md).
