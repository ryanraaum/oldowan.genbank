from setuptools import setup, find_packages
import sys, os

desc_lines = open('README', 'r').readlines()

setup(name='oldowan.genbank',
      version='0.1.0',
      description=desc_lines[0],
      long_description=''.join(desc_lines[2:]),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Scientific/Engineering :: Bio-Informatics"
      ],
      keywords='',
      platforms=['Any'],
      author='Ryan Raaum',
      author_email='code@raaum.org',
      url='http://www.raaum.org/software/oldowan',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=False,
      namespace_packages = ['oldowan'],
      zip_safe=True,
      test_suite = 'nose.collector',
      )

