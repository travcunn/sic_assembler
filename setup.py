#!/usr/bin/env python
from setuptools import setup, find_packages

setup  (
    name        = 'sic_assembler',
    version     = '0.0.1',
    description = 'A 2 pass SIC/XE assembler',
    author = 'Travis Cunningham',
    author_email = 'travcunn@umail.iu.edu',
    url = 'https://github.com/travcunn/sic_assembler',
    license = 'MIT',
    packages  =  find_packages('src'),
    package_dir = {'' : 'src'},
    entry_points = {
        'console_scripts': [
            'sic-assembler = sic_assembler.__init__:main',
        ],
    },
)
