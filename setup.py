#!/usr/bin/env python

import os
from glob import glob

if os.environ.get('USE_SETUPTOOLS'):
  from setuptools import setup
  setup_kwargs = dict(zip_safe=0)

else:
  from distutils.core import setup
  setup_kwargs = dict()


storage_dirs = []

for subdir in ('whisper', 'rrd', 'log', 'log/webapp'):
  storage_dirs.append( ('storage/%s' % subdir, []) )

webapp_content = {}

for root, dirs, files in os.walk('webapp/content'):
  for filename in files:
    filepath = os.path.join(root, filename)

    if root not in webapp_content:
      webapp_content[root] = []

    webapp_content[root].append(filepath)


conf_files = [ ('conf', glob('conf/*.example')) ]
examples = [ ('examples', glob('examples/example-*')) ]

requirements=["whisper==0.9.10-warden",
              "pycairo==1.8.10",
              "Django>=1.3", 
              "django-tagging>=0.3.1"]

# Check if the json is present in the current python standard library
try:
  import json
except ImportError:
  # python version < 2.6. simplejson is required.
  requirements.append('simplejson>=2.1.6')

setup(
  name='graphite-web',
  version='0.9.10-warden',
  url='https://launchpad.net/graphite',
  author='Chris Davis',
  author_email='chrismd@gmail.com',
  license='Apache Software License 2.0',
  description='Enterprise scalable realtime graphing',
  package_dir={'' : 'webapp'},
  packages=[
    'graphite',
    'graphite.account',
    'graphite.browser',
    'graphite.cli',
    'graphite.composer',
    'graphite.render',
    'graphite.whitelist',
    'graphite.metrics',
    'graphite.dashboard',
    'graphite.graphlot',
    'graphite.events',
    'graphite.version',
    'graphite.thirdparty',
    'graphite.thirdparty.pytz',
  ],
  package_data={'graphite' :
    ['templates/*', 'local_settings.py.example']},
  scripts=glob('bin/*'),
  install_requires=requirements,
  dependency_links = [
      'http://cairographics.org/releases/py2cairo-1.8.10.tar.gz#egg=pycairo-1.8.10',
      'http://github.com/richg/whisper/tarball/0.9.x-warden#egg=whisper-0.9.10-warden',
  ],
  data_files=webapp_content.items() + storage_dirs + conf_files + examples,
  **setup_kwargs
)
