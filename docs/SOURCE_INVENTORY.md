# Source Inventory

## Preserved Collections

`Original Source Recovered/TycoonTex-C16.d64` is the main 2026 disk capture, with 56 sequential files in its live directory. Every disk file matches the extraction in `Original Source Recovered/2026 - TycoonText-C16/`, including the hashes in its `manifest.json`.

`Original Source Recovered/1992 - Tycoon Tex C16/` holds the older text exports, graphics binaries and development utilities. Its `INDEX` maps the original Commodore names to PC filenames. When the build reads those older text exports it normalizes uppercase and newlines in memory, so the saved bytes stay as they were.

The disk alone isn't a complete assembly set. The main program and several required routines are missing from its live directory, and the older collection fills the gaps. The selection is explicit and reproducible, not a guess from similar filenames.

---

## Active Assembly Sets

| Assembly root      | Modules | Fresh | Fallback |
| ------------------ | ------- | ----- | -------- |
| `TYCOON-TEX`       | 59      | 36    | 23       |
| `SET#1-CHAR/ASSEM` | 10      | 7     | 3        |
| `SET#2-CHAR/ASSEM` | 6       | 4     | 2        |

The first set assembles the main code and embedded data, and the second assembles the terrain graphics that go into the PRG. The third assembles an earlier actor-graphics variant for comparison, and its output never overwrites the standalone complete font.

That makes 75 active source modules, counting the three assembly roots. The fresh disk supplies 47 of them and the older collection the other 28. The remaining disk files are kept as comparison material, alternative data or unused source. `OBJ` and `CHAR#1` are hex listings used for comparison, not `.LIB` modules.

---

## Fallback Modules

Every filename in this table is in the 1992 folder. None of these modules is in the 2026 disk's live directory, so each is picked explicitly through `INDEX`.

| Commodore module   | Older PC file  |
| ------------------ | -------------- |
| `CDATA-JET/PLANE`  | `CDATAJET.SEQ` |
| `CDATA-NORM/PIPE`  | `CDATANOR.SEQ` |
| `CDATA-PIPE/BREAK` | `CDATAPIP.SEQ` |
| `COMPLETED-GAUGE`  | `COMPLETE.SEQ` |
| `FIRING/MEGACODE`  | `FIRINGME.SEQ` |
| `GLOP-ANIMATIONS`  | `GLOPANIM.SEQ` |
| `INTERRUPT-ALIENS` | `INTERRUP.SEQ` |
| `JET/PLANE-PRINT`  | `JETPLANE.SEQ` |
| `JO/KE SELECTION`  | `JOKESELE.SEQ` |
| `PIXEL-MOVE STUFF` | `PIXELMOV.SEQ` |
| `RASTER-ROUTINES`  | `RASTERRO.SEQ` |
| `SCORE-ROUTINES`   | `SCOREROU.SEQ` |
| `SCR/BUFFER-ON`    | `SCRBUFFE.SEQ` |
| `SCREEN-SETUP`     | `SCREENSE.SEQ` |
| `SET#1-CHAR/ASSEM` | `SET1CHAR.SEQ` |
| `SET#2-CHAR/ASSEM` | `SET2CHAR.SEQ` |
| `SET-SHEET`        | `SETSHEET.SEQ` |
| `SETUP`            | `SETUP.SEQ`    |
| `SINKER !`         | `SINKER.SEQ`   |
| `SOUND`            | `SOUND.SEQ`    |
| `STARTER`          | `STARTER.SEQ`  |
| `SUICIDE/OBJ-MOVE` | `SUICIDEO.SEQ` |
| `TABLES`           | `TABLES.SEQ`   |
| `TITLE-PAGE`       | `TITLEPAG.SEQ` |
| `TYCOON-TEX`       | `TYCOONTE.SEQ` |
| `UTILS`            | `UTILS.SEQ`    |
| `VARS`             | `VARS.SEQ`     |
| `WHOOPPEE-MESSAGE` | `WHOOPPEE.SEQ` |

---

## Graphics and Reference Inputs

`FRAK.BIN` in the 1992 folder is the complete game-ready upper font: a `$3C00` load header followed by 1,024 bytes. I've kept `CHARS.BIN` as a font revision that differs from it. `CHAR#1` and `CHAR#2` are MOS hex listings, and `SET#1-CHAR/ASSEM` and `SET#2-CHAR/ASSEM` are the original graphics assembly drivers.

`Original Artifacts/tycoon_tex.prg` is the packed running version, which I supplied separately. It's used for the emulator comparison and for launching the original game, and it contributes no bytes to the source rebuild. The gameplay JPG reference isn't a build input either.

`BACKUP-VARS` is an alternative variable arrangement, not the active `VARS` file. The build follows the main program's includes and never swaps in a backup version because of its name. The BASIC loaders, editor, assembler, DOS utility and other binaries in the older folder are kept, but the modern build doesn't use them.

---

## Generated Audit Trail

Each build writes `recovery-manifest.json`, which records the disk image hash, the older index hash, and for every available module its source, byte count and hash, whether it is a fallback and what normalization was used. The `used_modules` field lists the active source dependencies, and the `assets` field separates graphics that go into the PRG from comparison-only outputs.

The [included manifest](verification/source-manifest.json) is the one for the verified checkpoint. [Source and Validation](SOURCE_AND_VALIDATION.md) explains the byte comparisons, the graphics revision choices and the difference from the running game.
