=======
larmour
=======

Larmour is a package to easily visualize the relationship between the larmour
frequency of any type of spin.

Usage
-----

CLI arguments:

-r/--range
    Range of database to generate, in mT
-q/--query
    Pandas dataframe query string(s) to match. Use ` around isotope names.
-d/--data
    Print the whole dataframe of calculated larmour values.

Querying
--------

The ``-q`` argument allows querying of the dataframe. 
Allows querying of the relative value of proton (in MHz) and electron (in GHz)
larmours at a certain field.

If query is not specified, the data is plotted in the browser with plotly.

Queryable variables:

* B: the field
* 1H: the proton larmour value
* 13C: the carbon larmour value
* e-: the electron larmour value
