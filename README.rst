===============
OSM Road Length
===============

A tool to get the highway length from Open Street Maps of a region using Python.

It supports any region size and shape.

Installing
-----------
.. code:: python

   pip install osm-road-length

Using
-----

Import It

.. code:: python

        import osm_road_length

Get length from geometry

.. code:: python        

        from shapely import wkt

        geometry = wkt.loads('POLYGON((-43.2958811591311 -22.853167273541693,-43.30961406928735 -23.035275736044728,-43.115980036084224 -23.02010939749927,-43.157178766552974 -22.832917893834313,-43.2958811591311 -22.853167273541693))')

        length = osm_road_length.get(geometry)

Credits
-------

* Free software: MIT license

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
    