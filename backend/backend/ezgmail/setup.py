"""Setup file for the whole project.

For now, this file only contain the setup for ezgmail.
We can add more modules in the future as need.
"""
import re
from setuptools import setup, find_packages

setup(
    name='EZGmail',
    url='https://github.com/asweigart/ezgmail',
    author='Al Sweigart',
    author_email='al@inventwithpython.com',
    license='GPLv3+',
    packages=find_packages(where='ezgmail'),
    package_dir={'': '.'},
    test_suite='tests',
    install_requires=['google-api-python-client', 'oauth2client'],
    keywords='',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)