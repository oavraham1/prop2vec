import math

class Comparision:
    def __init__(self, target, w1, w2, w1_prob, w2_prob, set_name, compare_type):
        self.target = target
        self.w1 = w1
        self.w2 = w2
        self.set_name = set_name
        self.compare_type = compare_type
        self.w1_prob = w1_prob
        self.w2_prob = w2_prob
        self.optimal_prob = max(w1_prob, w2_prob)
    
    def __str__(self):
        context_str = '[' + self.set_name + ',' + self.target + ',' + self.compare_type + '] '
        return context_str + self.w1 + ': ' + str(self.w1_prob) + ', ' + self.w2 + ': ' + str(self.w2_prob)

class Evaluator:
    def __init__(self, sets_folder_path):
        import glob
        import os.path
        comparisions = []
        set_files = glob.glob(sets_folder_path + "/*.txt")
        for path in set_files:
            with open(path) as f:
                lines = [line.rstrip() for line in f.readlines()]
            set_name = os.path.splitext(os.path.basename(path))[0]
            i = 0
            while (i < len(lines)):
                target = lines[i]
                i += 1
                compare_type = 'positives'
                while (i < len(lines) and lines[i] != ''):
                    if (not ',' in lines[i]):
                        compare_type = lines[i]
                        i += 1
                        continue
                    parts = lines[i].split(',')
                    w1 = parts[0]
                    w2 = parts[2]      
                    w1_prob = float(parts[1])
                    w2_prob = float(parts[3])
                    comparisions.append(Comparision(target, w1, w2, w1_prob, w2_prob, set_name, compare_type))
                    i += 1
                i += 1
        self.comparisions = comparisions

    def get_similarity(self, model, w1, w2):
        return model.similarity(w1, w2)
    
    def get_similarity_after_decode(self, model, w1, w2):
        return self.get_similarity(model, w1.decode('utf-8'), w2.decode('utf-8'))
		
    def get_score(self, model, comp_filter, decode_utf = True, print_oov = True):
        if (decode_utf):
            get_sim = self.get_similarity_after_decode
        else:
            get_sim = self.get_similarity
        model_score = 0
        optimal_score = 0
        relevant_comps = filter(comp_filter, self.comparisions)
        if (not relevant_comps):
            return 'N/A'
        for comp in relevant_comps:
            try:
                w1_sim = get_sim(model, comp.target, comp.w1)
                w2_sim = get_sim(model, comp.target, comp.w2)
            except KeyError:
                if (print_oov):
                    print "could not get similarity score between", comp.w1, "and", comp.w2
                continue
            if (w1_sim > w2_sim):
                model_prob = comp.w1_prob      
            else:
                model_prob = comp.w2_prob
            probs_diff = abs(comp.w1_prob - comp.w2_prob)
            if (model_prob == comp.optimal_prob):
                model_score += probs_diff
            optimal_score += probs_diff
        if (optimal_score == 0):
            return 'N/A'
        return model_score / optimal_score