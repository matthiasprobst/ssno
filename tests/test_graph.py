"""This thest is mainly taken from: https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/develop/tests/graph-test.py?ref_type=heads"""
import logging
import pathlib
import unittest

import rdflib
from rdflib import Graph

logger = logging.getLogger('ssno')

__this_dir__ = pathlib.Path(__file__).parent


class TestGraph(unittest.TestCase):

    def test_parse_onto(self):
        m4i_ttl = __this_dir__.parent / 'ssno.ttl'
        onto_purl = str(m4i_ttl)
        onto_format = "ttl"

        g = Graph()
        g.parse(onto_purl, format=onto_format)
        for s, p, o in g:
            assert isinstance(s, rdflib.URIRef), f'Error: {s} is not a URIRef'
            assert isinstance(p, rdflib.URIRef), f'Error: {s} is not a URIRef'
            assert isinstance(p, str), f'Error: {s} is not a str'
        assert len(g) > 0, f'Error: No triples found in {onto_purl}.'
        assert g, f'Error: {onto_purl} is not a graph'
