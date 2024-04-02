"""semi manual task

1. update the ontology in versions/X.X.X/ontology.ttl
2. run widoco
3. run this script
"""
import datetime
import logging
import pathlib
import shutil
import subprocess
import sys

DEFAULT_LOGGING_LEVEL = logging.DEBUG
_formatter = logging.Formatter(
    '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d_%H:%M:%S')

_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(DEFAULT_LOGGING_LEVEL)
_stream_handler.setFormatter(_formatter)

logger = logging.getLogger('ssno')
logger.addHandler(_stream_handler)
logger.setLevel(DEFAULT_LOGGING_LEVEL)

__this_dir__ = pathlib.Path(__file__).parent


def copy_version_to_docs(version_string):
    version_path = __this_dir__ / 'docs' / version_string.strip('v')
    target_path = __this_dir__ / 'docs'

    assert version_path.exists()
    assert version_path.is_dir()

    target_path.mkdir(exist_ok=True, parents=True)

    shutil.copytree(version_path, target_path, dirs_exist_ok=True)
    index_en = target_path / 'index-en.html'
    (target_path / 'index.html').unlink(missing_ok=True)
    index_en.rename(target_path / 'index.html')
    (target_path / 'ssno.jsonld').unlink(missing_ok=True)
    (target_path / 'ssno.nt').unlink(missing_ok=True)
    (target_path / 'ssno.ttl').unlink(missing_ok=True)
    (target_path / 'ssno.owl').unlink(missing_ok=True)
    (target_path / 'ontology.jsonld').rename(target_path / 'ssno.jsonld')
    (target_path / 'ontology.nt').rename(target_path / 'ssno.nt')
    (target_path / 'ontology.ttl').rename(target_path / 'ssno.ttl')
    (target_path / 'ontology.owl').rename(target_path / 'ssno.owl')

    vers_index_en = version_path / 'index-en.html'
    assert vers_index_en.exists()
    vers_index_en.with_name('index.html').unlink(missing_ok=True)
    vers_index_en.rename(vers_index_en.with_name('index.html'))

    (version_path / 'ssno.jsonld').unlink(missing_ok=True)
    (version_path / 'ssno.nt').unlink(missing_ok=True)
    (version_path / 'ssno.ttl').unlink(missing_ok=True)
    (version_path / 'ssno.owl').unlink(missing_ok=True)
    (version_path / 'ontology.jsonld').rename(version_path / 'ssno.jsonld')
    (version_path / 'ontology.nt').rename(version_path / 'ssno.nt')
    (version_path / 'ontology.ttl').rename(version_path / 'ssno.ttl')
    (version_path / 'ontology.owl').rename(version_path / 'ssno.owl')

    assert index_en.exists() is False
    logger.debug('done copying version to docs')


def create_version(version_folder, version_string, previousVersionURI: str = None):
    assert version_string.startswith('v')
    sys.path.insert(0, '.')
    # call batch script build.bat
    logger.info('Start building docs')

    logger.debug('Running tests...')
    subprocess.run(['python', 'tests/test_graph.py'])

    logger.debug('update modification data')
    # open widoco config file
    widico_cfg_filename = version_folder / 'widoco.cfg'
    assert widico_cfg_filename.exists()

    with open(widico_cfg_filename, 'r', encoding='utf-8') as f:
        lines = [l.strip().split('=') for l in f.readlines()]

    cfg_data = {l[0]: l[1] for l in lines if len(l) == 2}
    today = datetime.datetime.today()
    # cfg_data['dateCreated'] = today.strftime('%Y-%m-%d')
    cfg_data['dateModified'] = today.strftime('%Y-%m-%d')
    cfg_data['ontologyRevisionNumber'] = version_string
    if previousVersionURI:
        cfg_data['previousVersionURI'] = previousVersionURI

    def read_lines(filename) -> str:
        with open(filename, encoding='utf-8') as f:
            lines = f.readlines()
            return '<br>'.join([l.strip() for l in lines])

    cfg_data['abstract'] = read_lines(__this_dir__ / 'documentation' / 'Abstract.md')
    cfg_data['introduction'] = read_lines(__this_dir__ / 'documentation' / 'Introduction.md')
    cfg_data['description'] = read_lines(__this_dir__ / 'documentation' / 'Description.md')
    cfg_data['thisVersionURI'] = f'https://matthiasprobst.github.io/ssno/{version_string.strip("v")}'
    cfg_data['authors'] = 'Matthias Probst (https://orcid.org/0000-0001-8729-0482), Karlsruher Institut ' \
                          'für Technologie, Institut für Thermische Strömungsmaschinen'

    cfg_data['citeAs'] = 'Matthias Probst (https://orcid.org/0000-0001-8729-0482), Karlsruher Institut ' \
                         'für Technologie, Institut für Thermische Strömungsmaschinen. SSNO: A simple Standard ' \
                         f'Name Ontology. Revision: {version_string}. Retrieved from: ' \
                         f'https://matthiasprobst.github.io/ssno/{version_string.strip("v")}'

    with open(widico_cfg_filename, 'w', encoding='utf-8') as f:
        for k, v in cfg_data.items():
            f.write(f'\n{k}={v}')

    script_path = __this_dir__ / 'build_onto_doc.bat'
    logger.debug(f'calling script {script_path.absolute()}')
    # open script and replace <version> with version_string
    with open(script_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [l.replace('<version>', version_string.strip('v')) for l in lines]

    # write script to file
    script_path_vers = __this_dir__ / 'build_onto_doc_tmp.bat'
    with open(script_path_vers, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    subprocess.run(str(script_path_vers.absolute()))

    from generate_context import generate

    generate(version_folder / 'ssno.ttl')

    copy_version_to_docs(version_string)

    logger.info('Finished building docs')


if __name__ == "__main__":
    # # get ttl files from version/ folder
    # version_dir = __this_dir__ / 'versions'
    # for vers_folder in version_dir.glob('*'):
    #     version_string = vers_folder.name
    #     assert version_string.startswith('v')
    #     print(f'Processing version "{version_string}"')
    create_version(__this_dir__, 'v1.0.0', previousVersionURI=None)
    create_version(__this_dir__, 'v1.1.0', previousVersionURI='https://matthiasprobst.github.io/ssno/1.0.0')
