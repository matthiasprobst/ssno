"""This thest is mainly taken from: https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/develop/tests/graph-test.py?ref_type=heads"""
import logging
import rdflib
from pathlib import Path
from rdflib import Graph

logger = logging.getLogger('ssno')


def parse_onto(onto_purl, onto_format):
    g = Graph()
    g.parse(onto_purl, format=onto_format)
    for s, p, o in g:
        assert isinstance(s, rdflib.URIRef), f'Error: {s} is not a URIRef'
        assert isinstance(p, rdflib.URIRef), f'Error: {s} is not a URIRef'
        assert isinstance(p, str), f'Error: {s} is not a str'
    assert len(g) > 0, f'Error: No triples found in {onto_purl}.'
    assert g, f'Error: {onto_purl} is not a graph'


if __name__ == '__main__':
    logger.debug('Start testing graph')
    m4i = Path(__file__).parent.parent / 'ssno.ttl'
    parse_onto(str(m4i), onto_format="ttl")
    logger.debug('Finished testing graph')
