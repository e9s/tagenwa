***********************
Language identification
***********************

Introduction
============
Tagenwa is able to identify the natural language(s) in which a text even when the text is written in several languages.
Each token in the document is assigned to a natural language based on the letters that composes the token and the language of the tokens surrounding it.

The language identification in Tagenwa is performed by combining a n-gram language identification algorithm at the level of the token with a hidden Markov model over the whole sequence of tokens composing the text.
The n-gram language identification algorithm returns for each token a probability estimation of each language the algorithm has been trained on.
These probability estimates are then used as the emission probabilities of the hidden Markov model where the hidden state is the language. The transition probabilities of the hidden Markov model depends on whether the transition tokens are considered as word or not.


Token language identification
=============================   
The language identification of a single token can be done with an instance of the class `NgramLanguageIdentifier`.  This class implements the language identification using the frequencies of n-grams, as described by Dunning (1994).

.. autofunction:: tagenwa.langid.ngram.ngram_generator_factory

.. autoclass:: tagenwa.langid.ngram.NgramLanguageIdentifier
	:members:
	:undoc-members:


Text language identification
============================

The language identification of multi-lingual text can be done with an instance of the class `NgramHMMLanguageIdentifier` (see below).
This class extends the class `tagenwa.hmm.AbstractHMM` which implements the `Viterbi algorithm <http://en.wikipedia.org/wiki/Viterbi_algorithm>`_
but left unimplemented the methods to calculate the initial, emission and transition probabilities.


.. autoclass:: tagenwa.langid.ngramhmm.NgramHMMLanguageIdentifier
	:members:
	:undoc-members:

