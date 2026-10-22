# Changelog

All notable changes to the Tycoon Tex C16 preservation project. Dates are DD-MM-YYYY. This history was reconstructed from the git log and the project documentation after the first two commits.

---

## [1.2.0] 22-10-2026

Documentation release. The game build and its output are unchanged. It is not tagged.

### Added

- `docs/GREMLIN_ARCHIVE.md`: Mark Hardisty's book *A Gremlin in the Works* and his Gremlin Graphics Archive, the 1992 disk list from the archive's `READ.ME`, and how to cite them. Its project section shows that all 96 files in the archive's `DISK6.ZIP` match the 1992 folder by CRC-32 and size, lists the files the archive doesn't have, compares the C64 `DISK1A`, and links the archive's three Tycoon Tex posts. The first five sections are shared with the other Micro Projects reconstructions.
- History and Credits: a section on the Gremlin Archive and the book.
- The new chapter in the HTML handbook, after History and Credits.
- README status badges (release, platform, byte match, toolchain, PlatformIO, emulator, status) as local SVGs in `docs/images/badges/`, so the offline HTML handbook still builds.

---

## [1.1.0] 20-10-2026

Documentation and analysis release (commit `8e44b59`). The game build and its output are unchanged. It is not tagged.

### Added

- `CODEBASE_ANALYSIS.md`: how the game works, covering states, raster scheduling, player and hazard rules, collision, graphics, audio, scoring and the differences between revisions.
- `docs/PORTING_GUIDE.md`: a plan for modifying the game or porting it, with a compatibility-choice table, a proposed architecture and a test plan.
- `docs/analysis/`: generated developer references. These are `CODE_REFERENCE.md`, `codebase-index.json` and `asset-data.json`, plus three SVG graphics atlases (terrain, one-bit font, two-bit font) and a README.
- Illustrated graphics section with five PNG figures, a walking GIF and `graphics-manifest.json` recording input hashes and the VICE TED palette.
- `docs/analysis/rule-probes.json`: five controlled VICE observations of original routines. They confirm the one-byte score difference, where 999 plus one point grants an extra life in the source build and not in the running version. They also cover pressure borrowing and the completion carry.
- `scripts/analyze_codebase.py`, `scripts/probe_gameplay_rules.py` and `scripts/render_game_graphics.py` (needs Pillow 10.1 or later) to regenerate the above.
- `docs/TYCOON_TEX.html`: the complete offline HTML handbook, built from 16 Markdown documents with images, diagrams, chapter search, image enlargement and print support.
- HTML build tooling: `scripts/build_docs.mjs`, `scripts/docs/` (template, CSS, reader controls), `scripts/vendor/` (Marked 17.0.5 and Mermaid 10.9.3 with their licences), `docs/handbook.json` and `docs/HTML_DOCUMENTATION.md`.
- `test/test_docs.mjs`: seven documentation tests covering navigation, embedded assets, failure handling, freshness and watch mode.
- Makefile targets `docs`, `docs-html`, `docs-watch`, `docs-check` and `test-docs`.

### Changed

- Rewrote the prose in the existing guides in first person and plainer language: `README.md`, `QUICKSTART.md`, `TESTING.md`, `RIGHTS.md`, `src/README.md` and the `docs/` guides. Facts, hedges, headings, links, tables and code blocks are unchanged.
- `README.md` links to the HTML handbook, the codebase analysis and the porting guide.

---

## [1.0.0] 20-10-2026

Initial preservation checkpoint (commit `974ff72`, tag `v1.0.0`): the surviving Tycoon Tex source reassembled for the Commodore 16 and Plus/4.

### Added

- Preserved inputs: `Original Source Recovered/` (the 2026 disk image and extraction, and the 1992 text export) and `Original Artifacts/` (the packed running game, artwork, cassette inlay and the scanned scrapbook). Both are kept byte for byte.
- `scripts/restore_c16.py`, the build pipeline. It reads the disk image, checks the 56 live files against the 2026 extraction, fills missing modules from the 1992 export through its `INDEX`, expands the original `.LIB` order and assembles with ca65 and ld65. It builds 59 main modules (36 fresh, 23 fallback), and the terrain graphics are assembled from source with the surviving `FRAK.BIN` as the font.
- `scripts/d64_image.py` (disk reader) and `scripts/source_converter.py` (MOS assembler to ca65 syntax), plus `config/c16.cfg` for the memory layout.
- Verified output: all 9,179 bytes of the original `OBJ` object listing match with zero differences. The PRG is 12,290 bytes, loads at `$1000`, starts at `$1800` and has SHA-256 `09c9d0e3120e847f63c19b24560d46d08f15a48bfacb6956de01230e15cffbcd`.
- PlatformIO project with `c16` and `c16_debug` environments (pinned to `platformio/native@1.2.1`) that produce identical game bytes, plus labels, listing, map and debug data.
- `build.sh`, a `Makefile`, VS Code tasks, settings and recommended extensions.
- `scripts/run_vice.py`, a launcher that loads the PRG at the saved address and jumps to `$1800`. It has an `--original` option for the packed running game.
- `scripts/verify_vice.py`, an automated VICE 3.10 check on a PAL C16 with 16 KB RAM. It confirms title rendering and entry into gameplay, and compares memory with the decompressed running game, finding 41 differences.
- `test/test_restoration.py`: eight regression tests covering the PRG hash and header, every `OBJ` byte, source selection and fallbacks, asset provenance, unchanged input hashes, syntax conversion, and rejection of bad includes, malformed hex records and cyclic disk chains.
- GitHub Actions workflow that runs the tests, builds both PlatformIO environments and checks their bytes against the direct build.
- Documentation: `README.md`, `QUICKSTART.md`, `TESTING.md`, `RIGHTS.md`, `src/README.md`, and under `docs/` the Artifact Catalogue, Build and Run, History and Credits, Sharing on GitHub, Source and Validation and Source Inventory.
- Verification evidence in `docs/verification/` and the restored title and gameplay screenshots in `docs/images/`.
- Repository housekeeping: `.gitignore`, `.gitattributes` (text normalization off for both preserved input folders) and `.editorconfig`.

### Known limits

- The running game differs from the source build in one initialized code byte: `$3262` is `$58` in the source and `$57` in the running version, in the scoring routine. The build keeps the source version.
- Not yet tested: host keyboard mapping, a physical joystick, sound, scoring over a full game, level transitions, a full play-through and real C16 hardware.
