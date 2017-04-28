#!/usr/bin/env python
from setuptools import setup, find_packages


with open('./README.rst', 'r') as fp:
    long_description = fp.read()


with open('./LICENSE', 'r') as fp:
    _license = fp.read()

setup(
    name='rockyroad',
    version='',
    description='A library to simplify driving the web browser',
    long_description=long_description,
    author='Kevin Bradwick',
    author_email='kevinbradwick@gmail.com',
    url='https://github.com/kevbradwick/rockyroad',
    license=_license,
    packages=find_packages(exclude=('tests', 'docs', 'example',)),
    install_requires=[
        'selenium',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
