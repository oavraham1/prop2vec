The evaluation method and datasets are a part of the work presented in the papers:

1. Improving Reliability of Word Similarity Evaluation by Redesigning Annotation Task and Performance Measure

2. The Interplay of Semantics and Morphology in Word Embeddings

Please cite the latter when using these resources.


The 'datasets' directory is divided into several sub-directories:

'basic' - in these datasets, all the words are base forms.

'inflected' - these datasets contain the same words as 'basic', but inflected to other forms (to evaluate the effect of rich morphology).

'rare' - in these datasets, all the target words are rare (occur less than 100 times in Hebrew wikipedia).

'ambiguous' - in these datasets, the target words are morphologically ambiguous (to evaluate the ambiguity effect).

'cohyponyms' - datasets in which the preferred-relation is defined as "cohyponyms" (in contrast to "hyponym-hypernym" in the other datasets).

The code in "sample.py" loads a gensim word2vec model and runs evaluation on the 'nn' dataset.
Notice the sample model it uses ('model.vec') covers only part of the vocabulary, thus the output will contain messages of the type "could not get similarity..." for the OOV words in the datasets.

The model does not have to be gensim model, but it must have a method "similarity" which takes two words and returns a score.

Notice that you can filter comparisions by different properties (e.g. compare_type) to perform more fine-grained analysis.


For any question, contact me on oavraham1@gmail.com