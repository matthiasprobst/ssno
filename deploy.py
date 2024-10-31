"""semi manual task

Running this script will create a the documentation for a new version of the ontology.

So first change the ttl file with Protege (), then change the version string in this script
(see in bottom of the script) and then run the script.
"""
import datetime
import logging
import pathlib
import re
import shutil
import subprocess
import sys
from typing import Optional, Dict

ONTOLOGY_NAME = 'ssno'

DEFAULT_LOGGING_LEVEL = logging.DEBUG
_formatter = logging.Formatter(
    '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d_%H:%M:%S')

_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(DEFAULT_LOGGING_LEVEL)
_stream_handler.setFormatter(_formatter)

logger = logging.getLogger(f'{ONTOLOGY_NAME}')
logger.addHandler(_stream_handler)
logger.setLevel(DEFAULT_LOGGING_LEVEL)

__this_dir__ = pathlib.Path(__file__).parent


def bugfix_index_html(filename):
    tmp_filename = filename.with_suffix('.html_tmp')
    tmp_filename.unlink(missing_ok=True)
    with open(filename, "r", encoding='utf-8') as f:
        with open(tmp_filename, "w", encoding='utf-8') as f_out:
            for line in f.readlines():
                if 'metadata4ing' in line:
                    f_out.write(line.replace(
                        '<tr><td><b>metadata4ing</b></td><td>',
                        '<tr><td><b>m4i</b></td><td>'))
                elif '.after(marked.parse(jQuery' in line:
                    f_out.write(line.replace(
                        '.after(marked.parse(jQuery',
                        '.after(marked(jQuery'))
                else:
                    f_out.write(line)
    filename.unlink(missing_ok=True)
    tmp_filename.rename(filename)


def copy_version_to_docs(version_string):
    version_path = __this_dir__ / 'docs' / version_string.strip('v')
    target_path = __this_dir__ / 'docs'

    assert version_path.exists(), f'Version path {version_path} does not exist'
    assert version_path.is_dir(), f'Version path {version_path} is not a directory'

    target_path.mkdir(exist_ok=True, parents=True)

    shutil.copytree(version_path, target_path, dirs_exist_ok=True)
    index_en = target_path / 'index-en.html'
    (target_path / 'index.html').unlink(missing_ok=True)
    index_en.rename(target_path / 'index.html')
    (target_path / f'{ONTOLOGY_NAME}.jsonld').unlink(missing_ok=True)
    (target_path / f'{ONTOLOGY_NAME}.nt').unlink(missing_ok=True)
    (target_path / f'{ONTOLOGY_NAME}.ttl').unlink(missing_ok=True)
    (target_path / f'{ONTOLOGY_NAME}.owl').unlink(missing_ok=True)
    (target_path / 'ontology.jsonld').rename(target_path / f'{ONTOLOGY_NAME}.jsonld')
    (target_path / 'ontology.nt').rename(target_path / f'{ONTOLOGY_NAME}.nt')
    (target_path / 'ontology.ttl').rename(target_path / f'{ONTOLOGY_NAME}.ttl')
    (target_path / 'ontology.owl').rename(target_path / f'{ONTOLOGY_NAME}.owl')

    vers_index_en = version_path / 'index-en.html'
    assert vers_index_en.exists()
    vers_index_en.with_name('index.html').unlink(missing_ok=True)
    vers_index_en.rename(vers_index_en.with_name('index.html'))

    (version_path / f'{ONTOLOGY_NAME}.jsonld').unlink(missing_ok=True)
    (version_path / f'{ONTOLOGY_NAME}.nt').unlink(missing_ok=True)
    (version_path / f'{ONTOLOGY_NAME}.ttl').unlink(missing_ok=True)
    (version_path / f'{ONTOLOGY_NAME}.owl').unlink(missing_ok=True)
    (version_path / 'ontology.jsonld').rename(version_path / f'{ONTOLOGY_NAME}.jsonld')
    (version_path / 'ontology.nt').rename(version_path / f'{ONTOLOGY_NAME}.nt')
    (version_path / 'ontology.ttl').rename(version_path / f'{ONTOLOGY_NAME}.ttl')
    (version_path / 'ontology.owl').rename(version_path / f'{ONTOLOGY_NAME}.owl')

    assert index_en.exists() is False

    bugfix_index_html(version_path / 'index.html')
    bugfix_index_html(__this_dir__ / 'docs' / 'index.html')

    logger.debug('done copying version to docs')


