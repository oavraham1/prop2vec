The evaluation method and datasets are a part of the work presented in the papers:

1. Improving Reliability of Word Similarity Evaluation by Redesigning Annotation Task and Performance Measure

2. The Interplay of Semantics and Morphology in Word Embeddings

Please cite the latter when using these resources.


'nn', 'jj', 'vb' and 'cat' - in these datasets, all the words are base forms.

'nn-inf', 'jj-inf' and 'vb-inf' - contain the same words, but inflected to other forms (to evaluate the effect of rich morphology).

'nn-jj', 'nn-vb' and 'vb-jj' - in these datasets, the target words are morphologically ambiguous (to evaluate the ambiguity effect).

'0-100' is a dataset where the target words are rare (occur less than 100 times in Hebrew wikipedia).

The code in "sample.py" loads a gensim word2vec model and runs evaluation on the 'nn' dataset.
Notice the sample model it uses ('model.vec') covers only part of the vocabulary, thus the output will contain messages of the type "could not get similarity..." for the OOV words in the datasets.

The model does not have to be gensim model, but it must have a method "similarity" which takes two words and returns a score.

Notice that you can filter comparisions by different properties (e.g. compare_type) to perform more fine-grained analysis.


For any question, contact me on oavraham1@gmail.com