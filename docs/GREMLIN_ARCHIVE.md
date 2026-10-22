# Gremlin Archive and the Book

## About This Chapter

The first five sections are written to be reused unchanged in each of my Micro Projects C16 reconstructions (Xargon Wars, Xargon's Revenge, Dork's Dilemma, Tycoon Tex). Only [In This Project](#in-this-project) is specific to Tycoon Tex. I checked the links and the archive contents on 22 October 2026.

---

## A Gremlin in the Works

*A Gremlin in the Works* by Mark Hardisty, published by [Bitmap Books](http://www.bitmapbooks.co.uk/products/a-gremlin-in-the-works), is the officially endorsed history of Gremlin Graphics, endorsed by founder Ian Stewart. The 572-page book follows the company from Monty Mole and Thing on a Spring to its purchase by Infogrames in 1999, with interviews, letters, photographs and design documents. Mark announced it on the archive in the post [A Gremlin in the Works – The Book](https://www.gremlinarchive.com/index.php/2016/05/22/a-gremlin-in-the-works-the-book/) (22 May 2016).

I contributed to the book and to the archive. Mark's post [A Gremlin in the Works – Anthony Clarke](https://www.gremlinarchive.com/index.php/2017/07/31/a-gremlin-in-the-works-anthony-clarke/) (31 July 2017) introduces my part. In 1985 I joined Gremlin with Jason Perkins and Mark Rogers as Micro Projects Limited. Micro Projects wrote many of Gremlin's C16 games, as well as Thing on a Spring on the C64 and its port of Monty on the Run. The book tells the Micro Projects story in full.

---

## The Gremlin Graphics Archive

[The Gremlin Graphics Archive](https://www.gremlinarchive.com/) is Mark Hardisty's companion site to the book. It collects Gremlin's games, box art, adverts, letters, royalty statements, staff photographs and source code. Posts relevant to Micro Projects include:

| Post                                             | Date         |
| :----------------------------------------------- | :----------- |
| [Micro Projects Source Code][ga-src]             | 25 May 2016  |
| [Micro Projects Royalty Statements][ga-roy]      | 24 May 2016  |
| [Compliment Slip / Royalty Notes][ga-slip]       | 24 May 2016  |
| [Early Tradeshow Leaflet][ga-trade]              | 23 May 2016  |
| [Anthony Clarke Photograph][ga-photo]            | 2 June 2016  |
| [A Gremlin in the Works – Anthony Clarke][ga-me] | 31 July 2017 |

Each game also has its own post: for example [Xargon's Revenge (C16/Plus4)][ga-xr] (1 November 2016) and [Xargon Wars – Trade Promotion][ga-xw] (24 May 2016). The compilations have theirs too: [C16 Classics][ga-classics] (13 February 2021) and [C16 Omnibus][ga-omnibus] (20 December 2021).

---

## My Development Disks in the Archive

The [Micro Projects Source Code][ga-src] post holds the Oric and C16 assembler source I donated for many of the company's games, including the unreleased Ultra. Its download, [Old-Development-Disks.zip][ga-zip] (1,894,396 bytes, 846 entries), is my 1992 PC export of the original Commodore disks, re-zipped in 2014. It has two folders, `Disk 1-6/` and `Disk 7-11/`. Each disk is there both as my 1992 PKZIP file (for example `DISK9.ZIP`) and as an extracted folder, with a `READ.ME` from 1992 that names them:

| Disk     | Contents (from `READ.ME`)      |
| :------- | :----------------------------- |
| `DISK1A` | Tycoon Tex C64                 |
| `DISK1B` | Dorks Dilemma C64              |
| `DISK2`  | Utilities                      |
| `DISK3`  | Thingy                         |
| `DISK4A` | Graphics Editor                |
| `DISK4B` | Graphic2                       |
| `DISK5`  | Dorks Dilemma C16              |
| `DISK6`  | Tycoon Tex C16                 |
| `DISK7A` | Xargon Wars C16                |
| `DISK7B` | Xargon Wars C16 (Hack Version) |
| `DISK8`  | Revenge of Xargon (Xargon II)  |
| `DISK9`  | Xargon's Revenge               |
| `DISK10` | Xargon's Revenge – 5 lives     |
| `DISK11` | `LOAD "*",8,1`                 |

Each disk ZIP includes an `INDEX` listing the original Commodore directory next to the PC file names. One thing to watch: in the extracted `Disk 7-11/DISK9/` folder, `LOADER.BIN` is 0 bytes, while `DISK9.ZIP` itself holds the full file. Compare against the disk ZIPs, not the extracted folders.

---

## Plus/4 World and the Archive

[Plus/4 World](https://plus4world.powweb.com/) has entries for these games. Its [Xargon's Revenge entry](https://plus4world.powweb.com/software/Xargons_Revenge) says the early-stages and disk versions were rebuilt from source files on disks I gave to Mark Hardisty, which are the 1992 export above. Check each game's entry for similar notes. Copies labelled "early stages", "disk version" or "with loading screen" are then not independent releases. They come from my own development disks, and only the original cassettes show what was actually sold.

---

## How to Cite

> Mark Hardisty, *A Gremlin in the Works*, Bitmap Books. Officially endorsed history of Gremlin Graphics.

> Mark Hardisty, "Micro Projects Source Code", The Gremlin Graphics Archive, 25 May 2016, <https://www.gremlinarchive.com/index.php/2016/05/25/micro-projects-source-code/>. Download: `Old-Development-Disks.zip`.

> Mark Hardisty, "A Gremlin in the Works – Anthony Clarke", The Gremlin Graphics Archive, 31 July 2017, <https://www.gremlinarchive.com/index.php/2017/07/31/a-gremlin-in-the-works-anthony-clarke/>.

---

## In This Project

The 1992 source in `Original Source Recovered/1992 - Tycoon Tex C16/` is the archive's `DISK6`, "Tycoon Tex C16". There's no copy of `DISK6.ZIP` itself in this project, so I compared file by file. The archive's `Disk 1-6/DISK6.ZIP` is 94,814 bytes with CRC-32 `adbf0f1f` and holds 96 files, all dated 7 October 1992. Each of those 96 matches a file in my 1992 folder by CRC-32 and size:

| Archive `DISK6.ZIP`                         | This project's 1992 folder  |
| :------------------------------------------ | :-------------------------- |
| 84 `.TXT` source exports                    | Same bytes, saved as `.SEQ` |
| `ASMC64.BAS`, `BOOTALL.BAS`, `HYPRALOA.BAS` | Identical                   |
| 8 `.BIN` graphics and utility binaries      | Identical                   |
| `INDEX` (7,318 bytes)                       | Identical                   |

The binaries are `CHARS`, `DB1`, `DB2`, `DOS52`, `EDITOR`, `FRAK`, `MEGASUPE` and `SUPERLOA`. [Source Inventory](SOURCE_INVENTORY.md) covers how the build uses them. Only the extension differs on the source exports: the archive's `OBJ.TXT` is my `OBJ.SEQ`, and so on. The archive's extracted `Disk 1-6/DISK6/` folder agrees with `DISK6.ZIP` on all 96 files, so this disk doesn't have the empty-file problem `DISK9` has.

These files in this project aren't anywhere in the archive:

- **`ASMC64.PRG`, `BOOTALL.PRG` and `HYPRALOA.PRG`** in the 1992 folder. They're Commodore program files that go with the matching `.BAS` listings, and the archive only has the listings. `ASMC64.BAS` and `HYPRALOA.BAS` are each a `SYS` line followed by a hex dump of the program.
- **`TycoonTex-C16.d64`** and its 2026 extraction. None of the 56 extracted `.seq` files matches an archive file, because the extraction keeps the disk's own bytes and the 1992 export was converted to PC text.
- **`Original Artifacts/tycoon_tex.prg`**, the packed running game.

The archive's `DISK1A`, "Tycoon Tex C64", is the C64 version and isn't in this project. It has 97 files. 28 of them are identical to `DISK6` files, and its `CDATHILS.TXT` is byte-identical to `DISK6`'s `CDATHIL6.TXT`. `DISK6` alone has `BACKUPVA`, `CDATHIL6`, `CDATPBRK`, `MEGASUPE.BIN` and `SUPERLOA.BIN`. `DISK1A` alone has `CDATHILS`, `FRAK2.BAS`, `FRAK2.BIN`, `HILOADC6.BIN`, `OCHR.TXT` and `POLLKEYS.BAS`.

The archive has three posts on the game itself:

| Post                               | Date         | What it holds                        |
| :--------------------------------- | :----------- | :----------------------------------- |
| [Tycoon Tex Artwork][ga-tt-art1]   | 26 May 2016  | The cover painting without its text  |
| [Tycoon Tex (Artwork)][ga-tt-art2] | 8 June 2016  | Recreated cover artwork              |
| [Tycoon Tex (C64 Port)][ga-tt-c64] | 13 June 2016 | Hokuto Force's C64 preview build     |

The two artwork images are not byte-identical to `Tycoon Tex - No Text.jpg` or `Tycoon Tex - With Text.jpg` in [Artifacts](ARTIFACTS.md). The C64 port post says Hokuto Force pieced the conversion together from the C64 source files I donated, and describes it as the C16 code and graphics with no hardware sprites and no sound.

[ga-src]: https://www.gremlinarchive.com/index.php/2016/05/25/micro-projects-source-code/
[ga-zip]: http://agremlinintheworks.co.uk/archive/wp-content/uploads/2016/05/Old-Development-Disks.zip
[ga-roy]: https://www.gremlinarchive.com/index.php/2016/05/24/micro-projects-royalty-statements/
[ga-slip]: https://www.gremlinarchive.com/index.php/2016/05/24/compliment-slip-royalty-notes/
[ga-trade]: https://www.gremlinarchive.com/index.php/2016/05/23/early-tradeshow-leaflet/
[ga-photo]: https://www.gremlinarchive.com/index.php/2016/06/02/anthony-clarke-photograph/
[ga-me]: https://www.gremlinarchive.com/index.php/2017/07/31/a-gremlin-in-the-works-anthony-clarke/
[ga-xr]: https://www.gremlinarchive.com/index.php/2016/11/01/xargons-revenge-c16plus4/
[ga-xw]: https://www.gremlinarchive.com/index.php/2016/05/24/xargon-wars-trade-promotion/
[ga-classics]: https://www.gremlinarchive.com/index.php/2021/02/13/c16-classics/
[ga-omnibus]: https://www.gremlinarchive.com/index.php/2021/12/20/c16-omnibus/
[ga-tt-art1]: https://www.gremlinarchive.com/index.php/2016/05/26/tycoon-tex-artwork/
[ga-tt-art2]: https://www.gremlinarchive.com/index.php/2016/06/08/tycoon-tex-artwork-2/
[ga-tt-c64]: https://www.gremlinarchive.com/index.php/2016/06/13/tycoon-tex-c64-port/
