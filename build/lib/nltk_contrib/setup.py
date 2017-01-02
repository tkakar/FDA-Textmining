#!/usr/bin/env python
#
# Distutils setup script for NLTK-Contrib
#
# Copyright (C) 2001-2011 NLTK Project
# Author: Steven Bird <sb@csse.unimelb.edu.au>
#         Edward Loper <edloper@gradient.cis.upenn.edu>
#         Ewan Klein <ewan@inf.ed.ac.uk>
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT

from distutils.core import setup
import nltk

setup(
    #############################################
    ## Distribution Metadata
    name="nltk_contrib",
    description="NLTK-Contrib",

    version=nltk.__version__,
    url=nltk.__url__,
    long_description=nltk.__longdescr__,
    license=nltk.__license__,
    keywords=nltk.__keywords__,
    maintainer=nltk.__maintainer__,
    maintainer_email=nltk.__maintainer_email__,
    author=nltk.__author__,
    author_email=nltk.__author__,
    # platforms = <platforms>,

    #############################################
    ## Package List
    packages=['nltk_contrib'
              ]

)
