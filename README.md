# prop2vec

prop2vec is a library for learning of word representations based on custom properties. 
This library was used in the paper [The Interplay of Semantics and Morphology in Word Embeddings](https://www.aclweb.org/anthology/E/E17/E17-2067.pdf).

 prop2vec is based on the [fastText](https://github.com/facebookresearch/fastText) library, which learns n-gram vector and represents each word as a combination of its n-grams.
Instead of n-grams, prop2vec allows using custom properties of words.

For example, one could represent a word as a combination of lemma, morphological tag and surface form:
walking = V*walk* + V*present-participle* + V*walking*

### Requirements
- gcc-4.6.3 or newer (for compiling)
- Python 2.7 (for preprocessing and evaluation)
- [gensim](https://radimrehurek.com/gensim/install.html) (for evaluation)


### Example
Run the following line on shell:
```sh
$ ./example.sh
```
This should start a process of several steps:
1. Download a morphologically analyzed sample of Hebrew Wikipedia
2. Preprocess the sample to produce the input for prop2vec
3. Compile and run prop2vec to produce the word embeddings
4. Evaluate the embeddings on the benchmarks mentioned in the paper, and output results to a file

### How to perform modifications?
##### Changing the set of properties
In the example above, prop2vec learns the representations using the following properties: 
* surface form (w)
* lemma (m)
* morphological tag (m)

Let's say we want to learn representations that are based only on surface form and lemma.
What we should do is open the file *train_evaluate.sh* and change the line `props="w+l+m"` to `props="w+l"`.

##### Defining new properties
Let's say we want to define a new property, e.g. the index of the word in the sentence.
What we should do is open the file *preprocessing/preprocess.py* and change the `token_format`.
`token_format` lambda defines how to format every token in preprocessing, so instead:
`token_format = lambda t: special_char.join(['w:' + t.word, 'l:' + t.base, 'm:' + t.morph])`
we write:
`token_format = lambda t: special_char.join(['w:' + t.word, 'l:' + t.base, 'm:' + t.morph, 'i:' + t.index])`
Notice that the index value is already extracted and stored to `t.index` as a part of the sentence processing, otherwise we would have to handle the extraction of the property value rather than just use it.

##### Using on other languages
While the training code is language-agnostic, the preprocessing and evaluation rely on Hebrew resources. 
* To adapt preprocessing to other language, the file *utils/inf_dict.txt* should be replaced with an inflections dictionary for the new language.
In case the format of the new dictionary is different, a change in the function `get_word2bases` in *utils/utils.py* will be required.
* To adapt evaluation to other language, the datasets in the *evaluation* folder should be replaced by datasets for the new language.
In case the format of the new datasets is different, a change in the file *evaluation/ag-evaluation/evaluator.py* will be required.


### References
If you make use of this software for research purposes, we'll appreciate citing the following:

    @InProceedings{avraham-goldberg:2017:EACLshort,
      author    = {Avraham, Oded  and  Goldberg, Yoav},
      title     = {The Interplay of Semantics and Morphology in Word Embeddings},
      booktitle = {Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics: Volume 2, Short Papers},
      month     = {April},
      year      = {2017},
      address   = {Valencia, Spain},
      publisher = {Association for Computational Linguistics},
      pages     = {422--426},
      url       = {http://www.aclweb.org/anthology/E17-2067}
    }

### Contact
For any question, please contact oavraham1@gmail.com