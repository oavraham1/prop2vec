import sys,os,inspect
import gensim
import wrappers
model = gensim.models.Word2Vec.load_word2vec_format(sys.argv[1], binary=False)

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ag_dir = currentdir + '/ag-evaluation'
morpho_sim_dir = currentdir + '/morpho-sim'
sys.path.insert(0, ag_dir)
import evaluator

parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + '/utils')
import utils

word2bases = utils.get_word2bases()
wrapped_model = wrappers.Word2vecDisamb(model, word2bases)

def semantic_sim(subfolder):
	e = evaluator.Evaluator(ag_dir + "/datasets/" + subfolder)
	print subfolder + ':', e.get_score(wrapped_model, lambda comp: True, decode_utf=False, print_oov=False)

semantic_sim("basic")
semantic_sim("rare")
semantic_sim("ambiguous")

def morpho_sim(words_file, k):
    with open(morpho_sim_dir + '/' + words_file) as f:
        lines = f.readlines()
	words = [line.strip() for line in lines]
	words = [w for w in words if w in word2bases]
	morph_dist_sum = 0
	morph_dist_num = 0
	for w in words:
		sims = wrapped_model.most_similar(w, True, k)
		sims_dists = [sim[2] for sim in sims if sim[2] != 'N/A']
		if (len(sims_dists) != 0):
			morph_dist_num += 1
			morph_dist_sum += sum(sims_dists) / float(len(sims_dists))
    print 'Avg MorphoSim for ' + words_file + ':', morph_dist_sum / morph_dist_num
														  
morpho_sim("words.txt", 10)
morpho_sim("rare_words.txt", 10)