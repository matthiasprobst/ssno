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
        ssno_ttl = __this_dir__.parent / 'ssno.ttl'
        onto_purl = str(ssno_ttl)

        g = Graph()
        g.parse(onto_purl, format="ttl")
        for s, p, o in g:
            print(s, p, o)

            assert isinstance(p, rdflib.URIRef), f'Error: {s} is not a URIRef'
            if p not in (rdflib.RDF.first, rdflib.RDF.rest,
                         rdflib.OWL.unionOf) and o != rdflib.OWL.Class and o != rdflib.OWL.Restriction and p != rdflib.OWL.onProperty and p != rdflib.OWL.inverseOf and p != rdflib.OWL.someValuesFrom and p != rdflib.OWL.allValuesFrom:
                assert isinstance(s, rdflib.URIRef), f'Error: {s} is not a URIRef'
        assert len(g) > 0, f'Error: No triples found in {onto_purl}.'
        assert g, f'Error: {onto_purl} is not a graph'
