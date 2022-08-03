import setuptools
from pathlib import Path


long_description = (Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    name = 'ogameasure',
    version = "0.5.1",
    description = 'Driver for SCPI device',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/ogawa-ros/ogameasure',
    author = 'Shota Ueda',
    author_email = 's7u27astr0@gmail.com',
    license = 'MIT',
    keywords = '',
    install_requires=[
        "importlib-metadata; python_version < '3.8'",
        "numpy",
        "pyserial",
    ],
    packages = [
        'ogameasure',
        'ogameasure.communicator',
        'ogameasure.device',
        'ogameasure.device.Agilent',
        'ogameasure.device.Anritsu',
        'ogameasure.device.Pfeiffer',
        'ogameasure.device.Lakeshore',
        'ogameasure.device.SCPI',
        'ogameasure.device.ELVA1',
        'ogameasure.device.Phasematrix',
        'ogameasure.device.HEIDENHAIN',
        'ogameasure.device.KIKUSUI',
        'ogameasure.device.Canon',
        'ogameasure.device.Cosmotechs',
        'ogameasure.device.TandD',
        'ogameasure.device.SENA',
        'ogameasure.interface',
    ],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware',
    ],
)
