# Sharing on GitHub

## Repository

The public repository is [anthonyjclarke/Tycoon_Tex_C16](https://github.com/anthonyjclarke/Tycoon_Tex_C16). Development uses `main`, with the initial preservation checkpoint identified by the annotated tag `v1.0.0`.

`.gitignore` excludes generated output, PlatformIO caches, Python caches, and macOS metadata. It deliberately retains original `.prg`, `.BIN`, `.SEQ`, `.d64`, images, and the scrapbook. `.gitattributes` disables text normalization for both preserved input folders, including the original CRLF source exports.

The README links the build instructions, validation, history, artifact catalogue, and the Dorks Dilemma recovery background. `RIGHTS.md` records the retained historical notices; this preparation does not assign a new licence.

---

## Final Local Checks

Run these commands from the project root:

```sh
./build.sh
make test
pio run -e c16 -e c16_debug
python3 scripts/verify_vice.py
git status --short
```

The first three checks require Python, cc65, and PlatformIO. VICE verification also requires the supplied running PRG and a graphical desktop. Current results and verification limits are recorded in `docs/SOURCE_AND_VALIDATION.md` and `TESTING.md`.

The included evidence in `docs/verification/` and screenshots in `docs/images/` represent the documented checkpoint. If changing the source, refresh that evidence only after reviewing any changed bytes and rerunning the relevant checks.

---

## Clone or Update

Clone the published repository with:

```sh
git clone https://github.com/anthonyjclarke/Tycoon_Tex_C16.git
cd Tycoon_Tex_C16
```

To check out the initial tagged checkpoint:

```sh
git switch --detach v1.0.0
```

For subsequent work, return to `main`, review the changes, run the relevant checks, and commit and push:

```sh
git switch main
git add .
git diff --cached --stat
git commit -m "Describe the change"
git push origin main
```

The GitHub Actions workflow runs the source build, regression tests, both PlatformIO environments, and output agreement checks on pushes and pull requests. It uploads the rebuilt PRG and reports as a workflow artifact; it does not run a graphical emulator. View results on the repository's [Actions page](https://github.com/anthonyjclarke/Tycoon_Tex_C16/actions).

---

## Version Tags

`v1.0.0` identifies the first published preservation checkpoint. Later verified checkpoints can use new annotated version tags. Keep existing published tags intact so their source, documentation, and recorded evidence remain reproducible.
