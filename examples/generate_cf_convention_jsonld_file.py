from pivmetalib.ssno import StandardNameTable
from pivmetalib.utils import download_file

def generate():
    cf_contention = 'http://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml'
    snt_xml_filename = download_file(cf_contention, dest_filename='snt.xml')
    xml_snt = StandardNameTable.parse(snt_xml_filename, fmt=None)

    with open('cf.json', 'w') as f:
        f.write(xml_snt.model_dump_jsonld())


if __name__ == '__main__':
    generate()