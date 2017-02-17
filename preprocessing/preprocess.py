import os,sys,inspect,getopt

class Token:
    def __init__(self, conll_line, word2bases):
        parts = conll_line.split('\t')
        self.index = int(parts[0])
        if (parts[1] == special_char):
            parts[1] = '-'
        self.word = parts[1]
        self.dep_root_index = int(parts[6])
        self.dep_type = parts[7]
        self.morph = self.__get_morph(parts)
        self.base = self.__get_base(word2bases)
		
    def __str__(self):
        return self.word + ': ' + ','.join([self.index, self.morph, self.base, self.dep_root, self.dep_type])
        
    def __get_morph(self, parts):
        pos = parts[3]
        detailed_pos = parts[4]
        
        if (detailed_pos == "VB-TOINFINITIVE"):
            morph = "tense=TOINFINITIVE"
        else:
            morph = parts[5]
        if (morph == '_'):
            return pos
        if (pos == 'BN'):
            pos = 'VB'
            morph += "|tense=BEINONI"
        morph_parts = morph.split('|')
        if (len(morph_parts) == 5):
            morph_parts = ['gen=MF'] + morph_parts[2:]
        morph = '-'.join([pos] + [p.split('=')[1] for p in morph_parts])
        if ('POS' in detailed_pos):
            morph += '-B'
        
        return morph
    
    def __get_base(self, word2bases):
        if (self.word in word2bases and self.morph in word2bases[self.word]):
            return word2bases[self.word][self.morph]
        return self.word

class Sentence:
    def __init__(self, conll_lines, word2bases):
        self.tokens = [Token(line, word2bases) for line in conll_lines]
    
    def print_sentence(self):
        for token in self.tokens:
            print token

special_char = '~'

class ModelCreator:
    def __init__(self, word2bases, is_rare):
        self.word2bases = word2bases
        self.is_rare = is_rare
    
    def get_morph_parts(self, morph):
        morph_parts = morph.split('-');
        morph_parts[0] = morph_parts[0][:2]
        return morph_parts
            
    def create_model(self, corpus_file_path, output_path):
        with open(corpus_file_path, 'rb') as rf:
            with open(output_path, 'wb') as wf:
                line = rf.readline()
                while (line != ''):
                    conll_lines = []
                    while (line.strip() != ''):
                        conll_lines.append(line)
                        line = rf.readline()
                    if (not conll_lines):
                        line = rf.readline()
                        continue
                    sentence = Sentence(conll_lines, self.word2bases)        
                    tokens = [t for t in sentence.tokens if not self.is_rare(t.word) and not t.word in ['*PRP*', '*POS*', '*DEF*', '*ACC*']]                    
                    wf.write(' '.join([special_char.join(['w:'+t.word, 'l:'+t.base, 'm:'+t.morph]) for t in tokens]) + '\n')
                    line = rf.readline()
					
def main(argv):
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	parentdir = os.path.dirname(currentdir)
	sys.path.insert(0, parentdir + '/utils')
	import utils

	word2bases = utils.get_word2bases()
	word2count = utils.get_word2count(inputfile)

	is_rare = lambda word: word not in word2count or word2count[word] < 5
	creator = ModelCreator(word2bases, is_rare)
	creator.create_model(inputfile, outputfile)

	
if __name__ == "__main__":
    main(sys.argv[1:])
