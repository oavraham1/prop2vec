import sys,os,inspect
import gensim
import wrappers
model = gensim.models.Word2Vec.load_word2vec_format(sys.argv[1], binary=False)

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ag_dir = currentdir + '/ag-evaluation'
sys.path.insert(0, ag_dir)
import evaluator

parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + '/utils')
import utils

wrapped_model = wrappers.Word2vec(model, utils.get_word2bases())

e = evaluator.Evaluator(ag_dir + "/datasets/basic")
print e.get_score(wrapped_model, lambda comp: comp.set_name == 'nn', decode_utf=False)