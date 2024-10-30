The standard name construction rules are detailed in a document associated with
the <a href="https://matthiasprobst.github.io/ssno#StandardNameTabel">StandardNameTable</a>. This table encompasses all
standard names defined by a specific project or community. Instances of StandardName and StandardNameTable can be
applied in conjunction with other ontologies, such
as <a href="https://nfdi4ing.pages.rwth-aachen.de/metadata4ing/metadata4ing/" target="_blank">metadata4ing</a>, to offer
a clear, standardized description of a numerical variable.

The following class diagram provides a brief overview of the key classes within the ontology.
<img alt="class diagram" src="https://github.com/matthiasprobst/ssno/blob/main/documentation/imgs/SSNO_VERSION/classdiagram.png?raw=true" height="300 px">

Standard names as in the CF conventions are intended to be used for describing netCDF data. In this adopted ontology
version the focus is set on HDF5 files. To specify which standard name table applies to a file, a relationship can be
established between the file and the corresponding standard name table, as illustrated below. It is also possible to
associate a standard name table in a broader context, for instance, by linking it to
a <a href="https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset" target="_blank">dcat:Dataset</a> or
a <a href="https://schema.org/Project" target="_blank">schema:Project</a>.
<img alt="class diagram" src="https://github.com/matthiasprobst/ssno/blob/main/documentation/imgs/SSNO_VERSION/things_and_snt.png?raw=true" height="150 px">

In some cases, standard names can be adapted to form new, valid names. These adaptations, managed by the standard name
table, can take the form of qualifications or transformations. Both types of modifications are describable within the
ontology. Qualification-based modifications, as specified in
the <a href="https://cfconventions.org/Data/cf-standard-names/docs/guidelines.html">CF Standard Name Guidelines</a>,
involve adding qualification phrases (represented by the
class <a href="https://matthiasprobst.github.io/ssno/#Qualification" target="_blank">ssno:Qualification</a) before or
after a core standard name. Certain qualifications may also include prepositions, such as "at" or "due to."
<img alt="class diagram" src="https://github.com/matthiasprobst/ssno/blob/main/documentation/imgs/SSNO_VERSION/standard_name_modification.png?raw=true" height="500 px">