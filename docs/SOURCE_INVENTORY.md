# Source Inventory

## Preserved Collections

`Original Source Recovered/TycoonTex-C16.d64` is the primary 2026 disk capture. Its live directory contains 56 sequential files. Every disk file matches the supplied extraction in `Original Source Recovered/2026 - TycoonText-C16/`, including the hashes recorded in its `manifest.json`.

`Original Source Recovered/1992 - Tycoon Tex C16/` contains the older text exports, graphics binaries, and development utilities. Its `INDEX` maps original Commodore names to PC filenames. The build normalizes uppercase and newlines in memory when consuming those older text exports, leaving their saved bytes unchanged.

The disk is incomplete as an assembly set: the main program and several required routines are absent from its live directory. The older collection fills those gaps. Selection is explicit and reproducible, rather than based on approximate filename matching.

---

## Active Assembly Sets

| Assembly root      | Modules | Fresh | Fallback |
| ------------------ | ------- | ----- | -------- |
| `TYCOON-TEX`       | 59      | 36    | 23       |
| `SET#1-CHAR/ASSEM` | 10      | 7     | 3        |
| `SET#2-CHAR/ASSEM` | 6       | 4     | 2        |

The first set assembles the main code and embedded data. The second assembles the terrain graphics used in the PRG. The third assembles an earlier actor-graphics variant for comparison; its output does not overwrite the standalone complete font.

The total is 75 active source modules, including the three assembly roots. The fresh disk contributes 47 of those modules, with 28 supplied by the older collection. The remaining disk files are preserved comparison material, alternative data, or unused source. `OBJ` and `CHAR#1` are hex-listing comparison inputs rather than `.LIB` modules.

---

## Fallback Modules

All filenames in the following table are within the 1992 folder. These modules are absent from the 2026 disk's live directory and are explicitly selected through `INDEX`.

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

`FRAK.BIN` in the 1992 folder is the complete game-ready upper font: a `$3C00` load header followed by 1,024 bytes. `CHARS.BIN` is retained as a differing font revision. `CHAR#1` and `CHAR#2` are MOS hex listings; `SET#1-CHAR/ASSEM` and `SET#2-CHAR/ASSEM` are the original graphics assembly drivers.

The separately supplied `Original Artifacts/tycoon_tex.prg` is the packed running version. It is used for emulator comparison and original-game launch, and contributes no bytes to the source rebuild. The supplied JPG gameplay reference is likewise not a build input.

`BACKUP-VARS` is an alternative variable arrangement, not the active `VARS` file. The build follows the main program's includes and does not substitute backup versions based on their names. The BASIC loaders, editor, assembler, DOS utility, and other binaries in the older folder are preserved but are not invoked by the modern build.

---

## Generated Audit Trail

Each build writes `recovery-manifest.json`, recording the disk image hash, the older index hash, each available module's source, byte count and hash, whether it is a fallback, and the normalization used. Its `used_modules` field identifies active source dependencies; its `assets` field distinguishes graphics included in the PRG from comparison-only outputs.

The [included manifest](verification/source-manifest.json) records the verified checkpoint. [Source and Validation](SOURCE_AND_VALIDATION.md) explains byte comparisons, graphics revision choices, and the difference from the supplied running game.
