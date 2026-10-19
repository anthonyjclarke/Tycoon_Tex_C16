# Quick Start

## Build

Install Python 3.9+, cc65, and VICE. From the project folder:

```sh
./build.sh
python3 scripts/run_vice.py
```

The output is `build/tycoon-tex.prg`. The game loads at `$1000` and enters at `$1800` (`SYS 6144`); use the supplied launcher because the rebuilt PRG has no BASIC stub.

---

## PlatformIO and VS Code

Open this folder in VS Code, install the recommended PlatformIO extension, and run the default build task. From a PlatformIO terminal:

```sh
pio run -e c16
pio run -e c16 -t upload
```

For a build with the same game bytes and debug artifacts, use `pio run -e c16_debug`. Outputs are under `build/platformio/<environment>/`.

---

## Controls and Checks

Press `K` on the title screen to select keyboard control. The source maps `Z`, `X`, `;`, `/`, and Return to left, right, up, down, and fire/select. Manual host-key mapping remains unverified.

```sh
make test
make verify
make run-original
```

See [Build and Run](docs/BUILD_AND_RUN.md) and [Testing](TESTING.md) for details.
