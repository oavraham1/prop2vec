import gensim
hebModel = gensim.models.Word2Vec.load_word2vec_format("C:\\path\\to\\model\\HebModel.bin", binary=True)
import evaluator
e = evaluator.Evaluator("C:\\path\\to\\datasets")
e.get_score(hebModel, lambda comp: comp.set_name == 'nn')