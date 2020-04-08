# Está classe deve herdar da classe PipelineElement
import re
import random
# itertools — Functions creating iterators for efficient looping
# The module standardizes a core set of fast, memory efficient tools that are useful by themselves or in combination. 
from itertools import product,combinations
# from elements.element import PipelineElement
class directionality_augmentation:
    """[Directionality augmentation of a phrase for [agent -> verb -> receiver] and [agent -> pronoun -> verb]]
    """    
    # É necessário a nome do step para por no json de exec
    # The name of this pipeline element.
    name = 'directionality'
    
    _agents_dict = {
        '1S': ['EU'],
        '2S': ['TU'], 
        '3S': ['ELE', 'ELA'],
        '1P': ['NÓS'],
        '2P': ['VÓS'],
        '3P': ['ELES', 'ELAS']
    }
    _pronouns_dict = {
        '1S': ['ME'],
        '2S': ['TE'],
        '3S': ['LHE'],
        '1P': ['NÓS'],
        '2P': ['VÓS'],
        '3P': ['LHES']
    }
    
    _regex_latin ='[A-ZÁÉÍÓÚÀÂÊÔÃÕÜÇa-záéíóúàâêôãõüç]+'
    #filtro para GI pattern
    _gi_verb_pattern = '[1-3][SP]_('+_regex_latin+')_[1-3][SP]'
    _gi_pattern = '[1-3][SP]_'+_regex_latin+'_[1-3][SP]'

    # agentes
    _agent_pattern = r'\b(EU|TU|ELE|ELA|NÓS|VÓS|ELES|ELAS)\b'

    # verbos
    _verb_pattern = r'\b({0}R)\b'.format(_regex_latin)
    # pronome obliquo atono
    _pronoun_pattern = r'\b(ME|TE|LHE|VOS|NOS|LHES)\b'

    _pattern_agent_verb = "%s %s %s" %(_agent_pattern, _verb_pattern, _agent_pattern)
    _pattern_pronoun_verb = "%s %s %s" %(_agent_pattern, _pronoun_pattern, _verb_pattern)
    
    def __init__(self, *args, **kwargs):
        pass
    
    
    ### Métodos necessários para o step de augmentation
    def find_pattern(self,phrase_gr):
        """[Find pattern in phrase, return 2 list with patterns found]
        
        Arguments:
            phrase_gr {[type]} -- [Phrase side GR]
        
        Returns:
            [type] -- [2 Years with patterns found or empty list]
        """        
        # resultado do regex para o padrão [agente -> verbo -> receptor]
        search_pattern_agent_verb = re.findall(self._pattern_agent_verb, phrase_gr)
        # resultado do regex para o padrão [agente -> pronome -> verbo]
        search_pattern_pronoun_verb = re.findall(self._pattern_pronoun_verb, phrase_gr)

        return search_pattern_agent_verb, search_pattern_pronoun_verb
    
    
    def new_patterns(self, pattern_gr, verb_gi, **kwargs):
        '''Cria uma novas formas das frases a partir de um pattern [agente -> verbo -> receptor] ou [agente -> pronome -> verbo]'''
        patterns_gr = []
        patterns_gi = []
        # norm é int 1 ou 0, para as frases dos tipos 1 e 2
        t_type = kwargs.get('norm')
        
        if t_type:#frases tipo 1
            verb = pattern_gr[1]
            # combinação com todos as possibilidades do dicionário
            combinations = product(self._agents_dict.keys(), self._agents_dict.keys(), repeat=1)

            for item in combinations:
                # criação de frases do tipo [EU, TU ...]
                # os for's são necessários nos casos de [ELE, ELA, ELES ELAS]
                for index_1, item_1  in enumerate(self._agents_dict[item[0]]):
                    for index_2, item_2 in enumerate(self._agents_dict[item[1]]):
                        gr = f'{item_1} {verb} {item_2}'
                        gi = f'{item[0]}_{verb_gi}_{item[1]}'
                        patterns_gr.append(gr)
                        patterns_gi.append(gi)
        else:#frases tipo 2
            verb = pattern_gr[2]
            # combinação com todos as possibilidades do dicionário pronouns_dict
            combinations = product(self._agents_dict.keys(), self._pronouns_dict.keys(), repeat=1)
            
            for item in combinations:
                # criação de frases do tipo [EU, TU ...]
                # os for's são necessários nos casos de [ELE, ELA, ELES ELAS]
                for index_1, item_1  in enumerate(self._agents_dict[item[0]]):
                    for index_2, item_2 in enumerate(self._pronouns_dict[item[1]]):

                        gr = f'{item_1} {item_2} {verb}'
                        gi = f'{item[0]}_{verb_gi}_{item[1]}'
                        patterns_gr.append(gr)
                        patterns_gi.append(gi)
        
        return patterns_gr,patterns_gi
    
    
    def for_string(*args,**kwargs):
        '''Transformando a padrão em [agente -> verbo -> receptor] ou [agente -> pronome -> verbo]
        em string para pesquisar a parte de trás e da frente do padrão'''
        
        if kwargs.get('agent_verb'):
            search_pattern = kwargs.get('agent_verb')
            
        elif kwargs.get('pronoun_verb'):
            search_pattern = kwargs.get('pronoun_verb')
            
        strings = []
        for pattern in search_pattern: 
            line = ''
            for index, part in enumerate(pattern):
                if not index:
                    line +=part
                else:
                    line += ' '+part
            strings.append(line)    
        return strings
    
    def assembly_phrase(self,phrase,*args,**kwargs):
        '''Monta a frase dado [agente -> verbo -> receptor] ou [agente -> pronome -> verbo]'''
 
        new_phrase_gr = phrase[0]
        new_phrase_gi = phrase[1]
        combination_gr = kwargs.get('combination_gr')
        combination_gi = kwargs.get('combination_gi')
        
        if kwargs.get('agent_verb'):
            search_pattern = kwargs.get('agent_verb')    
            pstr = for_string(agent_verb = search_pattern)# Transforma search_pattern em string
        
        else:    
            search_pattern = kwargs.get('pronoun_verb')
            pstr = for_string(pronoun_verb = search_pattern)# Transforma search_pattern em string
        
        try:
            gi_verbs = re.findall(self._gi_pattern,new_phrase_gi)# Retira verbo do lado GI
            
            for i, part_string in enumerate(pstr):
                new_phrase_gr = re.sub(part_string,combination_gr[i],new_phrase_gr)
                new_phrase_gi = re.sub(gi_verbs[i],combination_gi[i],new_phrase_gi)
        
        except Exception as e:
            print(f'Erro assembly_phrase regex.\n',e)
        
        return (new_phrase_gr,new_phrase_gi)
    
    def augmentation(self, enter_phrase):
        '''Já é possível criar as frases GR para os dois pad        rões descritos como:
         [agente -> verbo -> receptor] e [agente -> pronome -> verbo]'''
        new_patterns_gr = []
        new_patterns_gi =[]
        new_p = []
        
        phrase_gr = enter_phrase[0]

        # [agente -> verbo -> receptor] and [agente -> pronome -> verbo]
        search_pattern_agent_verb, search_pattern_pronoun_verb = find_pattern(phrase_gr)
        
        gi_verbs = re.findall(gi_verb_pattern,enter_phrase[1])
        
        # Shuffle nos pattern encontradas para para retirada de apenas 2 de forma aleatória,
        # porque para cada padrão é gerada 64 frases, logo é 64 ^ NumeroDePatterns
        random.shuffle(search_pattern_agent_verb)
        random.shuffle(search_pattern_agent_verb)
        
        search_pattern_agent_verb = search_pattern_agent_verb[:2]
        search_pattern_pronoun_verb = search_pattern_pronoun_verb[:2]
        
        '''[agente -> verbo -> receptor]''' 
        if search_pattern_agent_verb:
            for i, patterns_in_phrase in enumerate(search_pattern_agent_verb):
                gr,gi = new_patterns(patterns_in_phrase, 
                                     gi_verbs[i],
                                     norm = 1)
                
                new_patterns_gr.append(gr)
                new_patterns_gi.append(gi)          
                
        '''[agente -> pronome -> verbo]'''
        if search_pattern_pronoun_verb:
            for i, patterns_in_phrase in enumerate(search_pattern_pronoun_verb):
                gr,gi = new_patterns(patterns_in_phrase,
                                     gi_verbs[i],
                                     norm = 0)
                
                new_patterns_gr.append(gr)
                new_patterns_gi.append(gi)
            
        #combinação dos pattern das frases geradas
        combination_patterns = product(*new_patterns_gr, repeat=1)
        combination_patterns_gi = product(*new_patterns_gi, repeat=1)
        
        for cont, item_gr in enumerate(combination_patterns):
            item_gi = next(combination_patterns_gi)

            if search_pattern_pronoun_verb:
                new_p.append(assembly_phrase(enter_phrase,
                                            agent_verb = search_pattern_pronoun_verb,
                                            combination_gr = item_gr,
                                            combination_gi = item_gi))
            if search_pattern_agent_verb:
                new_p.append(assembly_phrase(enter_phrase,
                                        agent_verb = search_pattern_agent_verb,
                                        combination_gr = item_gr,
                                        combination_gi = item_gi)) 
        # Shuffle para retornar 50 frases aleatórias
        random.shuffle(new_p)
        return new_p
    
    
    def process(self,data):
        new_phrases = []
        for phrase in data:
            new_phrases.append(augmentation(phrase))
            
        return new_phrases    
    
        
    