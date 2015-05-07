#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup
import os

def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = "b2share-server",
  version = "0.0.1",
  author = "Dennis Blommesteijn",
  author_email = "dennis.blommesteijn@surfsara.nl",
  description = ("B2share UI API"),
  license = "MIT",
  keywords = "eudat b2share api server",
  url = "https://github.com/EUDAT-B2SHARE/",
  packages = ['b2share_server'],
  package_dir = {'b2share_server': "src/"} ,
  long_description = read('README.md'),
  scripts = ["scripts/b2share-serve"],
  install_requires=[
    'Flask-Script', 'Flask-Jsonpify'
  ],
)