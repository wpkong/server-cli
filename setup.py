#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='server_cli',
    version='1.0.1',
    author='kwp',
    author_email='i@emmm.wtf',
    url='https://github.com/yjxkwp/server-cli',
    description=u'A server management tool which help you memorize ssh command',
    packages=find_packages(),
    install_requires=[
        'PrettyTable'
    ],
    entry_points={
        'console_scripts': [
            'sss=server_cli:sss'
        ]
    }
)