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
          name="bro-exchange", 
          version='1.0.2',
          description='This python package contains tools to retrieve data from / send data to the Dutch National Key Registry of the Subsurface (Basis Registratie Ondergrond).',
          author='Karl Schutt',
          author_email='karlschutt@outlook.com',

          packages=find_packages(exclude=['tests','examples']),
          install_requires=['requests>=2.24.0','lxml>=4.6.1','uuid'],
          keywords=['python', 'BRO','Basis Registratie Ondergrond','Bronhouderportaal',],
          classifiers= [    
             "Programming Language :: Python :: 3",
             "Operating System :: Microsoft :: Windows",
          ]                 
          )