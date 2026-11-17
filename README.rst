#########
ChemTools
#########

Chemtools is a set of python scripts to help with processing and interpreting
common data types I've run into. These exist as CLI utilities and/or as
importable python modules for use in other programs.

Components
==========

csvPlot
-------

A tool to easily make interactive plots of the CSV exported data from common
instruments. See the `readme`_ for more details:

.. _readme: csvPlot/README.rst

.. include:: csvPlot/README.rst

larmour
-------

A python script to easily compare and plot the larmour variables of different spins.
Similar to the EasySpin EPR tools and the BYU Larmour calculator, but allows the
comparison of electron larmour spins to nuclei. This is specifically useful for
getting the numbers on DNP. See the `readme`_ for more details:

.. _readme: larmour/README.rst

.. include:: larmour/README.rst

License
=======

All components of this repo are licensed under the GNU AGPL. No code in this
repo is LLM-generated.
