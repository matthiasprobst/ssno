import ontolutils
import pathlib
import ssno
import unittest
from ontolutils import parse_unit, QUDT_UNIT


import json
import pathlib
import unittest

import ssno


# ignore User Warnings:

__this_dir__ = pathlib.Path(__file__).parent

SNT_JSONLD = """{
  "@context": {
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dct": "http://purl.org/dc/terms/",
    "prov": "http://www.w3.org/ns/prov#",
    "ssno": "https://matthiasprobst.github.io/ssno#"
  },
  "@type": "ssno:StandardNameTable",
  "dct:title": "OpenCeFaDB Fan Standard Name Table",
  "ssno:standard_names": [
    {
      "@type": "ssno:StandardName",
      "ssno:standard_name": "absolute_pressure",
      "dcterms:description": "Pressure is force per unit area. Absolute air pressure is pressure deviation to a total vacuum.",
      "canonical_units": "Pa",
      "@id": "local:39257b94-d31c-480e-a43c-8ae7f57fae6d"
    },
    {
      "@type": "ssno:StandardName",
      "ssno:standard_name": "ambient_static_pressure",
      "dcterms:description": "Static air pressure is the amount of pressure exerted by air that is not moving. Ambient static air pressure is the static air pressure of the surrounding air.",
      "canonical_units": "Pa",
      "@id": "local:0637ec26-310b-4b0a-bf4c-e51d4afccc7d"
    },
    {
      "@type": "ssno:StandardName",
      "ssno:standard_name": "ambient_temperature",
      "dcterms:description": "Air temperature is the bulk temperature of the air, not the surface (skin) temperature. Ambient air temperature is the temperature of the surrounding air.",
      "canonical_units": "K",
      "@id": "local:3286d041-a826-4776-9d25-065dae107b55"
    },
    {
      "@type": "ssno:StandardName",
      "ssno:standard_name": "auxiliary_fan_rotational_speed",
      "dcterms:description": "Number of revolutions of an auxiliary fan.",
      "canonical_units": "1/s",
      "@id": "local:2a521e9d-4481-4965-9b42-390db2da4c83"
    }
  ]
}"""


class TestSSNO(unittest.TestCase):

    def tearDown(self):
        pathlib.Path('snt.json').unlink(missing_ok=True)

    def test_standard_name(self):
        sn = ssno.StandardName(standard_name='x_velocity',
                               description='x component of velocity',
                               canonical_units=QUDT_UNIT.M_PER_SEC)  # 'm s-1'
        self.assertIsInstance(sn, ontolutils.Thing)
        self.assertIsInstance(sn, ssno.StandardName)
        self.assertEqual(sn.standard_name, 'x_velocity')
        self.assertEqual(sn.description, 'x component of velocity')
        self.assertEqual(sn.canonical_units, str(parse_unit('m s-1')))

        sn = ssno.StandardName(standard_name='x_velocity',
                               description='x component of velocity',
                               canonical_units='m s-1')
        self.assertEqual(sn.canonical_units, str(parse_unit('m s-1')))

        with open('sn.jsonld', 'w') as f:
            f.write(sn.model_dump_jsonld())

        sn_loaded = ontolutils.query(ssno.StandardName, source='sn.jsonld')
        self.assertEqual(len(sn_loaded), 1)
        self.assertEqual(sn_loaded[0].standard_name, 'x_velocity')
        self.assertEqual(sn_loaded[0].description, 'x component of velocity')
        self.assertEqual(sn_loaded[0].canonical_units, str(parse_unit('m s-1')))

        sn_loaded = ssno.StandardName.from_jsonld(data=sn.model_dump_jsonld())
        self.assertEqual(len(sn_loaded), 1)
        self.assertEqual(sn_loaded[0].standard_name, 'x_velocity')
        self.assertEqual(sn_loaded[0].description, 'x component of velocity')
        self.assertEqual(sn_loaded[0].canonical_units, str(parse_unit('m s-1')))

        pathlib.Path('sn.jsonld').unlink(missing_ok=True)



class TestVersion(unittest.TestCase):

    def test_version(self):
        this_version = 'x.x.x'
        setupcfg_filename = __this_dir__ / '../setup.cfg'
        with open(setupcfg_filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'version' in line:
                    this_version = line.split(' = ')[-1].strip()
        self.assertEqual(ssno.__version__, this_version)
