#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='server_cli',
    version='0.0.1',
    author='kwp',
    author_email='i@emmm.wtf',
    description=u'A server management tool which help you memorize ssh command',
    packages=find_packages(),
    install_requires=[
        'PrettyTable'
    ],
    entry_points={
        'console_scripts': [
            'jujube=jujube_pill:jujube',
            'pill=jujube_pill:pill'
        ]
    }
)