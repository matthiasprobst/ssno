"""Implementation of classes
- dcat:Resource
- dcat:Distribution
- dcat:Dataset
"""
import pathlib
import re
import shutil
from datetime import datetime
from typing import Union, List

import pydantic
from dateutil import parser
from pydantic import HttpUrl, FileUrl, field_validator, Field

from ontolutils import Thing
from ontolutils import urirefs, namespaces
from ..prov import Person, Organization, Agent
from ..utils import download_file


@namespaces(dcat="http://www.w3.org/ns/dcat#",
            dcterms="http://purl.org/dc/terms/", )
@urirefs(Resource='dcat:Resource',
         title='dcterms:title',
         description='dcterms:description',
         creator='dcterms:creator',
         version='dcat:version',
         identifier='dcterms:identifier')
class Resource(Thing):
    """Pdyantic implementation of dcat:Resource

    .. note::

        More than the below parameters are possible but not explicitly defined here.



    Parameters
    ----------
    title: str
        Title of the resource (dcterms:title)
    description: str = None
        Description of the resource (dcterms:description)
    creator: Union[Person, Organization] = None
        Creator of the resource (dcterms:creator)
    version: str = None
        Version of the resource (dcat:version),
        best following semantic versioning (https://semver.org/lang/de/)
    """
    title: str = None  # dcterms:title
    description: str = None  # dcterms:description
    creator: Union[Person, Organization] = None  # dcterms:creator
    version: str = None  # dcat:version
    identifier: HttpUrl = None  # dcterms:identifier

    @field_validator('creator', mode='before')
    @classmethod
    def _parse_creator(cls, creator):
        # check if creator is a valid person or oragnisation. if both fail, just pass creator data, it will fail later
        is_person = False
        is_organisation = False
        try:
            person = Person.model_validate(creator, strict=True)
            is_person = True
        except pydantic.ValidationError:
            pass
            # not a person
        try:
            organisation = Organization.model_validate(creator, strict=True)
            is_organisation = True
        except pydantic.ValidationError:
            # not an organisation
            pass
        if is_person and is_organisation:
            return creator  # cannot distinguish between person and organisation
        if is_person:
            return person
        if is_organisation:
            return organisation
        return creator


@namespaces(dcat="http://www.w3.org/ns/dcat#")
@urirefs(Distribution='dcat:Distribution',
         download_URL='dcat:downloadURL',
         access_URL='dcat:accessURL',
         media_type='dcat:mediaType',
         byte_size='dcat:byteSize',
         keyword='dcat:keyword')
class Distribution(Resource):
    """Implementation of dcat:Distribution

    .. note::
        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    download_URL: Union[HttpUrl, FileUrl]
        Download URL of the distribution (dcat:downloadURL)
    media_type: HttpUrl = None
        Media type of the distribution (dcat:mediaType).
        Should be defined by the [IANA Media Types registry](https://www.iana.org/assignments/media-types/media-types.xhtml)
    byte_size: int = None
        Size of the distribution in bytes (dcat:byteSize)
    keyword: List[str]
        Keywords for the distribution.
    """
    download_URL: Union[HttpUrl, FileUrl, pathlib.Path] = Field(default=None, alias='downloadURL')
    access_URL: Union[HttpUrl, FileUrl, pathlib.Path] = Field(default=None, alias='accessURL')
    media_type: HttpUrl = Field(default=None, alias='mediaType')  # dcat:mediaType
    byte_size: int = Field(default=None, alias='byteSize')  # dcat:byteSize
    keyword: List[str] = None  # dcat:keyword

    def _repr_html_(self):
        """Returns the HTML representation of the class"""
        if self.download_URL is not None:
            return f"{self.__class__.__name__}({self.download_URL})"
        return super()._repr_html_()

    def download(self,
                 dest_filename: Union[str, pathlib.Path] = None,
                 overwrite_existing: bool = False,
                 **kwargs) -> pathlib.Path:
        """Downloads the distribution
        kwargs are passed to the download_file function, which goes to requests.get()"""

        if self.download_URL is None:
            raise ValueError('The downloadURL is not defined')

        def _parse_file_url(furl):
            """in windows, we might need to strip the leading slash"""
            fname = pathlib.Path(furl)
            if fname.exists():
                return fname
            fname = pathlib.Path(self.download_URL.path[1:])
            if fname.exists():
                return fname
            raise FileNotFoundError(f'File {self.download_URL.path} does not exist')

        if self.download_URL.scheme == 'file':
            if dest_filename is None:
                return _parse_file_url(self.download_URL.path)
            else:
                return shutil.copy(_parse_file_url(self.download_URL.path), dest_filename)
        dest_filename = pathlib.Path(dest_filename or self.download_URL.path.split('/')[-1])
        if dest_filename.exists():
            return dest_filename
        return download_file(self.download_URL,
                             dest_filename,
                             overwrite_existing=overwrite_existing,
                             **kwargs)

    @field_validator('media_type', mode='before')
    @classmethod
    def _mediaType(cls, mediaType):
        """should be a valid URI, like: https://www.iana.org/assignments/media-types/text/markdown"""
        if isinstance(mediaType, str):
            if mediaType.startswith('http'):
                return HttpUrl(mediaType)
            elif mediaType.startswith('iana:'):
                return HttpUrl("https://www.iana.org/assignments/media-types/" + mediaType.split(":", 1)[-1])
            elif re.match('[a-z].*/[a-z].*', mediaType):
                return HttpUrl("https://www.iana.org/assignments/media-types/" + mediaType)
        return mediaType

    @field_validator('download_URL', mode='before')
    @classmethod
    def _downloadURL(cls, downloadURL):
        """a pathlib.Path is also allowed but needs to be converted to a URL"""
        if isinstance(downloadURL, pathlib.Path):
            return FileUrl(f'file://{downloadURL.resolve().absolute()}')
        return downloadURL


