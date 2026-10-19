"""Regression checks for historical syntax, provenance and assembled bytes."""

import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from d64_image import D64Image
from restore_c16 import ROOT, IMAGE, OLDER, build_game, mos_hex, prepare_sources
from source_converter import convert, flatten


class RestorationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='tycoon-test-')
        cls.build = Path(cls.temp.name)
        cls.before = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (ROOT / 'Original Source Recovered').rglob('*') if p.is_file()}
        with contextlib.redirect_stdout(io.StringIO()):
            cls.output = build_game(cls.build).read_bytes()
        cls.manifest = json.loads((cls.build / 'recovery-manifest.json').read_text())
        cls.sources, _ = prepare_sources(cls.build / 'inputs')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_complete_prg_matches_verified_baseline(self):
        self.assertEqual(len(self.output), 12290)
        self.assertEqual(self.output[:2], b'\x00\x10')
        self.assertEqual(hashlib.sha256(self.output).hexdigest(),
                         '09c9d0e3120e847f63c19b24560d46d08f15a48bfacb6956de01230e15cffbcd')

    def test_all_object_records_match_assembled_code(self):
        obj = mos_hex(self.sources['OBJ'])
        self.assertEqual(len(obj), 9179)
        for address, value in obj.items():
            self.assertEqual(self.output[2 + address - 0x1000], value, hex(address))
        missing = set(range(0x1800, 0x3BF3)) - obj.keys()
        self.assertEqual(missing, set(range(0x25E1, 0x25F9)))

    def test_fresh_modules_and_explicit_fallbacks(self):
        files = {r['name']: r for r in self.manifest['files']}
        self.assertFalse(files['PLAY-GAME']['fallback'])
        self.assertFalse(files['OBJ']['fallback'])
        self.assertTrue(files['TYCOON-TEX']['fallback'])
        self.assertTrue(files['FIRING/MEGACODE']['fallback'])
        self.assertEqual(sum(not r['fallback'] for r in files.values()), 56)
        self.assertIn('SOURCE: TYCOON-TEX:36', (self.build / 'tycoon.s').read_text())

    def test_terrain_and_font_have_original_asset_provenance(self):
        for address, value in mos_hex(self.sources['CHAR#1']).items():
            self.assertEqual(self.output[2 + address - 0x1000], value)
        self.assertEqual(self.output[2 + 0x2C00:], (OLDER / 'FRAK.BIN').read_bytes()[2:])

    def test_inputs_are_unchanged_by_build(self):
        after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in self.before}
        self.assertEqual(self.before, after)

    def test_missing_ambiguous_and_recursive_includes_fail(self):
        with self.assertRaisesRegex(ValueError, 'ambiguous/missing'):
            flatten({'MAIN': ['.LIB LOST*']}, 'MAIN')
        with self.assertRaisesRegex(ValueError, 'ambiguous/missing'):
            flatten({'MAIN': ['.LIB AL*'], 'ALPHA': [], 'ALTO': []}, 'MAIN')
        with self.assertRaisesRegex(ValueError, 'Recursive'):
            flatten({'MAIN': ['.LIB MAIN*']}, 'MAIN')

    def test_historical_syntax_keeps_instructions_and_literals(self):
        result = convert([('TEST', 1, 'SELFMD LDA $FFFF,X'),
                          ('TEST', 2, 'REG = $FF00'),
                          ('TEST', 3, "TEXT .BYTE 'A;B',0"),
                          ('TEST', 4, "LDA #'Z")])
        self.assertIn('SELFMD: LDA $FFFF,X', result)
        self.assertIn('REG = $FF00', result)
        self.assertIn('TEXT: .BYTE "A;B",0', result)
        self.assertIn("LDA #'Z'", result)

    def test_invalid_hex_and_cyclic_disk_fail(self):
        with self.assertRaisesRegex(ValueError, 'checksum'):
            mos_hex([';011800000000'])
        disk = D64Image(IMAGE)
        data = bytearray(disk.data)
        # Isolated synthetic cycle on the first sector; no original file edits.
        data[0:2] = b'\x01\x00'
        disk.data = data
        with self.assertRaisesRegex(ValueError, 'Cyclic'):
            list(disk.chain(1, 0))


if __name__ == '__main__':
    unittest.main()
