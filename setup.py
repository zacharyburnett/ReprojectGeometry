import logging
import re
import subprocess
import sys

from setuptools import config, find_packages, setup


def installed_packages() -> [str]:
    return [
        re.split('#egg=', re.split('==| @ ', package.decode())[0])[
            -1].lower()
        for package in subprocess.run(
            f'{sys.executable} -m pip freeze', shell=True,
            capture_output=True,
        ).stdout.splitlines()
    ]


try:
    if 'dunamai' not in installed_packages():
        subprocess.run(
            f'{sys.executable} -m pip install dunamai',
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    from dunamai import Version

    version = Version.from_any_vcs().serialize()
except RuntimeError as error:
    logging.exception(error)
    version = '0.0.0'

logging.info(f'using version {version}')

metadata = config.read_configuration('setup.cfg')['metadata']

setup(
    name=metadata['name'],
    version=version,
    author=metadata['author'],
    author_email=metadata['author_email'],
    description=metadata['description'],
    long_description=metadata['long_description'],
    long_description_content_type='text/markdown',
    url=metadata['url'],
    packages=find_packages(),
    python_requires='>=3.6',
    setup_requires=['dunamai', 'setuptools>=41.2'],
    install_requires=['numpy', 'pyproj>2.6', 'shapely'],
    extras_require={
        'testing': ['pytest', 'pytest-xdist'],
        'development': ['flake8', 'isort', 'oitnb'],
    },
)
