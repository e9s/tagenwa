*****************************************************
Unicode block and script data
*****************************************************

Tagenwa provides functions in the module `tagenwa.text.script` to access the block data
and the script data from the Unicode database.
Tagenwa currently uses the version 6.0.0 of the unicode database.


Unicode block
=============
In Unicode, a `block <http://en.wikipedia.org/wiki/Unicode_block>`_
is a named continuous range of codepoints (see http://unicode.org/glossary/#block).
The `block()` function returns the name of the block as defined in the Unicode database.

.. autofunction:: tagenwa.text.script.block


Unicode script
==============
In Unicode, a `script <http://en.wikipedia.org/wiki/Scripts_in_Unicode>`_
is a collection of letters and other written signs used to represent textual information in one or more writing systems.
For example, Russian is written with a subset of the Cyrillic script,
Ukranian is written with a different subset
and Japanese writing system uses several scripts (see http://unicode.org/glossary/#script).
The `script()` function returns the name of the script as defined in the Unicode database.

.. autofunction:: tagenwa.text.script.script

