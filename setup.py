import setuptools

setuptools.setup(
    name = 'ogameasure',
    version = __import__('ogameasure').__version__,
    description = 'driver for SCPI device',
    url = 'https://github.com/ogawa-ros/ogameasure',
    author = 'Shota Ueda',
    author_email = 's7u27astr0@gmail.com',
    license = 'MIT',
    keywords = '',
    packages = [
        'ogameasure',
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