@namespaces(dcat="http://www.w3.org/ns/dcat#")
@urirefs(DatasetSeries='dcat:DatasetSeries')
class DatasetSeries(Resource):
    """Pydantic implementation of dcat:DatasetSeries"""


@namespaces(dcat="http://www.w3.org/ns/dcat#",
            prov="http://www.w3.org/ns/prov#",
            dcterms="http://purl.org/dc/terms/")
@urirefs(Dataset='dcat:Dataset',
         identifier='dcterms:identifier',
         creator='dcterms:creator',
         distribution='dcat:distribution',
         modified='dcterms:modified',
         landing_page='dcat:landingPage',
         in_series='dcat:inSeries')
class Dataset(Resource):
    """Pydantic implementation of dcat:Dataset

    .. note::

        More than the below parameters are possible but not explicitly defined here.



    Parameters
    ----------
    title: str
        Title of the resource (dcterms:title)
    description: str = None
        Description of the resource (dcterms:description)
    creator: Agent = None
        Creator of the resource (dcterms:creator)
    version: str = None
        Version of the resource (dcat:version)
    identifier: HttpUrl = None
        Identifier of the resource (dcterms:identifier)
    creator: Union[Person, Organization] = None  # dcterms:creator
        Contact person or Organization of the resource (http://www.w3.org/ns/prov#Person)
    distribution: List[Distribution] = None
        Distribution of the resource (dcat:Distribution)
    landing_page: HttpUrl = None
        Landing page of the resource (dcat:landingPage)
    modified: datetime = None
        Last modified date of the resource (dcterms:modified)
    in_series: DatasetSeries = None
        The series the dataset belongs to (dcat:inSeries)
    """
    identifier: HttpUrl = None  # dcterms:identifier, see https://www.w3.org/TR/vocab-dcat-3/#ex-identifier
    # http://www.w3.org/ns/prov#Person, see https://www.w3.org/TR/vocab-dcat-3/#ex-adms-identifier
    creator: Agent = None
    distribution: Union[Distribution, List[Distribution]] = None  # dcat:Distribution
    modified: datetime = None  # dcterms:modified
    landing_page: HttpUrl = Field(default=None, alias='landingPage')  # dcat:landingPage
    in_series: DatasetSeries = Field(default=None, alias='inSeries')  # dcat:inSeries

    @field_validator('distribution', mode='before')
    @classmethod
    def _distribution(cls, distribution):
        if not isinstance(distribution, list):
            return [distribution]
        return distribution
        # def _parse_dist(_dist):
        #     if isinstance(_dist, str):
        #         return Distribution(id=_dist)
        #     return _dist
        #
        # if isinstance(distribution, list):
        #     return [_parse_dist(_dist) for _dist in distribution]
        # return _parse_dist(distribution)

    @field_validator('modified', mode='before')
    @classmethod
    def _modified(cls, modified):
        """parse datetime"""
        if isinstance(modified, str):
            return parser.parse(modified)
        return modified
