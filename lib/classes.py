"""Classes of the ssno ontology"""
import abc
import json
from typing import List, Union

import pydantic
from pydantic import BaseModel, HttpUrl

standard_name_table: str

SSNO_CONTEXT_URL = "https://raw.githubusercontent.com/matthiasprobst/ssno/main/ssno_context.jsonld"


class _Core(abc.ABC):

    @abc.abstractmethod
    def _repr_html_(self):
        """Returns the HTML representation of the class"""


class Resource(BaseModel, _Core):
    """dcat:Resource"""
    title: str  # dcterms:title
    description: str = None  # dcterms:description
    creator: str = None  # dcterms:creator
    version: str = None  # dcat:version

    def _repr_html_(self):
        """Returns the HTML representation of the class"""
        return f"{self.__class__.__name__}({self.title})"


class Distribution(Resource):
    """dcat:Distribution"""
    downloadURL: HttpUrl  # dcat:downloadURL, e.g.
    mediaType: str = None  # dcat:mediaType
    byteSize: int = None  # dcat:byteSize

    def _repr_html_(self):
        """Returns the HTML representation of the class"""
        return f"{self.__class__.__name__}({self.downloadURL})"


class Dataset(Resource):
    """dcat:Dataset"""
    identifier: HttpUrl = None  # dcterms:identifier, see https://www.w3.org/TR/vocab-dcat-3/#ex-identifier
    publisher: str = None  # dcterms:publisher, see https://www.w3.org/TR/vocab-dcat-3/#ex-adms-identifier
    distribution: Distribution  # dcat:Distribution


# def dump_jsonld(model, types:Dict, context:Dict):
#     """Returns the JSON-LD representation of the model"""
#     import json
#     _json_dict = json.loads(model.model_dump_json())
#     _json_dict['@type'] = types
#     _json_dict['@context'] = context
#     return json.dumps(_json_dict)

class StandardName(BaseModel, _Core):
    """Implementation of ssno:StandardNmae"""
    standard_name: str
    canonical_units: str
    description: str = None  # dcterms:description
    dbpedia_match: Union[str, HttpUrl] = None  # ssno:dbpediaMatch
    standard_name_table: Dataset = None  # ssno:standard_name_table (subclass of dcat:Dataset)

    def __str__(self):
        """Returns the standard name"""
        return self.standard_name

    def dump_dict(self, *args, **kwargs):
        """alias for model_dump()"""
        return self.model_dump(*args, **kwargs)

    def dump_json(self, *args, **kwargs):
        """alias for model_dump_json()"""
        return self.model_dump_json(*args, **kwargs)

    def dump_jsonld(self, id=None, *args, **kwargs):
        """alias for model_dump_json()"""

        import rdflib

        g = rdflib.Graph()
        _atemp_json_dict = {k.replace('_', ' '): v for k, v in self.model_dump().items()}

        _qudt_unit_dict = {"K": "https://qudt.org/vocab/unit/K"}

        _atemp_json_dict['canonical units'] = _qudt_unit_dict.get(_atemp_json_dict['canonical units'],
                                                                  _atemp_json_dict['canonical units'])

        _id = '_:' or id
        jsonld = {"@context": {"@import": SSNO_CONTEXT_URL},
                  "@graph": [
                      {"@id": _id,
                       "@type": "ssno:StandardName",
                       **_atemp_json_dict}
                  ]}

        g.parse(data=json.dumps(jsonld), format='json-ld')
        # self.assertEqual(len(g), 5)
        # for t in g:
        #     print(t)
        return g.serialize(format='json-ld',
                           context={"@import": SSNO_CONTEXT_URL},
                           indent=4)
        #
        #
        # _json_dict = json.loads(self.model_dump_json(*args, **kwargs))
        #
        # jsonld_dict = {"@context": {"@import": SSNO_CONTEXT_URL}}
        #
        # if id is not None:
        #     _json_dict['@id'] = id
        #
        # jsonld_dict.update({"@type": "ssno:StandardName"})
        # jsonld_dict.update(_json_dict)
        # return json.dumps(jsonld_dict, indent=kwargs.get('indent', 4))

    @pydantic.field_validator('dbpedia_match')
    @classmethod
    def _dbpedia_match(cls, url):
        """Validates the dbpedia_match"""
        if url is None:
            return None
        else:
            return str(HttpUrl(url))

    def _repr_html_(self):
        """Returns the HTML representation of the class"""
        return self.standard_name


class StandardNameTable(Dataset):
    """Implementation of ssno:StandardNameTable

    Parameters
    ----------
    title: str
        Title of the Standard Name Table (dcterms:title)
    description: str
        Description of the Standard Name Table (dcterms:description)
    creator: str
        Creator of the Standard Name Table (dcterms:creator)
    version: str
        Version of the Standard Name Table (dcat:version)
    identifier: str
        Identifier of the Standard Name Table, e.g. the DOI (dcterms:identifier)
    standard_names: List[StandardName]
        List of Standard Names (ssno:standard_name)
    guidelines: Distribution
        Guidelines for the use of the Standard Name Table (dcat:Distribution)

    """
    standard_names: List[StandardName] = None  # ssno:standard_name
    guideline: Distribution = None  # ssno:guideline

    def _repr_html_(self):
        """Returns the HTML representation of the class"""
        return f"{self.__class__.__name__}(<a href={self.distribution.downloadURL}>{self.title}</a>)"
