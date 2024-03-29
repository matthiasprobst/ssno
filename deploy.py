"""semi manual task

1. update the ontology in versions/X.X.X/ontology.ttl
2. run widoco
3. run this script
"""
import configparser
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


def copy_version_to_docs():
    version_path = __this_dir__ / 'docs/versions' / '1.0.0'
    target_path = __this_dir__ / 'docs'

    assert version_path.exists()
    assert version_path.is_dir()

    target_path.mkdir(exist_ok=True, parents=True)

    shutil.copytree(version_path, target_path, dirs_exist_ok=True)
    index_en = target_path / 'index-en.html'
    (target_path / 'index.html').unlink(missing_ok=True)
    index_en.rename(target_path / 'index.html')
    assert index_en.exists() is False
    logger.debug('done copying version to docs')


if __name__ == "__main__":

    sys.path.insert(0, '.')
    # call batch script build.bat
    logger.info('Start building docs')

    logger.debug('Running tests...')
    subprocess.run(['python', 'tests/test_graph.py'])

    logger.debug('update modification data')
    # open widoco config file
    cfg_file = __this_dir__ / 'widoco.cfg'
    config = configparser.ConfigParser()
    with open('widoco.cfg', 'r') as f:
        lines = [l.strip().split('=') for l in f.readlines()]

    cfg_data = {l[0]: l[1] for l in lines if len(l) == 2}
    today = datetime.datetime.today()
    cfg_data['dateModified'] = today.strftime('%Y-%m-%d')

    with open(cfg_file, 'w') as f:
        for k, v in cfg_data.items():
            f.write(f'\n{k}={v}')
    script_path = __this_dir__ / 'build_onto_doc.bat'
    logger.debug(f'calling script {script_path.absolute()}')
    subprocess.run(str(script_path.absolute()))

    from generate_context import generate

    generate()
    copy_version_to_docs()

    logger.info('Finished building docs')
