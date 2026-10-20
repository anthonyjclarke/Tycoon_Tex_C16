# Source Navigation

## Build Inputs

The active assembly source is kept under `Original Source Recovered/`. The build reads the 2026 disk sources first and fills any missing modules from the 1992 export. `TYCOONTE.SEQ` in the older folder is the original main assembly file; `INDEX` maps its `.LIB` names to the shortened PC filenames.

The modern ca65 source is generated as `build/tycoon.s`, with graphics sources in `build/terrain.s` and `build/actors.s`. These files keep module and line markers, so converted code can be traced back to the originals. Listings, labels, maps and debug files are generated next to them.

---

## Preservation Target

I haven't kept a hand-consolidated copy of the game in this folder. The direct build, Makefile, PlatformIO, tests and VS Code tasks all use the same source-selection and conversion path, and editing generated assembly changes nothing on the next build.

[Source Inventory](../docs/SOURCE_INVENTORY.md) lists the active dependencies, [Build and Run](../docs/BUILD_AND_RUN.md) covers the tooling and [Source and Validation](../docs/SOURCE_AND_VALIDATION.md) describes the original object-listing checks. If you change the source on purpose, you also have to change the strict preservation checks on purpose.
