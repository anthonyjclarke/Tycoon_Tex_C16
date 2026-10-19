# Source and Validation

## Result – 20 October 2026

The rebuilt PRG contains 12,288 memory bytes plus a two-byte `$1000` load header. It starts execution at `$1800` on a 16 KB PAL C16.

| Measurement                 | Result                    |
| --------------------------- | ------------------------- |
| Complete PRG                | 12,290 bytes              |
| Main source region          | 9,203 bytes               |
| Object-listing bytes        | 9,179 bytes               |
| Reserved work buffer        | 24 bytes                  |
| Object-listing differences  | 0                         |
| Terrain source/listing diff | 0                         |
| Regression tests            | 8 passing                 |
| Emulator                    | VICE 3.10, PAL C16, 16 KB |

The verified output SHA-256 is:

```text
09c9d0e3120e847f63c19b24560d46d08f15a48bfacb6956de01230e15cffbcd
```

The supplied packed running PRG has SHA-256:

```text
87b99fcdbb0de146b2d373ec11ef7f759175544c37659e47aaa880d3693b253f
```

The included [build comparison](verification/build-comparison.json), [VICE report](verification/vice-verification.json), and [source manifest](verification/source-manifest.json) preserve this checkpoint's evidence. The [tool checks](verification/tool-checks.json) record build agreement and the independent disk extraction check. New builds generate fresh reports in their output directory.

---

## Source Selection and Assembly

The primary input is `Original Source Recovered/TycoonTex-C16.d64`. Its 56 live files match the supplied 2026 extraction byte for byte and pass the extraction manifest's hashes. Missing modules are supplied by the 1992 export. Its `INDEX` restores the relationship between Commodore filenames and shortened PC filenames, including names containing `/`, `#`, and spaces.

The main source is the older `TYCOONTE.SEQ`, mapped to `TYCOON-TEX`. Its original `.LIB` order is retained. The main assembly expands 59 modules: 36 from the fresh disk and 23 fallbacks. The build restores uppercase source representation and universal newlines for the older text exports without rewriting them. Includes must resolve uniquely; missing, ambiguous, or recursive references fail the build.

VICE's separate `c1541` disk utility independently extracted `OBJ`; its output matched the 2026 extraction byte for byte.

The syntax converter retains instructions after labels, equates, self-modifying operands, literal text, and the two original macros. ca65 and ld65 assemble and link the fixed addresses. `OBJ` is a MOS Technology hex-format object listing, not an assembly module. Its record lengths, checksums, and terminal record count are checked before comparison. Every one of its 9,179 bytes matches the reassembly. The 24-byte `SCRBUF` reservation at `$25E1–$25F8` has no emitted records in `OBJ`; the linker initializes that output space to zero.

### Memory Layout

| Address range  | Content                       |
| -------------- | ----------------------------- |
| `$0002–$00FF`  | Zero-page variable region     |
| `$0400–$04A7`  | Saved Tex character workspace |
| `$0560` onward | Double-width title workspace  |
| `$1000–$17FF`  | Terrain and pipe graphics     |
| `$1800–$3BF2`  | Main assembled code and data  |
| `$3BF3–$3BFF`  | Zero-filled output gap        |
| `$3C00–$3FFF`  | Supplied complete font asset  |

The first three regions are workspace, not PRG payload. The main linker configuration is `config/c16.cfg`; generated graphics configurations retain the original individual origins.

---

## Graphics Provenance

`SET#1-CHAR/ASSEM` assembles nine terrain blocks, using the fresh disk first and older modules where necessary. All 2,048 bytes match the original `CHAR#1` hex listing. The complete font comes from the surviving 1,026-byte `FRAK.BIN` file, including its `$3C00` load header. Its 1,024 payload bytes differ from the supplied running version's decompressed upper font at only `$3FFF`.

The similarly sized `CHARS.BIN` is a different graphics revision: 436 payload bytes differ from `FRAK.BIN`. It is preserved but is not the chosen font input. The earlier actor definitions in `SET#2-CHAR/ASSEM` and `CHAR#2` also differ from the game-ready font. They are retained and assembled as comparison material; they do not overwrite `FRAK.BIN` in the playable output. The old `CHAR#2` listing differs at 106 of its 263 recorded addresses from that final font.

All graphics dependencies are surviving standalone assets or assembled source. The rebuild never copies executable or graphics bytes from `Original Artifacts/tycoon_tex.prg`.

---

## Comparison with the Running Version

The supplied running PRG is compressed, so raw file equality would compare different formats. VICE executes its BASIC-stub entry at `$100D` and stops at `$1800` before the first game instruction. The script saves `$1000–$3FFF` and compares that decompressed memory with the rebuilt payload.

Across addresses represented in `OBJ`, exactly one byte differs: `$3262` is `$58` in the source build and `$57` in the running version. This is the low byte of `LDA SCRPOS+2` at `$3261`: the source reads `$0C58`, whereas the supplied running version reads `$0C57`. The instruction is in the scoring routine and its source comment identifies the thousands digit. The build retains the source instruction. The reason for the revision difference and its complete gameplay consequences are not established.

There are 41 differences across the full memory comparison:

| Region                   | Different bytes |
| ------------------------ | --------------- |
| Terrain `$1001–$1002`    | 2               |
| Reserved `SCRBUF`        | 24              |
| Score operand `$3262`    | 1               |
| Output gap `$3BF3–$3BFF` | 13              |
| Last font byte `$3FFF`   | 1               |

The reserved buffer and output gap contain different initial contents. The other differences are recorded without silently patching the source or importing reference bytes. This establishes a source-accurate reassembly, with a closely related running reference; it does not establish complete equality to that reference or identify either version as a definitive retail master.

---

## Emulator Evidence and Limits

VICE renders the title and executes the normal game initialization and countdown. The verification script stops at the original `BIT JFIRE` menu test, supplies the fire-input flag, and resumes the existing code. It reaches `LOOP` at `$2A24` with `TITLE = 0` and `LIVES = 3`. No executable instructions are patched, and the script does not jump directly into the game loop.

![Restored title screen](images/restored-title.png)

![Entry into gameplay](images/restored-gameplay.png)

The screenshots have been visually inspected. The test establishes rendering and gameplay entry with scripted input. Manual keyboard mapping, joystick operation, sound playback, collisions, scoring over a full game, level transitions, and a complete play-through remain unverified. Physical C16 hardware has not been tested.

---

## Recovery Background

For the original development environment and the disk/source recovery background, refer to [Dorks Dilemma C16](https://github.com/anthonyjclarke/Dorks_Dilemma_C16) and its [Development History](https://github.com/anthonyjclarke/Dorks_Dilemma_C16/blob/main/docs/DEVELOPMENT_HISTORY.md). This document covers only Tycoon Tex's inputs, build, and validation.
