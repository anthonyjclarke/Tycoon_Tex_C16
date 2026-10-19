# Source Navigation

## Build Inputs

The active assembly source is preserved under `Original Source Recovered/`. The build reads the 2026 disk sources first and supplies missing modules from the 1992 export. `TYCOONTE.SEQ` in the older folder is the original main assembly file; `INDEX` maps its `.LIB` names to the shortened PC filenames.

The modern ca65 source is generated as `build/tycoon.s`, with graphics sources in `build/terrain.s` and `build/actors.s`. These files retain module/line markers for tracing converted code back to the originals. Their corresponding listings, labels, maps, and debug files are generated alongside them.

---

## Preservation Target

There is no manually consolidated duplicate of the game in this folder. The same source-selection and conversion path is used by the direct build, Makefile, PlatformIO, tests, and VS Code tasks. Editing generated assembly has no effect on the next build.

See [Source Inventory](../docs/SOURCE_INVENTORY.md) for active dependencies, [Build and Run](../docs/BUILD_AND_RUN.md) for tooling, and [Source and Validation](../docs/SOURCE_AND_VALIDATION.md) for the original object-listing checks. Intentional source modifications require deliberate changes to the strict preservation checks.
