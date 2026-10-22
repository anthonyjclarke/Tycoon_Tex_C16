# History and Credits

## Tycoon Tex

Tycoon Tex is a 1985 Commodore 16 and Plus/4 game that I programmed at Micro Projects for Gremlin Graphics Ltd. The surviving main source credits the concept to Matthew Clarke, Anthony Clarke, and Ian Stewart, and carries the notice `program (c) '85 micro projects`.

As I recorded on 20 October 2026, I remember playing Moon Patrol in pubs and elsewhere at the time. Tycoon Tex looks very like it, but I can't recall exactly how the concept came about. That's my memory, not a documented design brief, and the game isn't an official arcade conversion.

The 1992 date on the source folder belongs to the older extraction and export, not to the game's development. The source notices and the surviving packaging both point to 1985.

---

## Surviving Contemporary Material

The artwork, cassette packaging and press scrapbook give some context from the time. Page 5 of the scrapbook has the Tycoon Tex cassette inlay, and pages 11 and 12 have reviews. I've kept the scans as they are and haven't added publication details the cuttings don't make clear.

The separate `Tycoon Tex Cassette Inlay.jpg` shows the cassette cover, description and gameplay screenshots. [Artifacts](ARTIFACTS.md) lists the whole collection with page references.

---

## The Gremlin Archive and the Book

Mark Hardisty's book *A Gremlin in the Works* (Bitmap Books), the officially endorsed history of Gremlin Graphics, tells the Micro Projects story, and I contributed to it. His [Gremlin Graphics Archive](https://www.gremlinarchive.com/) publishes my 1992 export of the development disks, including this game's `DISK6`, and introduces my part in [A Gremlin in the Works – Anthony Clarke](https://www.gremlinarchive.com/index.php/2017/07/31/a-gremlin-in-the-works-anthony-clarke/). [Gremlin Archive and the Book](GREMLIN_ARCHIVE.md) has the references, the archive's disk list and how my 1992 folder matches `DISK6`.

---

## Recovery Background and Build Template

My original C64/1541 development setup and the later source recovery are written up in the companion [Dorks Dilemma C16 repository](https://github.com/anthonyjclarke/Dorks_Dilemma_C16). Its [History and Credits](https://github.com/anthonyjclarke/Dorks_Dilemma_C16/blob/main/docs/HISTORY_AND_CREDITS.md) has my recollections and the recovery-tool acknowledgements.

This project adapts the Dorks Dilemma source conversion, disk reader, ca65/ld65 build, PlatformIO integration and VICE-monitor approach. Tycoon Tex's source order, memory layout, graphics choices, original object listing and comparison with the running version are validated separately here. I've left the recovery story in the companion repository on purpose.

---

## Tool Acknowledgements

The modern build uses the [cc65 toolchain](https://cc65.github.io/), the [VICE emulator](https://vice-emu.sourceforge.io/), [PlatformIO](https://platformio.org/) and [Visual Studio Code](https://code.visualstudio.com/), along with Python. The reassembly and emulator checks depend on the people who write and maintain them.

The original Commodore tools, the disk capture tools and the people who helped with recovery are acknowledged in the companion project's history. The historical copyright notices in the source, binaries and printed material are all kept. See [Rights and Preservation](../RIGHTS.md).
