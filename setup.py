# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '2.0.0'

setup(
    name='cciaa.portlet.ulteriori_approfondimenti',
    version=version,
    description='Un riquadro che mostra una sezione "Ulteriori Approfondimenti"',
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='RedTurtle Technology',
    author_email='sviluppoplone@redturtle.it',
    url='https://github.com/PloneGov-IT/cciaa.portlet.ulteriori_approfondimenti',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['cciaa', 'cciaa.portlet'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
