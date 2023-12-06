Sonify Class
============

The score functionality of Sci-Sonify is built around the ``Sonify`` class

..  code-block:: Python
    from scisonify import Sonify


A ``Sonify`` object can be constructed from a one-dimensional array-like data variable, such as a Numpy Array or Python List

..  code-block:: Python

    data = [1, 2, 3, 4]
    soni = Sonify(data)

We can then directly operate on this object to perform our Data Sonification and other
supported functionality.

..  code-block:: Python

    soni.to_audio(note_length=0.5, wave='sine')

..  code-block:: Python

    soni.plot()
