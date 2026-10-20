#!/usr/bin/env python3
"""Reconstruct explanatory graphics from Tycoon Tex's exported original bytes.

Requires Pillow 10.1 or later. Uses asset-data.json, a VICE TED .vpl palette (or the palette
saved in graphics-manifest.json), and the verified gameplay screenshot.
This is an asset decoder and diagram generator, not a TED/raster emulator.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
INK = '#142c45'
MUTED = '#52677c'
PAPER = '#f4f7fb'
BLUE = '#1768a4'
LINE = '#bdcbd9'
ENVIRONMENTS = ('Desert', 'Ice', 'Pipes')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def font(size=20):
    return ImageFont.load_default(size=size)


def label(im, xy, text, size=20, fill=INK):
    ImageDraw.Draw(im).text(xy, text, font=font(size), fill=fill)


def canvas(title, subtitle, height):
    im = Image.new('RGB', (1200, height), PAPER)
    label(im, (32, 22), title, 30)
    label(im, (32, 65), subtitle, 18, MUTED)
    ImageDraw.Draw(im).line((32, 99, 1168, 99), fill=LINE, width=2)
    return im


def enlarged(im, scale):
    return im.resize((im.width * scale, im.height * scale), Image.Resampling.NEAREST)


def tile_grid(im, xy, width, height, scale):
    d = ImageDraw.Draw(im)
    x, y = xy
    for c in range(width + 1):
        d.line((x + c * 8 * scale, y, x + c * 8 * scale, y + height * 8 * scale), fill=BLUE)
    for r in range(height + 1):
        d.line((x, y + r * 8 * scale, x + width * 8 * scale, y + r * 8 * scale), fill=BLUE)


def code_grid(im, xy, rows, cell=(48, 36), highlight_from=None):
    x, y = xy
    d = ImageDraw.Draw(im)
    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            box = (x+c*cell[0], y+r*cell[1], x+(c+1)*cell[0], y+(r+1)*cell[1])
            fill = '#daeafa' if highlight_from is not None and r >= highlight_from else 'white'
            d.rectangle(box, fill=fill, outline=LINE)
            label(im, (box[0]+7, box[1]+8), str(value), 17)


class Graphics:
    def __init__(self, assets, palette):
        self.assets = assets
        self.palette = palette
        self.terrain = bytes.fromhex(assets['terrain']['hex'])
        self.font = bytes.fromhex(assets['font']['hex'])
        assert len(self.terrain) == 2048 and len(self.font) == 1024
        self.colors = self.table('SHTCOL')
        assert len(self.colors) == 48

    def table(self, name):
        return bytes.fromhex(self.assets['tables'][name]['hex'])

    def sheet(self, area):
        return self.colors[area*16:(area+1)*16]

    def actor_bank(self, area, frame=None):
        bank = bytearray(self.font)
        for name, address in [('ARRCHR', 0x3EE8), ('BACHAR', 0x3F68), ('SUCHAR', 0x3FA8)]:
            bank[address-0x3C00:address-0x3C00+48] = self.table(name)[area*48:(area+1)*48]
        if frame is not None:
            bank[0x248:0x278] = self.table('ANDATA')[frame*48:(frame+1)*48]
        return bank

    def render(self, rows, bank, attribute, colors):
        """colors = background, MULTI1, MULTI2. No cursor, blink or reverse."""
        assert all(len(row) == len(rows[0]) for row in rows)
        out = Image.new('RGB', (len(rows[0])*8, len(rows)*8))
        # TED attribute bit 3 selects multicolor within a multicolor window.
        # In that window the per-cell color is attribute & $77 in both modes.
        mc = bool(attribute & 8)
        cell_color = attribute & 0x77
        pens = [self.palette[c & 0x7F] for c in (*colors, cell_color)]
        for r, row in enumerate(rows):
            for c, code in enumerate(row):
                glyph = bank[code*8:code*8+8]
                assert len(glyph) == 8
                for y, byte in enumerate(glyph):
                    for x in range(8):
                        index = (byte >> (6-2*(x//2))) & 3 if mc else (3 if byte & (0x80 >> x) else 0)
                        out.putpixel((c*8+x, r*8+y), tuple(pens[index]))
        return out

    def actor(self, area, rows, tex=False, frame=None):
        s = self.sheet(area)
        return self.render(rows, self.actor_bank(area, frame), s[11] if tex else 0x78, (s[10], s[8], s[9]))

    def land(self, area, rows, hills=False):
        s = self.sheet(area)
        return self.render(rows, self.terrain, s[6] if hills else s[2],
                           (s[7], s[4], s[5]) if hills else (s[3], s[0], s[1]))


def player(g, output):
    im = canvas('Tex: 15 characters make one player',
                'Original font + ANDATA walk frames | 24 x 40 display pixels | one-bit artwork', 735)
    rows = [list(range(64+r*3, 67+r*3)) for r in range(5)]
    assert list(g.table('YVAL')) == [r*40+c for r in range(5) for c in range(3)]
    im.paste(enlarged(g.actor(0, rows, tex=True), 7), (42, 135))
    tile_grid(im, (42, 135), 3, 5, 7)
    label(im, (247, 128), 'Screen character codes', 23)
    code_grid(im, (247, 173), rows, (52, 42), highlight_from=3)
    label(im, (450, 175), '64-72: static upper body', 21)
    label(im, (450, 215), '$3E00-$3E47: 72 bytes from FRAK.BIN', 18, MUTED)
    label(im, (450, 282), '73-78: animated legs', 21, BLUE)
    label(im, (450, 322), '$3E48-$3E77: 48 bytes replaced per frame', 18, MUTED)
    label(im, (42, 441), 'Whole player reconstructed in cyclic DECODE order: 1, 3, 0, 2', 23)
    for i, frame in enumerate(g.table('DECODE')):
        x = 55+i*275
        im.paste(enlarged(g.actor(0, rows, tex=True, frame=frame), 4), (x, 495))
        label(im, (x+115, 515), f'ANDATA {frame}', 19)
        label(im, (x+115, 552), f'offset {frame*48}', 18, MUTED)
    label(im, (42, 686), 'Blue grid = 8 x 8 character cells. Images use the desert playfield palette.', 18, MUTED)
    im.save(output/'tex-character.png')
    frames = [enlarged(g.actor(0, rows, tex=True, frame=f), 6) for f in g.table('DECODE')]
    frames[0].save(output/'tex-walk.gif', save_all=True, append_images=frames[1:], duration=200,
                   loop=0, disposal=2, optimize=False)


def aliens(g, output):
    im = canvas('Aliens and hazards: assembled character footprints',
                'ALIGET installs environment variants; active alien attributes are all $78.', 995)
    specs = [
        ('Arrow', [list(g.table('ARCHAR')[:4]), list(g.table('ARCHAR')[4:])], '93-98 + space', '3 x 2 art; 4 x 2 writes'),
        ('Bouncer', [[109, 110], [111, 112], [113, 114]], '109-114', '2 x 3 cells'),
        ('Crash-diver', [[117, 118, 119], [120, 121, 122]], '117-122', '3 x 2 cells'),
        ('Jet', [list(g.table('JTCHAR')[:6]), list(g.table('JTCHAR')[6:])], '99-108 + space', '5 x 2 art; 6 x 2 writes'),
        ('Jet bomb', [[32, 32], [115, 116]], '115-116 below spaces', '2 x 1 art; 2 x 2 writes'),
    ]
    for area, name in enumerate(ENVIRONMENTS):
        label(im, (390+area*270, 122), name, 25)
    for i, (name, rows, codes, size) in enumerate(specs):
        y = 180+i*150
        label(im, (32, y), name, 23)
        label(im, (32, y+35), codes, 18, MUTED)
        label(im, (32, y+65), size, 18, MUTED)
        for area in range(3):
            x = 342+area*270
            im.paste(enlarged(g.actor(area, rows), 4), (x, y))
            tile_grid(im, (x, y), len(rows[0]), len(rows), 4)
    label(im, (32, 952), 'Jet and bomb retain their font glyphs; their shared playfield colors change by environment.', 18, MUTED)
    im.save(output/'alien-characters.png')


def road_rows(buffer):
    assert len(buffer) % 2 == 0
    return [buffer[1::2], buffer[0::2]]


def pipeline(g, output):
    im = canvas('Pipeline and ground: a queue of two-cell columns',
                'ROAD chooses motifs; SCRBUF holds character codes; NEWROD writes each pair to screen RAM.', 960)
    for i, (start, count) in enumerate(zip(g.table('PIPCHR')[::2], g.table('PIPCHR')[1::2])):
        x = 35+i*287
        label(im, (x, 123), f'Pipe motif {i}: {start}-{start+count-1}', 20)
        rows = road_rows(list(range(start, start+count)))
        im.paste(enlarged(g.land(2, rows), 6), (x, 164))
        code_grid(im, (x+119, 164), rows, (52, 42))
    for area, key, y in [(0, 'DESCHR', 295), (1, 'ICECHR', 405)]:
        label(im, (35, y), ENVIRONMENTS[area]+' ground', 21)
        for i, (start, count) in enumerate(zip(g.table(key)[::2], g.table(key)[1::2])):
            x = 300+i*285
            rows = road_rows(list(range(start, start+count)))
            im.paste(enlarged(g.land(area, rows), 4), (x, y))
            label(im, (x+90, y+13), f'{start}-{start+count-1}', 18, MUTED)
    label(im, (35, 520), 'Example streamed break: left edge + one middle section + right edge', 23)
    buffer = list(range(214, 218))+list(range(222, 226))+list(range(221, 217, -1))
    rows = road_rows(buffer)
    im.paste(enlarged(g.land(2, rows), 5), (35, 569))
    tile_grid(im, (35, 569), 6, 2, 5)
    code_grid(im, (340, 569), rows, (56, 40))
    label(im, (35, 684), 'SCRBUF byte order:', 21)
    label(im, (35, 725), '214,215 | 216,217 | 222,223 | 224,225 | 221,220 | 219,218', 21, BLUE)
    label(im, (35, 771), 'Each pair is bottom,top. Display rows above are top,bottom.', 20)
    label(im, (35, 820), 'At the right edge: SCRBUF[X+1] -> $0F97; SCRBUF[X] -> $0FBF.', 20)
    label(im, (35, 865), 'BUFPOI advances by 2; a spent queue triggers ROAD. Maximum queue capacity: 24 bytes.', 18, MUTED)
    label(im, (35, 910), 'The illustrated middle section is one valid BREAK choice; random play also uses other sections.', 18, MUTED)
    im.save(output/'pipeline-assembly.png')


def hill_rows(start):
    # NEWHIL starts at HILY[4], increments HILCHR, and decrements X.
    return [[start+c*5+4-r for c in range(8)] for r in range(5)]


def background(g, output):
    im = canvas('Background: five motifs, stored column by column',
                'Each motif is 8 x 5 characters (64 x 40 pixels). The same bytes use three environment palettes.', 1055)
    for i in range(5):
        x = 32+i*232
        label(im, (x, 124), f'Glyphs {i*40}-{i*40+39}', 19)
        im.paste(enlarged(g.land(0, hill_rows(i*40), hills=True), 3), (x, 162))
    label(im, (32, 312), 'First motif: screen order after NEWHIL places eight columns', 23)
    code_grid(im, (32, 355), hill_rows(0), (54, 36))
    label(im, (520, 367), 'First stored column: 0, 1, 2, 3, 4', 21)
    label(im, (520, 410), 'First screen column, top to bottom: 4, 3, 2, 1, 0', 20, BLUE)
    label(im, (520, 455), 'HILY = 0, 40, 80, 120, 160; X counts 4 down to 0.', 18, MUTED)
    label(im, (520, 493), 'HILLST chooses starts 0,40,80,120,160,40,80,120.', 18, MUTED)
    strip = [sum((hill_rows(start)[r] for start in range(0, 200, 40)), []) for r in range(5)]
    for area, name in enumerate(ENVIRONMENTS):
        y = 590+area*140
        label(im, (32, y+22), name, 23)
        im.paste(enlarged(g.land(area, strip, hills=True), 3), (200, y))
    label(im, (32, 1020), 'These strips concatenate all five motifs for inspection; actual play selects their order procedurally.', 18, MUTED)
    im.save(output/'background-assembly.png')


def screen(screenshot, output):
    capture = Image.open(screenshot).convert('RGB')
    if capture.size != (384, 288):
        raise ValueError('Expected the verified 384 x 288 VICE capture; review crop coordinates for new captures')
    im = canvas('From graphics bytes to the displayed game',
                'Verified PAL C16 gameplay capture at left; screen-memory bands and raster roles at right.', 1140)
    # The verified capture has a 320 x 200 character matrix at (32, 40).
    xy = (32, 130)
    im.paste(enlarged(capture.crop((32, 40, 352, 240)), 2), xy)
    bands = [
        (0, 3, 'HUD | rows 0-2 | $0C00-$0C77', '$3C00 font; fixed horizontal position'),
        (3, 8, 'Hills | rows 3-7 | $0C78-$0D3F', '$1000 terrain; HILLX fine scroll'),
        (8, 22, 'Play | rows 8-21 | $0D40-$0F6F', '$3C00 font/actors; fixed X; Tex at row 17'),
        (22, 24, 'Ground | rows 22-23 | $0F70-$0FBF', '$1000 terrain; GNDX fine scroll'),
        (24, 25, 'Message | row 24 | $0FC0-$0FE7', '$3C00 font; MESSX fine scroll'),
    ]
    d = ImageDraw.Draw(im)
    centers = (154, 219, 350, 490, 551)
    for (start, end, title, detail), cy in zip(bands, centers):
        y = xy[1]+start*16
        d.rectangle((32, y, 672, xy[1]+end*16), outline='#e6edf5', width=1)
        mid = xy[1]+(start+end)*8
        d.line((672, mid, 692, mid, 705, cy+10), fill=BLUE, width=2)
        label(im, (715, cy-6), title, 19)
        label(im, (715, cy+25), detail, 17, MUTED)
    # Highlight Tex's actual resting 3 x 5 footprint at row 17, column 1.
    d.rectangle((48, 402, 96, 482), outline='#ffffff', width=2)
    label(im, (32, 634), 'Character data', 23)
    label(im, (32, 674), '8 bytes per glyph in RAM', 19, MUTED)
    label(im, (32, 708), '$1000 terrain / $3C00 font', 19, MUTED)
    label(im, (359, 634), 'Screen + attributes', 23)
    label(im, (359, 674), '$0C00 + row*40 + column', 19, MUTED)
    label(im, (359, 708), 'Attribute at screen - $0400', 19, MUTED)
    label(im, (735, 634), 'TED draws each band', 23)
    label(im, (735, 674), 'IRQ selects bank, palette and fine X', 19, MUTED)
    label(im, (735, 708), 'Glyph bits become visible pixels', 19, MUTED)
    for x1, x2 in [(285, 341), (663, 716)]:
        d.line((x1, 652, x2, 652), fill=BLUE, width=3)
        d.polygon([(x2, 652), (x2-10, 646), (x2-10, 658)], fill=BLUE)
    label(im, (32, 785), 'Software assembly example: Tex at ML = $0EA9 (row 17, column 1)', 23)
    for i, text in enumerate([
        'MANON writes codes 64-78 at YVAL offsets: 0,1,2 / 40,41,42 / ... / 160,161,162.',
        'MANCOL is written to matching attribute cells, beginning at $0AA9.',
        'ANIMAT replaces glyph bytes at $3E48; existing screen codes immediately select the new legs.',
        'MANOFF clears those 15 screen cells to code 32; it does not restore a saved background.',
    ]):
        label(im, (32, 837+i*43), text, 19, MUTED)
    label(im, (32, 1040), 'Band borders are explanatory overlays. The capture shows startup gameplay, with no active aliens.', 18)
    label(im, (32, 1080), 'The matrix is 40 x 25 cells; terrain/play windows use 38-column masking for scrolling edges.', 18, MUTED)
    im.save(output/'screen-composition.png')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path, default=ROOT/'docs/analysis/asset-data.json')
    parser.add_argument('--output-dir', type=Path, default=ROOT/'docs/analysis/graphics')
    parser.add_argument('--palette', type=Path, help='VICE 128-entry TED .vpl file; saved for subsequent runs')
    parser.add_argument('--screenshot', type=Path, default=ROOT/'docs/images/restored-gameplay.png')
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output_dir/'graphics-manifest.json'
    if args.palette:
        raw = args.palette.read_bytes()
        colors = [list(bytes.fromhex(line.strip())) for line in raw.decode().splitlines()
                  if re.fullmatch(r'(?:[0-9A-Fa-f]{2}\s+){2}[0-9A-Fa-f]{2}', line.strip())]
        palette = {'name': 'VICE '+args.palette.name, 'sha256': digest(raw), 'rgb': colors,
                   'source': 'https://github.com/VICE-Team/svn-mirror/blob/main/vice/data/PLUS4/'+args.palette.name}
    else:
        palette = json.loads(manifest_path.read_text())['palette']
    if len(palette['rgb']) != 128:
        raise ValueError('A TED palette must contain 128 RGB entries')
    assets = json.loads(args.assets.read_text())
    g = Graphics(assets, palette['rgb'])
    player(g, args.output_dir)
    aliens(g, args.output_dir)
    pipeline(g, args.output_dir)
    background(g, args.output_dir)
    screen(args.screenshot, args.output_dir)
    manifest = {'method': 'Original glyph bits and tables; nearest-neighbor enlargement; schematic assembly diagrams.',
                'asset_data_sha256': digest(args.assets.read_bytes()),
                'screenshot_sha256': digest(args.screenshot.read_bytes()),
                'palette': palette,
                'gif_frame_order': list(g.table('DECODE')), 'gif_frame_duration_ms': 200,
                'gif_timing': 'Illustration only; game animation cadence depends on speed.',
                'images': {p.name: {'size': list(Image.open(p).size), 'sha256': digest(p.read_bytes())}
                           for p in sorted(args.output_dir.iterdir()) if p.suffix in ('.png', '.gif')}}
    manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')
    print(f'Wrote {len(manifest["images"])} images and {manifest_path}')


if __name__ == '__main__':
    main()
