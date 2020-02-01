#!/usr/bin/env python
# encoding: utf-8
__author__ = 'liguobao'

from setuptools import setup

setup(
    name='novel-update-robot',
    install_requires=[
        'requests',
        'bs4',
        'html2text',
        'redis'
    ],
)
