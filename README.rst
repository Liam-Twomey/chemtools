#########
ChemTools
#########

Chemtools is a set of python scripts to help with processing and interpreting
common data types I've run into. These exist as CLI utilities and/or as
importable python modules for use in other programs.

Components
==========

scicsvutils
-----------

A tool to import data from, and easily make interactive plots of the CSV-exported
data from common instruments. Currently implemented: Akta FPLC, and Cary UV-Vis

See the package `readme`_ for more details.

.. _readme: csvPlot/README.rst

larmour
-------

A python script to easily compare and plot the larmour variables of different spins.
Similar to the EasySpin EPR tools and the BYU Larmour calculator, but allows the
comparison of electron larmour spins to nuclei. This is specifically useful for
getting the numbers on DNP. See the package `readme`_ for more details.

.. _readme: larmour/README.rst

License
=======

All components of this repo are licensed under the GNU AGPL. No code in this
repo is LLM-generated.
