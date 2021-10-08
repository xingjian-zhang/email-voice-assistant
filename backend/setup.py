"""Backend python package configuration."""

from setuptools import find_packages, setup

setup(
    name='backend',
    version='0.0.1',
    packages=find_packages(),
    package_data={'': ["token/*.json"]},
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'Flask',
        'html5validator',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'requests',
        'selenium',
    ],
    python_requires='>=3.6',
)