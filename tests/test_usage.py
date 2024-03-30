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
        ssno.StandardName.from_json(json1)
