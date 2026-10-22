# Sharing on GitHub

## Repository

The public repository is [anthonyjclarke/Tycoon_Tex_C16](https://github.com/anthonyjclarke/Tycoon_Tex_C16). I work on `dev` and merge verified checkpoints into `main`. The annotated tag `v1.0.0` marks the first preservation checkpoint.

`.gitignore` leaves out generated output, PlatformIO caches, Python caches and macOS metadata. It deliberately keeps the original `.prg`, `.BIN`, `.SEQ`, `.d64` files, the images and the scrapbook. `.gitattributes` turns off text normalization for both preserved input folders, including the original CRLF source exports.

The README links to the build instructions, validation, history, artifact catalogue and the Dorks Dilemma recovery story. `RIGHTS.md` records the historical notices I've kept, and I haven't assigned a new licence.

---

## Final Local Checks

Run these commands from the project root:

```sh
./build.sh
make test
pio run -e c16 -e c16_debug
make verify
make docs-check
git status --short
```

The first three checks need Python, cc65 and PlatformIO. The VICE verification also needs the running PRG and a graphical desktop. `docs/SOURCE_AND_VALIDATION.md` and `TESTING.md` have the current results and the limits of the verification.

The evidence in `docs/verification/` and the screenshots in `docs/images/` belong to the documented checkpoint. If you change the source, refresh them only after reviewing any changed bytes and rerunning the relevant checks.

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

For later work, use `dev`, review the changes, run the relevant checks, then commit. Merge into `main` only when a checkpoint is verified:

```sh
git switch dev
git add .
git diff --cached --stat
git commit -m "docs(scope): describe the change"
git push origin dev
```

On every push and pull request, the GitHub Actions workflow runs the source build, the regression tests, both PlatformIO environments, the handbook freshness check, the documentation tests and the output agreement checks. It uploads the rebuilt PRG and reports as a workflow artifact, and it doesn't run a graphical emulator. Results are on the repository's [Actions page](https://github.com/anthonyjclarke/Tycoon_Tex_C16/actions).

---

## Version Tags

`v1.0.0` is the first published preservation checkpoint and `v1.2.0` the documentation release; 1.1.0 was recorded in the changelog but never tagged. Later verified checkpoints get new annotated version tags on `main`. Leave published tags alone, so their source, documentation and recorded evidence can still be reproduced.
