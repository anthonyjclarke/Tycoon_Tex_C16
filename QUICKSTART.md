# Quick Start

## Build

Install Python 3.9+, cc65, and VICE. From the project folder:

```sh
./build.sh
python3 scripts/run_vice.py
```

The output is `build/tycoon-tex.prg`. The game loads at `$1000` and enters at `$1800` (`SYS 6144`). Use the launcher, because the rebuilt PRG has no BASIC stub.

---

## PlatformIO and VS Code

Open this folder in VS Code, install the recommended PlatformIO extension and run the default build task. From a PlatformIO terminal:

```sh
pio run -e c16
pio run -e c16 -t upload
```

`pio run -e c16_debug` gives the same game bytes plus debug files. Outputs land in `build/platformio/<environment>/`.

---

## Controls and Checks

Press `K` on the title screen for keyboard control. The source maps `Z`, `X`, `;`, `/` and Return to left, right, up, down and fire/select. I haven't checked the host-key mapping by hand yet.

```sh
make test
make verify
make run-original
```

See [Build and Run](docs/BUILD_AND_RUN.md) and [Testing](TESTING.md) for details.
