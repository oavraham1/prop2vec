import itertools
import re
import random
import sys,os,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + '/utils')
import utils

random.seed(10)

class Word2vec(object):
    def __init__(self, model, word2bases):
        self.model = model
        self.word2bases = word2bases

    def inflection_sims_count(self, word, n=10):
        if (not word in self.word2bases):
            print 'N/A'
            return 0
        word_bases = set(self.word2bases[word].values())
        sims = self.get_senses_sims(word, n)
        count = 0
        for sim in sims:
            sim_token = self.get_raw_word(sim[0].encode('utf-8'))
            if (sim_token in self.word2bases and len(set(self.word2bases[sim_token].values()) & word_bases) > 0):
                count += 1
        return count / float(n)

    def get_senses_sims(self, word, n):
        senses = self.filter_oovs(self.get_senses(word))
        senses_sims = [self.model.most_similar(sense, topn=n) for sense in senses]
        sims = [item for sublist in senses_sims for item in sublist if item[0]!='</s>']
        return sorted(sims, key=lambda sim:sim[1], reverse=True)[:n]
		
    def get_morph_parts_combinations(self, word_senses, sim):
        if (not sim.encode('utf-8') in self.word2bases):
            return []
        word = next(iter(word_senses))
        word_senses_morph_parts = [utils.get_morph_parts_from_mila_str(m) for m in set(self.word2bases[word.encode('utf-8')].keys())]
        sim_senses_morph_parts = [utils.get_morph_parts_from_mila_str(m) for m in set(self.word2bases[sim.encode('utf-8')].keys())]
        return itertools.product(word_senses_morph_parts, sim_senses_morph_parts)

    def most_similar(self, word, distinct_base=True, n=10):
        num_of_sims = n
        if (distinct_base):
            num_of_sims *= 10
        senses = s/home/oded/ag-evaluation/model.vecelf.filter_oovs(self.get_senses(word))
        senses_sims = [self.model.most_similar(sense, topn=num_of_sims) for sense in senses]
        sims = [item for sublist in senses_sims for item in sublist if item[0]!='</s>']
        best_sims = sorted(sims, key=lambda sim:sim[1], reverse=True)
        if (distinct_base):
            all_sims_bases = set()
            if (word in self.word2bases):
                all_sims_bases = set(self.word2bases[word].values())
            distinct_sims = []
            for sim in best_sims:
                sim_token = self.get_raw_word(sim[0].encode('utf-8'))
                if (sim_token in self.word2bases):
                    bases = set(self.word2bases[sim_token].values())
                    if (len(bases & all_sims_bases) > 0):
                        continue
                    all_sims_bases |= bases
                distinct_sims.append(sim)
            best_sims = distinct_sims
        return [(sim[0], sim[1], utils.morpho_dist(self.get_morph_parts_combinations(senses, sim[0]))) for sim in best_sims[:n]]
    
    def similarity(self, w1, w2, print_pair=False, print_errors=True):
        w1_senses = self.filter_oovs(self.get_senses(w1))
        w2_senses = self.filter_oovs(self.get_senses(w2))
        combinations = self.get_combinations(w1_senses, w2_senses)
        if (not combinations):
            if (print_errors):
                print w1, w2, "N/A"
            return random.random() / 10.0
        
        max_sim = -1
        for w1_sense, w2_sense in combinations:
            sim = self.model.similarity(w1_sense, w2_sense)
            if (sim > max_sim):
                max_sim = sim
                best_senses = w1_sense, w2_sense             
        
        if (print_pair):
            print best_senses[0], best_senses[1]
            
        return self.model.similarity(best_senses[0], best_senses[1])
    
    def get_senses(self, word):
        return [word]
    
    def filter_oovs(self, words):
        return set([w for w in [word.decode('utf-8') for word in words] if self.model.vocab.has_key(w)])
    
    def get_combinations(self, w1_senses, w2_senses):
        return set(itertools.product(w1_senses, w2_senses))
	
    def get_raw_word(self, word):
        return word

class Word2vecBases(Word2vec):
    def get_senses(self, word):
        if (not word in self.word2bases):
            return [word]
        return [base for base in self.word2bases[word].values()]
		
class Word2vecDisamb(Word2vec):
    def __init__(self, model, word2bases):
        super(Word2vecDisamb, self).__init__(model, word2bases)
        self.word2taggedwords = { }
        for tagged_word in [w for w in self.model.vocab.iterkeys() if w != '</s>']:
            word = self.get_raw_word(tagged_word).encode('utf-8')         
            if (not word in self.word2taggedwords):
                self.word2taggedwords[word] = []
            self.word2taggedwords[word].append(tagged_word.encode('utf-8'))

    def get_senses(self, word):
        if (not word in self.word2taggedwords):
            return []
        return self.word2taggedwords[word]

    def get_raw_word(self, word):
        return word[1:word.index('~')]

    def get_morph_parts_combinations(self, word_senses, sim):
        senses_morph_parts = [utils.get_morph_parts_from_wlm_str(sense) for sense in word_senses]
        sim_morph_parts = utils.get_morph_parts_from_wlm_str(sim)
        return [[sense_morph_parts, sim_morph_parts] for sense_morph_parts in senses_morph_parts]