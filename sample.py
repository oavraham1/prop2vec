import gensim
hebModel = gensim.models.Word2Vec.load_word2vec_format("model.vec", binary=False)
import evaluator
e = evaluator.Evaluator("datasets/")
print e.get_score(hebModel, lambda comp: comp.set_name == 'nn')