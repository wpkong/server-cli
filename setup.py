#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='server_cli',
    version='1.0.2',
    author='kwp',
    author_email='i@emmm.wtf',
    url='https://github.com/yjxkwp/server-cli',
    description=u'A server management tool which helps you memorize ssh command',
    long_description=open("README.rst").read(),
    packages=find_packages(),
    python_requires='>=3.5, <4',
    license='MIT',
    install_requires=[
        'PrettyTable',
        'ping3'
    ],
    entry_points={
        'console_scripts': [
            'sss=server_cli:sss'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)