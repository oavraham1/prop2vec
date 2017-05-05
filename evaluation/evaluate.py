import sys,os,inspect
import gensim
import wrappers
gensim_model = gensim.models.Word2Vec.load_word2vec_format(sys.argv[1], binary=False)

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ag_dir = currentdir + '/ag-evaluation'
morpho_sim_dir = currentdir + '/morpho-sim'
sys.path.insert(0, ag_dir)
import evaluator

parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + '/utils')
import utils

word2bases = utils.get_word2bases()
wrapped_model = wrappers.Word2vecDisamb(gensim_model, word2bases)

def get_word2inf(tags_file):  
    word2inf = { }
    with open(tags_file) as f:
        for line in [l.rstrip() for l in f.readlines()]:
            word_and_inf = line.split(' ')
            word2inf[word_and_inf[0]] = word_and_inf[1]
    return word2inf

word2inf = get_word2inf(parentdir + '/utils/nn_dataset_tags.txt')
	
basic_eval = evaluator.Evaluator(ag_dir + "/datasets/basic")
rare_eval = evaluator.Evaluator(ag_dir + "/datasets/rare")
amb_eval = evaluator.Evaluator(ag_dir + "/datasets/ambiguous")

def handle_err(result):
    if (result == 'N/A'):
        return 0.0001
    return result

############################### MEASURE DEFINITIONS ###############################

def basic_measure(model, pos):
    return basic_eval.get_score(model, lambda comp: comp.set_name == pos, decode_utf=False, print_oov=False)

def basic_rand_measure(model, pos):
    return basic_eval.get_score(model, lambda comp: comp.set_name == pos and comp.compare_type == 'randoms', decode_utf=False, print_oov=False)


#--------- AMBIGUITY ---------#

def ambiguous_measure(model, set_name):
    return amb_eval.get_score(model, lambda comp: comp.set_name == set_name, decode_utf=False, print_oov=False)


#--------- SPARSITY ---------#

def rare_measure(model, pos):
    return rare_eval.get_score(model, lambda comp: is_comp_of(comp, pos), decode_utf=False, print_oov=False)

def is_comp_of(comp, pos):
    return is_pos(comp.w1, pos) and is_pos(comp.w2, pos) and is_pos(comp.target, pos) 

def is_pos(word, pos):
    return word in word2bases and pos.upper() in [tag[:2] for tag in word2bases[word].keys()]


#--------- MORPHOLOGY ---------#

def morphology_measure(model, pos):
    return morpho_sim(model, pos + '.txt', 10)
        
def morpho_sim(model, words_file, k):
    with open(morpho_sim_dir + '/' + words_file) as f:
        lines = f.readlines()
    words = [line.strip() for line in lines]
    words = [w for w in words if w in word2bases]
    morph_dist_sum = 0
    morph_dist_num = 0
    for w in words:
        sims = model.most_similar(w, True, k)
        sims_dists = [sim[2] for sim in sims if sim[2] != 'N/A']
        if (len(sims_dists) != 0):
            morph_dist_num += 1
            morph_dist_sum += sum(sims_dists) / float(len(sims_dists))
    return morph_dist_sum / morph_dist_num


#--------- GENDER-AGREEMENT-BIAS ---------#

def target_gen_win_measure(model):
    return basic_eval.get_score(model, lambda comp: comp.set_name=='nn' and target_gender_win(comp), decode_utf=False, print_oov=False)

def other_gen_win_measure(model):   
    return basic_eval.get_score(model, lambda comp: comp.set_name=='nn' and other_gender_win(comp), decode_utf=False, print_oov=False)

def same_gen_measure(model):   
    return basic_eval.get_score(model, lambda comp: comp.set_name=='nn' and sg_same_gen_comp(comp), decode_utf=False, print_oov=False)

def target_gender_win(comp):
    return sg_diff_gen_comp(comp) and ((word2inf[comp.w1] == word2inf[comp.target] and comp.w1_prob > comp.w2_prob) or (word2inf[comp.w2] == word2inf[comp.target] and comp.w2_prob > comp.w1_prob))    
    
def other_gender_win(comp):
    return sg_diff_gen_comp(comp) and ((word2inf[comp.w1] == word2inf[comp.target] and comp.w1_prob < comp.w2_prob) or (word2inf[comp.w2] == word2inf[comp.target] and comp.w2_prob < comp.w1_prob))

def sg_diff_gen_comp(comp):
    return sg_comp(comp) and word2inf[comp.w1] != word2inf[comp.w2]

def sg_same_gen_comp(comp):
    return sg_comp(comp) and word2inf[comp.w1] != word2inf[comp.w2]

def sg_comp(comp):
    for word in [comp.w1, comp.w2, comp.target]:
        if (not word2inf[word] in ['NN-F-S', 'NN-M-S']):
            return False
    return True

############################### BENCHMARKS DEFINITIONS ###############################

def run_benchmark(model, measure_name, measure_func, datasets):
    total = 0
    for dataset in datasets:
        result = measure_func(model, dataset)
        print measure_name + '-' + dataset, result
        total += handle_err(result)
    print measure_name + '-avg', total / float(len(datasets))    

def basic_benchmark(model):
    run_benchmark(model, 'basic', basic_measure, ['nn', 'vb', 'jj'])
    
def basic_rand_benchmark(model):
    run_benchmark(model, 'basic-rand', basic_rand_measure, ['nn', 'vb', 'jj'])
    
def ambiguty_benchmark(model):
    run_benchmark(model, 'amb', ambiguous_measure, ['nn-vb','nn-jj','vb-jj'])
    
def sparsity_benchmark(model):
    run_benchmark(model, 'rare', rare_measure, ['nn', 'vb', 'jj'])

def gender_bias_benchmark(model):
    tgw_result = target_gen_win_measure(model)
    ogw_result = other_gen_win_measure(model)
    dg_avg = (handle_err(tgw_result) + handle_err(ogw_result)) / 2.0
    sg_result = same_gen_measure(model)
    print 'same-gen', sg_result
    print 'target-gen-win', tgw_result
    print 'other-gen-win', ogw_result
    print 'diff-gens-avg', dg_avg
    print 'diff/same', dg_avg / handle_err(sg_result)
    
def morphology_benchmark(model):
    run_benchmark(model, 'morph', morphology_measure, ['nn','vb','jj'])
	
############################### RUN BENCHMARKS ###############################
	
benchmarks = [basic_benchmark, basic_rand_benchmark, ambiguty_benchmark, sparsity_benchmark, gender_bias_benchmark, morphology_benchmark]
for benchmark in benchmarks:
    benchmark(wrapped_model)