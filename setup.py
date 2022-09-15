# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 14:09:18 2021

"""

from setuptools import find_packages
from setuptools import setup

import os

# loc = os.path.dirname(os.path.realpath(__file__))
# requirementPath = loc + '/requirements.txt'
# install_requires = []

# if os.path.isfile(requirementPath):
    # with open(requirementPath) as f:
        # install_requires = f.read().splitlines()
    
setup(
          name="gwmpy", 
          version='1.0.0',
          description='this package contains some tools for data exchange with the BRO, specificly for the groundwatermonitoring domain',
          author='',
          packages=find_packages(exclude=['tests','examples']),
          install_requires=['requests>=2.24.0','lxml>=4.6.1','uuid', 'xmltodict>=0.13.0', 'pandas>=1.4.3']
          
          )