def create_version(*,
                   widico_cfg_filename,
                   ttl_filename: pathlib.Path,
                   version_string: str,
                   doi_url: str,
                   previous_version_string: str = None,
                   img_version_string: str = None):
    assert version_string.startswith('v')
    if img_version_string is None:
        img_version_string = version_string
    sys.path.insert(0, '.')
    # call batch script build.bat
    logger.info('Start building docs')

    logger.debug('Running tests...')
    subprocess.run(['python', 'tests/test_graph.py'])

    logger.debug('update modification data')
    # open widoco config file
    # widico_cfg_filename = version_folder / 'widoco.cfg'
    assert widico_cfg_filename.exists()

    with open(widico_cfg_filename, 'r', encoding='utf-8') as f:
        lines = [l.strip().split('=') for l in f.readlines()]

    cfg_data = {l[0]: l[1] for l in lines if len(l) == 2}
    today = datetime.datetime.today()
    # cfg_data['dateCreated'] = today.strftime('%Y-%m-%d')
    cfg_data['dateModified'] = today.strftime('%Y-%m-%d')
    cfg_data['dateIssued'] = today.strftime('%Y-%m-%d')
    cfg_data['ontologyRevisionNumber'] = version_string

    this_version_uri = f'https://matthiasprobst.github.io/{ONTOLOGY_NAME}/{version_string.strip("v")}'
    latest_version_uri = this_version_uri

    cfg_data['latestVersionURI'] = latest_version_uri
    if previous_version_string:
        prev_version_uri = f'https://matthiasprobst.github.io/{ONTOLOGY_NAME}/{previous_version_string.strip("v")}'
        cfg_data['previousVersionURI'] = prev_version_uri

    def read_lines(filename, replace_dict: Optional[Dict] = None) -> str:
        replace_dict = replace_dict or {}
        with open(filename, encoding='utf-8') as f:
            lines = f.readlines()
            for k, v in replace_dict.items():
                lines = [l.replace(k, v) for l in lines]
            return '<br>'.join([l.strip() for l in lines])

    cfg_data['abstract'] = read_lines(__this_dir__ / 'documentation' / 'Abstract.md')
    cfg_data['introduction'] = read_lines(__this_dir__ / 'documentation' / 'Introduction.md',
                                          replace_dict={"SSNO_VERSION": img_version_string.strip("v")})
    cfg_data['description'] = read_lines(__this_dir__ / 'documentation' / 'Description.md',
                                         replace_dict={"SSNO_VERSION": img_version_string.strip("v")})

    cfg_data['thisVersionURI'] = this_version_uri
    cfg_data['authors'] = 'Matthias Probst (https://orcid.org/0000-0001-8729-0482), Karlsruhe Institute ' \
                          'of Technology, Institute of Thermal Turbomachinery'

    cfg_data['citeAs'] = 'Matthias Probst (https://orcid.org/0000-0001-8729-0482), Karlsruher Institute ' \
                         f'of Technology, Institute of Thermal Turbomachinery. {ONTOLOGY_NAME}: A simple Standard ' \
                         f'Name Ontology. Revision: {version_string}. Retrieved from: ' \
                         f'https://matthiasprobst.github.io/{ONTOLOGY_NAME}/{version_string.strip("v")}'
    cfg_data['DOI'] = doi_url

    with open(widico_cfg_filename, 'w', encoding='utf-8') as f:
        for k, v in cfg_data.items():
            f.write(f'\n{k}={v}')

    logger.debug(f'Updating version in ttl file')
    shutil.copy(ttl_filename, ttl_filename.with_suffix('.bak'))
    with open(ttl_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, l in enumerate(lines):
            if 'owl:versionInfo' in l:
                _splitted_line = l.split('owl:versionInfo', 1)
                _new_line = f"{_splitted_line[0]}owl:versionInfo \"{version_string}\" .\n"
                lines[i] = _new_line
            elif 'owl:versionIRI' in l:
                _splitted_line = l.split('owl:versionIRI', 1)
                _new_line = f"{_splitted_line[0]}owl:versionIRI <https://matthiasprobst.github.io/ssno/{version_string.strip('v')}> ;\n"
                lines[i] = _new_line
    with open(ttl_filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    script_path = __this_dir__ / 'build_onto_doc.bat'
    # open script and replace <version> with version_string
    with open(script_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [l.replace('<version>', version_string.strip('v')) for l in lines]

    logger.debug(f'calling script {script_path.absolute()}')
    # write script to file
    script_path_vers = __this_dir__ / 'build_onto_doc_tmp.bat'
    with open(script_path_vers, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    r = subprocess.run(str(script_path_vers.absolute()))
    assert r.returncode == 0, f'Error running script {script_path_vers}.'

    from generate_context import generate

    generate(ttl_filename)

    copy_version_to_docs(version_string)

    script_path_vers.unlink()

    # now go through all versions in docs/ and update the latest version URL:
    docs_path = __this_dir__ / 'docs'
    for d in docs_path.iterdir():
        if d.is_dir():
            if re.match(r'^\d+(\.\d+)*$', d.name):
                html_filename = d / 'index.html'
                html_filename.exists()
                with open(html_filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                for i, l in enumerate(lines):
                    if '<dt>Latest version:</dt>' in l:
                        lines[
                            i + 1] = f'            <dd><a href="https://matthiasprobst.github.io/ssno">https://matthiasprobst.github.io/ssno/{version_string.strip("v")}</a></dd>\n'
                with open(html_filename, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
    logger.info('Finished building docs')


if __name__ == "__main__":
    prev_version_string = 'v1.2.1'
    version_string = 'v1.3.0'
    img_version_string = 'v1.3.0'
    doi_url = "https://doi.org/10.5281/zenodo.13351343"
    overwrite = True

    version_dir = __this_dir__ / 'docs' / version_string.strip('v')
    if version_dir.exists():
        if overwrite:
            shutil.rmtree(version_dir)
        else:
            raise ValueError(f'Version {version_dir} already exists. You might be about to create '
                             f'a new version. Please provide a new version number if something has changed!.')

    create_version(
        widico_cfg_filename=__this_dir__ / 'widoco.cfg',
        ttl_filename=__this_dir__ / f'{ONTOLOGY_NAME}.ttl',
        version_string=version_string,
        previous_version_string=prev_version_string,
        img_version_string=img_version_string,
        doi_url=doi_url)
