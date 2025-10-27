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

            assert isinstance(p, rdflib.URIRef), f'Error: {p} is not a URIRef'
            if p not in (rdflib.RDF.first,
                         rdflib.RDF.rest,
                         rdflib.OWL.qualifiedCardinality,
                         rdflib.OWL.minQualifiedCardinality,
                         rdflib.OWL.maxQualifiedCardinality,
                         rdflib.OWL.withRestrictions,
                         rdflib.OWL.someValuesFrom,
                         rdflib.OWL.allValuesFrom,
                         rdflib.OWL.cardinality,
                         rdflib.OWL.onDataRange,
                         rdflib.OWL.onDatatype,
                         rdflib.OWL.onProperty,
                         rdflib.OWL.onClass,
                         rdflib.OWL.inverseOf,
                         rdflib.URIRef("http://www.w3.org/2001/XMLSchema#pattern"),
                         rdflib.OWL.unionOf) and o not in (
                    rdflib.OWL.Class,
                    rdflib.OWL.Restriction,
                    rdflib.OWL.ObjectProperty,
                    rdflib.RDFS.Datatype
            ):
                assert isinstance(s, rdflib.URIRef), f'Error: {s} ({p} {o}) is not a URIRef'
        assert len(g) > 0, f'Error: No triples found in {onto_purl}.'
        assert g, f'Error: {onto_purl} is not a graph'
