import warnings
from ontolutils import namespaces, urirefs, parse_unit
from pydantic import HttpUrl, field_validator, Field
from typing import Union

from ..dcat import Dataset
from ..skos import Concept


@namespaces(ssno="https://matthiasprobst.github.io/ssno#",
            dcat="http://www.w3.org/ns/dcat#")
@urirefs(StandardName='ssno:StandardName',
         canonical_units='ssno:canonicalUnits',
         standard_name='ssno:standardName',
         description='ssno:description',
         standard_name_table='ssno:standardNameTable')
class StandardName(Concept):
    """Implementation of ssno:StandardName"""
    canonical_units: str = Field(default=None, alias="canonicalUnits")
    standard_name: str = Field(default=None, alias="standardName")
    description: str = None  # ssno:description
    standard_name_table: Dataset = Field(default=None, alias="standardNameTable")

    @field_validator("standard_name_table", mode='before')
    @classmethod
    def _parse_standard_name_table(cls, standard_name_table: Union[Dataset, str]) -> Dataset:
        """Parse the standard_name_table and return the standard_name_table as Dataset."""
        if isinstance(standard_name_table, Dataset):
            return standard_name_table
        raise TypeError(f"Expected a Dataset, got {type(standard_name_table)}")

    @field_validator("canonical_units", mode='before')
    @classmethod
    def _parse_unit(cls, canonical_units: Union[HttpUrl, str]) -> str:
        """Parse the canonical_units and return the canonical_units as string."""
        if canonical_units is None:
            return parse_unit('dimensionless')
        if isinstance(canonical_units, str):
            if canonical_units.startswith('http'):
                return str(HttpUrl(canonical_units))
            try:
                return str(parse_unit(canonical_units))
            except KeyError:
                warnings.warn(f'Could not parse canonical_units: "{canonical_units}".', UserWarning)
            return str(canonical_units)
        return str(HttpUrl(canonical_units))
