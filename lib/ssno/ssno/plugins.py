import abc
import pathlib
import warnings
from typing import Dict, Union


class TableReader(abc.ABC):
    """Abstract Standard Name Table Reader"""

    def __init__(self, filename: Union[str, pathlib.Path]):
        self.filename = pathlib.Path(filename)
        assert self.filename.exists(), f'{self.filename} does not exist'
        assert self.filename.is_file(), f'{self.filename} is not a file'

    @abc.abstractmethod
    def parse(self) -> Dict:
        """Parse the file"""


class XMLReader(TableReader):

    def parse(self) -> Dict:
        """Parse the file"""
        try:
            import xmltodict
        except ImportError:
            raise ImportError('Package "xmltodict" is missing, but required to import from XML files.')

        with open(str(self.filename), 'r', encoding='utf-8') as file:
            my_xml = file.read()
        xmldict = xmltodict.parse(my_xml)
        _name = list(xmldict.keys())[0]

        xmldata = xmldict[_name]

        def _parse_standard_name(sndict):
            canonical_units = sndict.get('canonical_units', '')
            if canonical_units == '1':
                canonical_units = ''
            elif canonical_units is None:
                canonical_units = ''
            description = sndict.get('description', '')
            if description is None:
                description = ''
            standard_name = sndict.get('@id')
            assert standard_name is not None, 'Expected key "@id" in the XML file.'
            assert canonical_units is not None, 'Expected key "canonical_units" in the XML file.'
            assert description is not None, 'Expected key "description" in the XML file.'
            return dict(standard_name=standard_name,
                        canonical_units=canonical_units,
                        description=description)

        version = xmldata.get('version', None)
        if version is None:
            version = xmldata.get('version_number', None)

        # last_modified = xmldata.get('last_modified', None)

        contact = xmldata.get('contact', None)
        institution = xmldata.get('institution', None)
        if "@" in contact and institution is not None:
            # it is an email address
            from ..prov import Organization
            creator = Organization(mbox=contact, name=institution)
        else:
            creator = contact
            
            # else cannot be parsed

        sn_data = xmldata.get('entry', None)
        if sn_data is None:
            raise KeyError('Expected key "entry" in the XML file.')
        data = {'standard_name': [_parse_standard_name(sn) for sn in sn_data],
                'version': version,
                # 'modified': last_modified,
                'creator': creator}

        if 'title' not in xmldata:
            data['title'] = self.filename.stem

        sndata = data.pop('standard_name')
        for sn in sndata:
            if sn['description'] is None:
                name = sn['standard_name']
                warnings.warn(f'Description of "{name}" is None. Setting to empty string.', UserWarning)
                sn['description'] = ""
        data['standard_names'] = sndata
        return data


class YAMLReader(TableReader):

    def parse(self):
        try:
            import yaml
        except ImportError as e:
            raise ImportError('Package "pyyaml" is missing, but required to import from YAML files.') from e

        with open(self.filename, 'r') as f:
            data = yaml.safe_load(f)
        standard_names = data['standard_names']

        def _parse_standard_names(name, sndata: Dict):
            for ustr in ('unit', 'units', 'canonical_unit'):
                if ustr in sndata:
                    sndata['canonical_units'] = sndata.pop(ustr)
                    break
            _data = {'standard_name': name,
                     **sndata
                     }
            for k in list(_data.keys()):
                if k not in ('canonical_units', 'description', 'standard_name'):
                    _data.pop(k)
            return _data

        creator = data.get('creator', {})
        # make the orcid id the ID of the creator:
        if creator:
            if isinstance(creator, list):
                for ic, c in enumerate(creator.copy()):
                    if c['orcid_id']:
                        creator[ic]['id'] = c['orcid_id']
            else:
                if creator['orcid_id']:
                    creator['id'] = creator['orcid_id']

        qualifications = {}
        # locations = data.get('locations', None)
        # devices = data.get('devices', None)
        # media = data.get('media', None)
        # conditions = data.get('conditions', None)
        # reference_frames = data.get('reference_frames', None)
        # surfaces = data.get('surfaces', None)

        for q in ('locations', 'devices', 'media', 'conditions', 'reference_frames', 'surfaces'):
            if q in data:
                qualifications[q] = [{'name': ak, 'description': av} for ak, av in data[q].items()]
        # if locations:
        #     qualifications = {'locations': [{'location': ak, 'description': av} for ak, av in locations.items()]}

        data_dict = {'title': data.get('name', data.get('title', None)),
                     'creator': data.get('creator', {}),
                     'version': data.get('version', None),
                     'description': data.get('description', None),
                     'identifier': data.get('identifier', None),
                     'standard_names': [_parse_standard_names(k, v) for k, v in standard_names.items()],
                     **qualifications}
        if data.get('identifier', None):
            data_dict['id'] = data.get('identifier', None)

        return data_dict


class JSONLDReader(TableReader):
    def parse(self) -> Dict:
        from .standard_name_table import StandardNameTable
        with open(self.filename, 'r') as f:
            import json
            snt = StandardNameTable.from_jsonld(data=json.load(f), limit=1)
            return snt.model_dump(exclude_none=True)


_plugins = {
    'xml': XMLReader,
    'text/xml': XMLReader,
    'https://www.iana.org/assignments/media-types/text/xml': XMLReader,
    'https://www.iana.org/assignments/media-types/application/xml': XMLReader,
    'yaml': YAMLReader,
    'yml': YAMLReader,
    'application/yaml': YAMLReader,
    'https://www.iana.org/assignments/media-types/application/yaml': YAMLReader,
    'jsonld': JSONLDReader,
    'application/json-ld': JSONLDReader,
    'https://www.iana.org/assignments/media-types/application/ld+json': JSONLDReader
}


def get(plugin_name: str, default=None) -> Union[TableReader, None]:
    """Returns the plugin"""
    plugin = _plugins.get(str(plugin_name), None)
    if plugin is None:
        return default
    return plugin
