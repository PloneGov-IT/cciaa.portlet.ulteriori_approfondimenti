# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.1.0'

setup(name='cciaa.portlet.ulteriori_approfondimenti',
      version=version,
      description="A portlet that show the C3P \"Ulteriori Approfondimenti\" section",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='https://code.redturtle.it/svn/camera-di-commercio-fe/C3P/cciaa.portlet.ulteriori_approfondimenti',
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
