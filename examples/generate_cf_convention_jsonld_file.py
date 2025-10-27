import ssnolib
from ssnolib import StandardNameTable
from ssnolib.dcat import Distribution


def generate():
    distribution = Distribution(
        title='XML Table',
        downloadURL='https://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml',
        mediaType='application/xml'
    )
    snt = ssnolib.StandardNameTable(
        id="_:standard_name_table_v79",
        title='CF Standard Name Table (latest version)',
        distribution=distribution
    )

    with open('cf.json', 'w') as f:
        f.write(snt.model_dump_jsonld(base_uri="https://local.org#"))

    download_filename = distribution.download('cf-standard-name-table.xml')

    snt_from_xml = snt.parse(download_filename, fmt='xml', make_standard_names_lowercase=True)
    print(snt_from_xml.standard_names[:5])


if __name__ == '__main__':
    generate()
