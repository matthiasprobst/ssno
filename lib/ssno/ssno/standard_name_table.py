import pathlib
from typing import List, Union, Dict

from ontolutils import namespaces, urirefs, Thing
from pydantic import field_validator, Field

from . import plugins
from .standard_name import StandardName
from ..dcat import Dataset, Distribution
from ..prov import Person, Organization


@namespaces(ssno="https://matthiasprobst.github.io/ssno#",
            schema="http://schema.org/",
            dcterms="http://purl.org/dc/terms/")
@urirefs(Qualification='ssno:Qualification',
         name='schema:name',
         description='dcterms:description')
class Qualification(Thing):
    """Implementation of ssno:Qualification"""

    name: str  # schema:name
    description: str  # dcterms:description

    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.name}")'


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Medium='ssno:Medium')
class Medium(Qualification):
    """Implementation of ssno:Medium"""

    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.name}")'


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Location='ssno:Location')
class Location(Qualification):
    """Implementation of ssno:Location"""

    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.name}")'


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Device='ssno:Device')
class Device(Qualification):
    """Implementation of ssno:Device"""

    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.name}")'


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Condition='ssno:Condition')
class Condition(Qualification):
    """Implementation of ssno:Condition"""

    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.name}")'


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Component='ssno:Component')
class Component(Qualification):
    """Implementation of ssno:Component"""

    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.name}")'


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(ReferenceFrame='ssno:ReferenceFrame')
class ReferenceFrame(Qualification):
    """Implementation of ssno:ReferenceFrame"""

    components: List[Component]

    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.name}")'


@namespaces(ssno="https://matthiasprobst.github.io/ssno#",
            dcterms="http://purl.org/dc/terms/")
@urirefs(StandardNameTable='ssno:StandardNameTable',
         creator='dcterms:creator',
         standard_names='ssno:standardNames',
         locations='ssno:locations',
         devices='ssno:devices',
         media='ssno:media',
         conditions='ssno:conditions',
         reference_frames='ssno:referenceFrames',
         )
class StandardNameTable(Dataset):
    """Implementation of ssno:StandardNameTable

    Parameters
    ----------
    title: str
        Title of the Standard Name Table (dcterms:title)
    description: str
        Description of the Standard Name Table (dcterms:description)
    creator: Union[Person, List[Person], Organization, List[Organization]]
        Creator of the SNT (dcterms:creator)
    version: str
        Version of the Standard Name Table (dcat:version)
    identifier: str
        Identifier of the Standard Name Table, e.g. the DOI (dcterms:identifier)
    standard_names: List[StandardName]
        List of Standard Names (ssno:standardNames)
    locations: List[Location]
        List of Locations (ssno:locations)
    devices: List[Device]
        List of Devices (ssno:devices)
    media: List[Medium]
        List of Media (ssno:media)
    conditions: List[Condition]
        List of Conditions (ssno:conditions)
    reference_frames: List[ReferenceFrame]
        List of Reference Frames (ssno:referenceFrames)

    """
    title: str = None
    version: str = None
    description: str = None
    identifier: str = None
    creator: Union[Person, List[Person], Organization, List[Organization]] = None
    standard_names: List[StandardName] = Field(default=None, alias="standardNames")  # ssno:standardNames
    locations: List[Location] = None
    devices: List[Device] = None
    media: List[Medium] = None
    conditions: List[Condition] = None
    reference_frames: List[ReferenceFrame] = None

    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.title}")'

    @classmethod
    def parse(cls,
              source: Union[str, pathlib.Path, Distribution],
              fmt: str = None):
        """Call the reader plugin for the given format.
        Format will select the reader plugin to use. Currently, 'xml' is supported."""
        if isinstance(source, (str, pathlib.Path)):
            filename = source
            if fmt is None:
                filename = source
                fmt = pathlib.Path(source).suffix[1:].lower()
        else:
            if fmt is None:
                fmt = source.media_type
            filename = source.download()
        reader = plugins.get(fmt, None)
        if reader is None:
            raise ValueError(
                f'No plugin found for the file. The reader was determined based on the suffix: {fmt}. '
                'You may overwrite this by providing the parameter fmt'
            )

        data: Dict = reader(filename).parse()

        return cls(**data)

    @field_validator('standard_names')
    @classmethod
    def _standard_names(cls, standard_names: Union[StandardName, List[StandardName]]) -> List[StandardName]:
        if not isinstance(standard_names, list):
            return [standard_names]
        return standard_names

    def get_standard_name(self, standard_name: str) -> Union[StandardName, None]:
        """Check if the Standard Name Table has a given standard name. The
        standard name object is returned if found, otherwise None.

        Parameters
        ----------
        standard_name: str
            The standard name to look for

        Returns
        -------
        Union[StandardName, None]
            The standard name object if found, otherwise None
        """
        for sn in self.standard_names:
            if sn.standard_name == standard_name:
                return sn
        return
