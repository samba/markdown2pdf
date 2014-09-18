#!/usr/bin/env python

from setuptools import setup
VERSION="0.0.1"

try:
    long_description=open('DESCRIPTION.rst', 'rt').read()
except Exception:
    long_description="Generates PDF files from Markdown documents"



setup(
    name = "markdown2pdf",
    description = "Markdown to PDF Converter",
    long_description = long_description,

    version = VERSION,

    author = 'Sam Briesemeister',
    author_email = 'engineering@analyticspros.com',

    license = 'Copyright Analytics Pros, 2014',
    packages = ["markdown2pdf"],

    install_requires = ["markdown2", "pisa", "reportlab==2.4", "html5lib==0.11.1", "pypdf", "pillow"],

    scripts = [  ],

    zip_safe = True
)