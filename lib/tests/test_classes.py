import json
import sys
import unittest

sys.path.insert(0, '.')

from .. import classes

import pydantic


class TestClasses(unittest.TestCase):

    def test_standard_name(self):
        """describe "air_temperature" from
        http://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html"""

        with self.assertRaises(pydantic.ValidationError):
            # invalid URL
            atemp = classes.StandardName(standard_name='air_temperature',
                                         canonical_units='K',
                                         description='Air temperature is the bulk temperature of the air, not the surface (skin) temperature.',
                                         dbpedia_match='Air_temperature')

        atemp = classes.StandardName(standard_name='air_temperature',
                                     canonical_units='K',
                                     description='Air temperature is the bulk temperature of the air, not the surface (skin) temperature.',
                                     dbpedia_match='http://dbpedia.org/resource/Air_temperature')
        self.assertEqual(atemp.standard_name, 'air_temperature')
        self.assertEqual(atemp.canonical_units, 'K')
        self.assertEqual(atemp.description,
                         'Air temperature is the bulk temperature of the air, not the surface (skin) temperature.')
        self.assertEqual(atemp.dbpedia_match, 'http://dbpedia.org/resource/Air_temperature')

        self.assertEqual(str(atemp), 'air_temperature')
        self.assertEqual(atemp.standard_name_table, None)

        # to dict:
        atemp_dict = atemp.model_dump(exclude_none=True)
        self.assertIsInstance(atemp_dict, dict)
        self.assertEqual(atemp_dict['standard_name'], 'air_temperature')
        self.assertEqual(atemp_dict['canonical_units'], 'K')
        self.assertEqual(atemp_dict['description'],
                         'Air temperature is the bulk temperature of the air, not the surface (skin) temperature.')
        self.assertEqual(atemp_dict['dbpedia_match'], 'http://dbpedia.org/resource/Air_temperature')

        atemp_json = atemp.model_dump_json()
        self.assertIsInstance(atemp_json, str)
        atemp_json_dict = json.loads(atemp_json)
        self.assertIsInstance(atemp_json_dict, dict)
        self.assertEqual(atemp_json_dict['standard_name'], 'air_temperature')
        self.assertEqual(atemp_json_dict['canonical_units'], 'K')
        self.assertEqual(atemp_json_dict['description'],
                         'Air temperature is the bulk temperature of the air, not the surface (skin) temperature.')
        self.assertEqual(atemp_json_dict['dbpedia_match'], 'http://dbpedia.org/resource/Air_temperature')

        # to json-ld:
        atemp_jsonld = atemp.dump_jsonld()
        print(atemp_jsonld)
        # serialize with rdflib:
        jsonld_dict = json.loads(atemp_jsonld)
        self.assertEqual(jsonld_dict['@context']['@import'], classes.SSNO_CONTEXT_URL)
        print(jsonld_dict)
        self.assertEqual(jsonld_dict['@type'], 'StandardName')
        self.assertEqual(jsonld_dict['standard name'], 'air_temperature')
        self.assertEqual(jsonld_dict['canonical units'], 'https://qudt.org/vocab/unit/K')

        # https://qudt.org/vocab/unit/K
