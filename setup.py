# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme  =  f.read()

setup(
    name = 'bom_scraper',
    version = '0.1.0',
    description = 'BoxOfficeMojo scraper for movie pages',
    long_description = readme,
    author = 'Hyun Joon "Billy" Seol',
    author_email = 'hyunjoon.seol@gmail.com',
    url = 'https://github.com/tglstory/Box-Office-Mojo-Scrapper',
    packages = find_packages(exclude=('tests', 'docs')),
    install_requires = [
        'beautifulsoup4',
        'requests',
        's3fs',
    ],
    scripts=[
    	'bom_runner.py'
    ],
    entry_points = {
        "console_scripts": ['bom_download = bom_scraper.bom_download_html:main']
    },
    test_suite='tests',
    tests_require=[
        'beautifulsoup4'
    ]
)
