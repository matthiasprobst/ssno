"""This thest is mainly taken from: https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/develop/tests/graph-test.py?ref_type=heads"""
import logging
import pathlib
import unittest

from pivmetalib import ssno

logger = logging.getLogger('ssno')

__this_dir__ = pathlib.Path(__file__).parent


class TestUserGuide(unittest.TestCase):
    """Testing the User Guide code"""

    def test_json_1(self):
        json1 = __this_dir__ / 'json1.json'
        sn = ssno.StandardName.from_jsonld(source=str(json1))
        snt = ssno.StandardNameTable.from_jsonld(source=str(json1))
        self.assertEqual(len(sn), 1)
        for _sn in sn:
            self.assertIsInstance(_sn, ssno.StandardName)
        self.assertEqual(len(snt), 1)
        self.assertEqual(snt[0].identifier, "https://doi.org/10.5281/zenodo.10428817")
        self.assertEqual(sn[0].standard_name, 'x_velocity')
        self.assertEqual(sn[0].canonical_units, 'http://qudt.org/vocab/unit/M-PER-SEC')


    def test_json_2(self):
        json2 = __this_dir__ / 'json2.json'
        snt = ssno.StandardNameTable.from_jsonld(source=str(json2))
        self.assertEqual(snt[0].description, 'My table description')
        self.assertEqual(len(snt), 1)
        self.assertEqual(len(snt[0].standard_names), 2)
        self.assertEqual(sorted(snt[0].standard_names)[0].standard_name, 'x_velocity')
        self.assertEqual(sorted(snt[0].standard_names)[1].standard_name, 'y_velocity')