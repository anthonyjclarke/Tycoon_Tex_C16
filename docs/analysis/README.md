# Generated Developer References

## Contents

[Code Reference](CODE_REFERENCE.md) lists main modules in assembly order, all selected source locations, the complete zero-page allocation, and symbols grouped by module. [Codebase Index](codebase-index.json) contains the same underlying catalogue plus direct control-transfer sites. [Asset Data](asset-data.json) contains the raw selected graphics and 57 named byte tables for a port or analysis tool.

The three SVG atlases show the [terrain multicolor indices](terrain-multicolor.svg), the [upper font as one-bit pixels](font-hires.svg) and the [upper font as two-bit pixels](font-multicolor.svg). They decode the original bytes into vector rectangles and label each glyph code and address. The colors are index keys, not a calibrated TED palette or a rebuilt final frame.

The [illustrated graphics section](../../CODEBASE_ANALYSIS.md#main-character--tex-and-his-walk-frames) reconstructs complete Tex frames, environment-specific aliens, pipeline pieces and breaks, and background motifs. Five PNG figures and a walking GIF are stored in `graphics/`, together with a [manifest](graphics/graphics-manifest.json) recording their input/output hashes and VICE TED palette. The screen-composition figure annotates the existing verified gameplay capture; the other figures decode original asset bytes with environment colors.

[Rule Probes](rule-probes.json) records five controlled observations from original routines in VICE. It's a reviewed snapshot of evidence and isn't regenerated automatically.

---

## Codebase Index Fields

`assembly_roots` lists the selected modules for each of the main, terrain, and comparison actor builds. `modules` records source provenance, fallback status, raw byte size, normalized logical line count, instruction-like source lines, assembly-stage membership, and the allocation attributed to the main output region.

`main_region_bytes` includes machine code, embedded data, and reserved road-buffer bytes. It is not an executed-instruction count or a function-size estimate. Modules used only by graphics builds or variable declarations may have zero main-region allocation. `raw_bytes` measures the preserved input representation and can include CRLF overhead absent from normalized lines.

`symbols` records the defining module, normalized logical source line, address where resolved, original comment, and a conservative kind. `equate` entries also retain their expression. Instruction labels include local branch destinations, not just subroutine entries. A data/control label classification is intentionally broader than a proven data structure.

`zero_page_variables` records symbol, address, byte size, comment, and declaration line. Addresses are JSON integers in bytes, not hexadecimal strings. The allocated variables occupy `$0002–$00E9`; the reset routine's larger clearing range is described in the main analysis.

`direct_transfers` records source module and line, opcode, operand text, target module when identified, and target address when the expression resolves. Offset entries such as `SCORE+2` resolve to the offset address. Indirect or macro-placeholder expressions can remain unresolved. The list omits fall-through, IRQ-vector dispatch, runtime patches, and expanded macro control flow; it is not a complete call graph.

`source_image_sha256` and `prg_sha256` identify the analyzed input and output. The static method is documented in `scripts/analyze_codebase.py`. Counts are useful navigation metrics and should not be mistaken for a runtime profile.

---

## Asset Data Fields

`terrain` and `font` each provide an integer memory address, glyph count, and hexadecimal byte payload without a PRG load header. Terrain has 256 glyphs at `$1000`; the selected upper font has 128 at `$3C00`. Each glyph occupies eight consecutive bytes.

`tables` maps original symbol names to integer addresses, byte counts, and hexadecimal payloads. These cover player animation, environment-specific actor glyphs, title lettering, palettes, speed/progress settings, terrain motifs, render footprints, input masks, difficulty masks, and selected presentation/effect data. They are named extracts, not a serialization of the whole program or every source-defined table.

Decode bytes explicitly in a consumer. Original `.WORD` address tables are little-endian. Other table semantics, strides, coordinate units, frame order, and rendering interpretation are described in [Codebase Analysis](../../CODEBASE_ANALYSIS.md) and [Porting Guide](../PORTING_GUIDE.md). A raw byte does not by itself establish a universal color, collision category, or elapsed time.

The upper font is the initial selected `FRAK.BIN` payload. Runtime animation and environment installation change its contents; reconstruct those changes when building complete actor frames. The font atlas is not a substitute for those state-dependent images.

---

## Reproduction and Verification

From the repository root:

```sh
./build.sh
python3 scripts/analyze_codebase.py
```

The exporter uses Python's standard library and the existing build outputs. Before it writes the catalogue it checks that listing-derived ownership covers the whole main region. The same inputs and build always give the same output, and the original source collections and the game binary are never rewritten.

To regenerate the assembled graphics figures with Python and Pillow 10.1 or later:

```sh
python3 scripts/render_game_graphics.py
```

This reads `asset-data.json`, the saved palette in `graphics/graphics-manifest.json`, and `../images/restored-gameplay.png`. Pass `--palette /path/to/vice/PLUS4/colodore_ted.vpl` to replace the saved 128-color TED palette. GIF timing is illustrative and does not measure the game's speed-dependent animation cadence.

To regenerate rule-probe observations:

```sh
python3 scripts/verify_vice.py
python3 scripts/probe_gameplay_rules.py
```

The second command writes reports and monitor captures to `build/rule-probes/`. Review them before replacing the included `rule-probes.json`. The probe caller is installed at `$0500`, outside the game's declared workspaces, with the game instructions untouched, interrupts disabled and decimal mode cleared. It tests selected arithmetic under controlled state, not complete gameplay or IRQ interaction.
