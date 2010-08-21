*****************************************************
Unicode block and script data
*****************************************************

Tagenwa provides two functions in the module `tagenwa.uniscript` to access the block data and the script data from the Unicode database.
The version of the unicode database currently used by Tagenwa is 5.1.0.

Unicode block
=============
In Unicode, a `block <http://en.wikipedia.org/wiki/Unicode_block>`_
is a continuous range of code points that is named. (see http://unicode.org/glossary/#block)

.. autofunction:: tagenwa.uniscript.block


Unicode script
==============
In Unicode, a `script <http://en.wikipedia.org/wiki/Scripts_in_Unicode>`_
is a collection of letters and other written signs used to represent textual information in one or more writing systems.  For example, Russian is written with a subset of the Cyrillic script; Ukranian is written with a different subset.  The Japanese writing system uses several scripts. (see http://unicode.org/glossary/#script)

.. autofunction:: tagenwa.uniscript.script

