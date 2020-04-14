import re
import random

# Pipeline
####from registry import register_element
####from elements.element import PipelineElement
# This class will inherit from PipelineElement class

# itertools — Functions creating iterators for efficient looping
# The module standardizes a core set of fast, memory efficient tools that are useful by themselves or in combination. 
from itertools import product,combinations

class Directionality_Augmentation():##(PipelineElement)
    """[Directionality augmentation of a phrase for the following pattern 
    [agent -> verb -> receiver] and [agent -> pronoun -> verb]]
    """    
    
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
        '1P': ['NOS'],
        '2P': ['VOS'],
        '3P': ['LHES']
    }
    _valid_chars ='A-ZÁÉÍÓÚÀÂÊÔÃÕÜÇa-záéíóúàâêôãõüç_'
    _high_valid_chars = '['+_valid_chars+']+'
    #GI pattern filter 
    _gi_verb_pattern = '[1-3][SP]_('+_high_valid_chars+')_[1-3][SP]'
    _gi_pattern = '[1-3][SP]_'+_high_valid_chars+'_[1-3][SP]'

    # pronome reto
    _agent_pattern = r'\b(EU|TU|ELE|ELA|NÓS|VÓS|ELES|ELAS)\b'

    # verbs
    _verb_pattern = r'\b({0}R|DO_QUE)\b'.format(_high_valid_chars)
    
    # pronome obliquo atono
    _pronoun_pattern = r'\b(ME|TE|LHE|VOS|NOS|LHES)\b'

    # both patterns -> [pronome reto, verbo, pronome reto] 
    # e [pronome reto, pronome obliquo atono, verbo]
    _pattern_agent_verb = "%s %s %s" %(_agent_pattern, _verb_pattern, _agent_pattern)
    _pattern_pronoun_verb = "%s %s %s" %(_agent_pattern, _pronoun_pattern, _verb_pattern)
    
    def __init__(self, *args, **kwargs):
        #super.__init__(*args, **kwargs)
        pass
        
     
    #! Métodos necessários para o step de augmentation
    def find_pattern(self,phrase_gr):
        """[Find pattern in phrase, return 2 lists with each pattern]
        
        Arguments:
            phrase_gr {string} -- [gr type phrase]
        
        Returns:
            [type] -- [2 lists with patterns found or 2 empty lists if 
                       no pattern is encountered]
        """ 
               
        # regex result for [pronome reto, verbo, pronome reto]
        search_pattern_agent_verb = re.findall(self._pattern_agent_verb+'|'+self._pattern_pronoun_verb, phrase_gr)
        
        # regex result for [pronome reto, pronome obliquo atono, verbo]
        #search_pattern_pronoun_verb = re.findall(self._pattern_pronoun_verb, phrase_gr)

        return search_pattern_agent_verb#, search_pattern_pronoun_verb
    
    
    def new_patterns(self, pattern_gr, verb_gi, **kwargs):
        '''creates new phrases from the following patterns 
       [pronome reto, verbo, pronome reto] ou [pronome reto, pronome obliquo atono, verbo]'''
        patterns_gr = []
        patterns_gi = []
        
        # pattern_gr[-1]  == '' -> [pronome reto, verbo, pronome reto] 
        # or pattern_gr[0] == '' -> [pronome reto, pronome obliquo atono, verbo]
               
        # [pronome reto, verbo, pronome reto] -> 1
        if pattern_gr[-1] == '':
            
            verb = pattern_gr[1]
            
            # Combinations involving all possible dictionary keys of agensts_dict
            combinations = product(self._agents_dict.keys(), self._agents_dict.keys(), repeat=1)


            for combination in combinations:
                # creating phrases of type: [EU, TU ...]
                # The other loops are necessary in these following cases: [ELE, ELA, ELES ELAS]
                for index_1, directional_1  in enumerate(self._agents_dict[combination[0]]):
                    
                    for index_2, directional_2 in enumerate(self._agents_dict[combination[1]]):
                        
                        gr = f'{directional_1} {verb} {directional_2}'
                        gi = f'{combination[0]}_{verb_gi}_{combination[1]}'
                        patterns_gr.append(gr)
                        patterns_gi.append(gi)
        
        # [pronome reto, pronome obliquo atono, verbo] -> 2
        elif pattern_gr[0] == '':
            
            verb = pattern_gr[-1]
            # Combinations involving all possible dictionary keys of pronouns_dict
            combinations = product(self._agents_dict.keys(), self._pronouns_dict.keys(), repeat=1)
            
            for combination in combinations:
                # creating phrases of type: [EU, TU ...]
                # The other loops are necessary in these following cases: [ELE, ELA, ELES ELAS]
                for index_1, directional_1  in enumerate(self._agents_dict[combination[0]]):
                    for index_2, directional_2 in enumerate(self._pronouns_dict[combination[1]]):

                        gr = f'{directional_1} {directional_2} {verb}'
                        gi = f'{combination[0]}_{verb_gi}_{combination[1]}'
                        patterns_gr.append(gr)
                        patterns_gi.append(gi)
        
        return patterns_gr,patterns_gi
    
    
    def for_string(*args,**kwargs):
        '''Transforms a pattern ([pronome reto -> verbo -> pronome reto] 
            or [pronome reto -> pronome obliquo -> verbo])
            in a string to search for what comes before and after '''
        
        if kwargs.get('search_pattern'):
            search_pattern = kwargs.get('search_pattern')
            
        list_of_str = []
        
        # Transforms the pattern in a string to check
        # for what comes before and after it in the phrase
        
        for tuple_pattern  in search_pattern:
            pattern_str = ''

            for index, str_pattern in enumerate(tuple_pattern):

                if str_pattern != '':
                    pattern_str += str_pattern + ' '

            list_of_str.append(pattern_str[:-1])
                                
        return list_of_str
    
    def assembly_phrase(self,phrase,*args,**kwargs):
        '''Creates new phrases with => before_part + pattern + after_part 
        for each combination in new_patterns method [pronome reto -> verbo -> pronome reto] 
        or [pronome reto -> pronome obliquo -> verb]'''
 
        new_phrase_gr = phrase[0]
        new_phrase_gi = phrase[1]
        combination_gr = kwargs.get('combination_gr')
        combination_gi = kwargs.get('combination_gi')
        
        if kwargs.get('search_pattern'): 
            search_pattern = kwargs.get('search_pattern')  
            # Transforms search_pattern in a string  
            search_pattern_to_string = self.for_string(search_pattern = search_pattern)

        #print(f'assembly_phrase: \nGR:{combination_gr}\nGI:{combination_gi}')
        #print(f'search_pattern_to_string:{search_pattern_to_string}')
        try:
            # Gets all patterns in GI
            gi_verbs = re.findall(self._gi_pattern, new_phrase_gi)
            
            # Creates new phrases with new directionalities elements for both gr and gi
            for i, part_string in enumerate(search_pattern_to_string):
                
                new_phrase_gr = re.sub(part_string,combination_gr[i], new_phrase_gr)
                new_phrase_gi = re.sub(gi_verbs[i], combination_gi[i], new_phrase_gi)
        
        except Exception as e:
            print(f'Error assembly_phrase regex.\n',e)
            
        return (new_phrase_gr,new_phrase_gi)
    
    def augmentation(self, gr_gi_tuple, max_new_sentences=50):
        """[Does the augmentation for both gr, gi]
        
        Arguments:
            gr_gi_tuple {(string, string)} -- [tuple containing (gr_phrase, gi_phrase)]
        
        Keyword Arguments:
            max_new_sentences {int} -- [max_new_sentencess the amount of new phrases generated for
                            each (gr, gi)] (default: {50})
        
        Returns:
            [list] -- [New phrases generated]
        """        
        new_patterns_gr = []
        new_patterns_gi =[]
        new_phrases = []
        phrase_gr = gr_gi_tuple[0]

        # gets both [pronome reto -> verbo -> pronome reto]  
        # and [pronome reto -> pronome obliquo -> verbo]
        search_pattern_agent_verb  = self.find_pattern(phrase_gr)
              
        # find all verbs in GI 
        gi_verbs = re.findall(self._gi_verb_pattern, gr_gi_tuple[1])
        
        #* [pronome reto -> verbo -> pronome reto]
        # [pronome reto -> pronome obliquo -> verbo]
        if search_pattern_agent_verb:
            
            # Creates new phrases for each pattern
            # [pronome reto -> pronome obliquo -> verbo]
            for i, patterns_in_phrase in enumerate(search_pattern_agent_verb):
                gr,gi = self.new_patterns(patterns_in_phrase, 
                                          gi_verbs[i])
                new_patterns_gr.append(gr)
                new_patterns_gi.append(gi)            
        
              
        try:
            # Combinating patterns of the newly created phrases
            combination_patterns_gr = product(*new_patterns_gr)
            combination_patterns_gi = product(*new_patterns_gi)
            
            for combination_gr in combination_patterns_gr:
                # New Patterns for GI 
                combination_gi = next(combination_patterns_gi)
                
                # Generates new phrases [befores_string + pattern + after_string] 
                # if the following pattern is encountered 
                # [pronome reto -> pronome obliquo -> verbo]
                # Generates new phrases [befores_string + pattern + after_string] 
                # if the following pattern is encountered 
                # [pronome reto -> verbo -> pronome reto]
                new_phrases.append(self.assembly_phrase(gr_gi_tuple,
                                                        search_pattern = search_pattern_agent_verb,
                                                        combination_gr = combination_gr,
                                                        combination_gi = combination_gi))
                    
        except Exception as e:
            print('No pattern was found',e)
        
        # Shuffle to return {max_new_sentences ( default_val = 50 )} random phrases
        try:
            new_phrases.remove(gr_gi_tuple)
        except Exception as e:
            print(e)
        finally:
            random.shuffle(new_phrases)
            new_phrases = new_phrases[:max_new_sentences]
            new_phrases.insert(0,gr_gi_tuple)
            
        return new_phrases
    
    
    def process(self,data, max_new_sentences=50):
        # Used to do the augmentation in phrases
        new_phrases = []
        for phrase in data:
            new_phrases.extend(self.augmentation(phrase, max_new_sentences = max_new_sentences))
            
        return new_phrases 