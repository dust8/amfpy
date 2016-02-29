from setuptools import setup, find_packages


setup(
    name='amfpy',
    version='0.0.1',

    packages=find_packages('amfpy'),
    package_dir={'': 'amfpy'},

    zip_safe=True,

    description='amfpy provides Action Message Format support for python3.',

    keywords='amf amfpy pyamf python3',
)
