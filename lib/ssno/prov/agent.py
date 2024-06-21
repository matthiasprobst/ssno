from typing import Union

from pydantic import EmailStr, HttpUrl, Field

from ontolutils import Thing, namespaces, urirefs


@namespaces(prov="http://www.w3.org/ns/prov#",
            foaf="http://xmlns.com/foaf/0.1/")
@urirefs(Agent='prov:Agent',
         mbox='foaf:mbox')
class Agent(Thing):
    """Pydantic Model for http://www.w3.org/ns/prov#Agent

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    mbox: EmailStr = None
        Email address (foaf:mbox)
    """
    mbox: EmailStr = None  # foaf:mbox

    # def _repr_html_(self) -> str:
    #     """Returns the HTML representation of the class"""
    #     return f"{self.__class__.__name__}({self.mbox})"


@namespaces(schema='https://schema.org/',
            foaf='http://xmlns.com/foaf/0.1/',
            m4i='http://w3id.org/nfdi4ing/metadata4ing#',
            prov='http://www.w3.org/ns/prov#')
@urirefs(Organization='prov:Organization',
         name='foaf:name',
         url='schema:url',
         ror_id='m4i:hasRorId')
class Organization(Agent):
    """Pydantic Model for http://www.w3.org/ns/prov#Organization

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    name: str
        Name of the Organization (foaf:name)
    url: HttpUrl = None
        URL of the item. From schema:url.
    ror_id: HttpUrl
        A Research Organization Registry identifier, that points to a research organization
    """
    name: str  # foaf:name
    url: HttpUrl = None
    ror_id: HttpUrl = Field(alias="hasRorId", default=None)


@namespaces(prov="http://www.w3.org/ns/prov#",
            foaf="http://xmlns.com/foaf/0.1/",
            m4i='http://w3id.org/nfdi4ing/metadata4ing#',
            schema="https://schema.org/")
@urirefs(Person='prov:Person',
         first_name='foaf:firstName',
         last_name='foaf:lastName',
         orcid_id='m4i:orcidId',
         had_role='prov:hadRole',
         was_role_in='prov:wasRoleIn',
         affiliation='schema:affiliation')
class Person(Agent):
    """Pydantic Model for http://www.w3.org/ns/prov#Person

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    first_name: str = None
        First name (foaf:firstName)
    last_name: str = None
        Last name (foaf:lastName)
    orcid_id: str = None
        ORCID ID of person (m4i:orcidID)
    had_role: HttpUrl
        prov:hadRole references the Role (i.e. the function of an entity with respect to an activity)
    was_role_in: HttpUrl
        prov:wasRoleIn references the association (e.g. between an agent and an activity) in which a role shall be defined. Inverse property of prov:hadRole.

    Extra fields are possible but not explicitly defined here.
    """
    first_name: str = Field(default=None, alias="firstName")  # foaf:first_name
    last_name: str = Field(default=None, alias="lastName")  # foaf:last_name
    orcid_id: str = Field(default=None, alias="orcidID")  # m4i:orcidID
    had_role: HttpUrl = Field(default=None, alias="hadRole")  # m4i:hadRole
    was_role_in: Union[HttpUrl, str, Thing] = Field(default=None, alias="wasRoleIn")  # m4i:wasRoleIn
    affiliation: Organization = Field(default=None, alias="affiliation")  # schema:affiliation
