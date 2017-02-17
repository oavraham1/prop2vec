def extract_zipped_txt(file_name):
	import os.path
	if (os.path.exists(file_name + '.txt')):
		return
	import zipfile
	zip_file = zipfile.ZipFile(file_name + '.zip')
	zip_file.extractall()

def get_word2bases():
	import zipfile
	dict_file_name = "inf_dict"
	extract_zipped_txt(dict_file_name)
	dict_file_path = dict_file_name + ".txt"
	
	morphDict = { }
	morphs = open(dict_file_path).read().splitlines()
	for line in morphs:
		lineParts = line.split(' ');
		target = lineParts[0];
		options = { }
		for option in zip(lineParts[1::2], lineParts[2::2]):
			infParts = [p for p in option[0].split(':') if p]
			if (len(infParts) > 1 and infParts[1].startswith('S_PP')):	# unify possesives
				inf = infParts[0] + '-B'
			else:
				inf = '-'.join(infParts)
			if (inf.startswith('VB') or inf.startswith('BN')):
				parts = inf.split('-')
				props = parts[0:len(parts)-1]
				if (any(props) and props[0].startswith('BN')):	# unify present tense
					props[0] = 'VB'
					props.append('BEINONI')
				inf = '-'.join(props)
			base = option[1]
			if (not inf in options or len(options[inf]) > len(base)):	# in case of multi options for base, take the shortest
				options[inf] = base
		if (any(options)):
			morphDict[target] = options
	return morphDict
	
def get_word2count(corpus_path):
	word2count = { }
	fi = open(corpus_path, 'r')
	for line in fi:
		if (line == '\n'):
			continue
		words = line.split()
		for word in words:
		    if (not word in word2count):
			    word2count[word] = 1
		    else:
			    word2count[word] += 1
	fi.close()
	return word2count

def get_morph_parts_from_mila_str(morph_str):
    morph_parts = morph_str.split('-');
    morph_parts[0] = morph_parts[0][:2]
    return morph_parts

def get_morph_parts_from_wlm_str(wlm_str):
    return [p for p in wlm_str.split('~') if p.startswith('m:')]
	
def morpho_dist(morph_parts_combinations):
    if (not morph_parts_combinations):
        return 'N/A'
    return max([morpho_dist_per_pair(comb[0], comb[1]) for comb in morph_parts_combinations])
	
def morpho_dist_per_pair(w1_parts, w2_parts):
	max_len = max(len(w1_parts), len(w2_parts))
	for parts in [w1_parts, w2_parts]:
		for i in xrange(len(parts),max_len):
			parts.append('')
	return 1 - sum(el1 != el2 for el1, el2 in zip(w1_parts, w2_parts)) / float(max_len)

def get_wlm_str(w, l, m):
    '~'.join(['w:' + w, 'l:' + l] + ['m:' + p for p in self.get_morph_parts(m)])