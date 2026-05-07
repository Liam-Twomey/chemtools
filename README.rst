########
fplcPlot
########

This is a simple python program to parse csv exports from FPLC software,
and plot that data.

It loads the csv, then uses Plotly to generate an interactive plot, which
is then displayed in your default web browser.

Using the interactive plot
==========================

- Trace values can be extracted by mousing over the trace
- Clicking an entry in the legend will hide/show that line.
- Zoom/manipulation controls are in the top right corner.

Installation
============

``fplcPlot.py`` is the entire program. To use it, you *can* just download
the file, install the dependencies (``pandas`` and ``plotly``) in your python
environment and use the script. It is also recommended to add the script to
your system path, to avoid needing to specify the full path for every use.

However, for convenience and ease of use, it can be installed as a tool with
the `uv` package manager:

.. code:: shell

    uv tool install git+https://github.com/Liam-Twomey/fplcPlot

This will deal with downloading the script, installing dependencies, and
adding it to your system path.

License
=======

This script is licensed under the GNU Affero Public License (AGPL).
