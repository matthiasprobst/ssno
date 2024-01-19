# Guide - Using sSNO ontology

The context JSON-LD file can be found
[here](https://raw.githubusercontent.com/matthiasprobst/ssno/main/ssno_context.jsonld). It should be added at the
beginning of the JSON-LD file to be validated. It contains the translation of keys to their IRIs and thereby giving
*context* to the JSON data written afterwards.

## Describe a standard name

```json
{
  "@context": {
    "@import": "https://raw.githubusercontent.com/matthiasprobst/ssno/main/ssno_context.jsonld"
  },
  "@graph": [
    {
      "@id": "_:b0",
      "@type": "StandardName",
      "standard name": "x_velocity",
      "canonical units": "m/s",
      "description": "Velocity in x-axis direction.",
      "standard name table": "https://doi.org/10.5281/zenodo.10428817"
    },
    {
      "@id": "https://doi.org/10.5281/zenodo.10428817",
      "@type": "StandardNameTable",
      "identifier": "https://doi.org/10.5281/zenodo.10428817"
    }
  ]
}
```

## Describe a standard name table

In the previous example, we used an external StandardNameTable. We can also define a table in JSON-LD file:

```json
{
  "@context": {
    "@import": "https://raw.githubusercontent.com/matthiasprobst/ssno/main/ssno_context.jsonld"
  },
  "@graph": [
    {
      "@id": "https://doi.org/10.5281/zenodo.10428817",
      "@type": "StandardNameTable",
      "doi": "https://doi.org/10.5281/zenodo.10428817",
      "title": "My Table",
      "description": "My table description",
      "standard names": [
        {
          "@id": "_:b0",
          "@type": "StandardName",
          "standard name": "x_velocity",
          "canonical units": "m/s",
          "description": "Velocity in x-axis direction.",
          "standard name table": "https://doi.org/10.5281/zenodo.10428817"
        },
        {
          "@id": "_:b1",
          "@type": "StandardName",
          "standard name": "y_velocity",
          "canonical units": "m/s",
          "description": "Velocity in y-axis direction.",
          "standard name table": "https://doi.org/10.5281/zenodo.10428817"
        }
      ]
    }
  ]
}
```