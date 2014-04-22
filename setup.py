#!/usr/bin/env python
from setuptools import setup

setup  (
    name        = 'sic_assembler',
    version     = '1.0.0',
    description = 'A mult- pass SIC/XE assembler',
    author = 'Travis Cunningham',
    author_email = 'travcunn@umail.iu.edu',
    url = 'https://github.com/travcunn/sic_assembler',
    license = 'MIT',
    packages  =  ['sic_assembler'],
    package_dir = {'sic_assembler' : 'sic_assembler'},
    entry_points = {
        'console_scripts': [
            'sic-assembler = sic_assembler.__init__:main',
        ],
    },
)
