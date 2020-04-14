import re
import random

<<<<<<< HEAD
# Pipeline
####from registry import register_element
####from elements.element import PipelineElement
=======

>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
# This class will inherit from PipelineElement class

# itertools — Functions creating iterators for efficient looping
# The module standardizes a core set of fast, memory efficient tools that are useful by themselves or in combination. 
from itertools import product,combinations

<<<<<<< HEAD
class Directionality_Augmentation():##(PipelineElement)
=======

class Directionality_Augmentation:
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
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
<<<<<<< HEAD
    _valid_chars ='A-ZÁÉÍÓÚÀÂÊÔÃÕÜÇa-záéíóúàâêôãõüç_'
    _high_valid_chars = '['+_valid_chars+']+'
    #GI pattern filter 
    _gi_verb_pattern = '[1-3][SP]_('+_high_valid_chars+')_[1-3][SP]'
    _gi_pattern = '[1-3][SP]_'+_high_valid_chars+'_[1-3][SP]'
=======
    
    _regex_latin ='[A-ZÁÉÍÓÚÀÂÊÔÃÕÜÇa-záéíóúàâêôãõüç]+'
    
    #GI pattern filter 
    _gi_verb_pattern = '[1-3][SP]_('+_regex_latin+')_[1-3][SP]'
    _gi_pattern = '[1-3][SP]_'+_regex_latin+'_[1-3][SP]'
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519

    # pronome reto
    _agent_pattern = r'\b(EU|TU|ELE|ELA|NÓS|VÓS|ELES|ELAS)\b'

    # verbs
<<<<<<< HEAD
    _verb_pattern = r'\b({0}R|DO_QUE)\b'.format(_high_valid_chars)
=======
    _verb_pattern = r'\b({0}R)\b'.format(_regex_latin)
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
    
    # pronome obliquo atono
    _pronoun_pattern = r'\b(ME|TE|LHE|VOS|NOS|LHES)\b'

    # both patterns -> [pronome reto, verbo, pronome reto] 
    # e [pronome reto, pronome obliquo atono, verbo]
    _pattern_agent_verb = "%s %s %s" %(_agent_pattern, _verb_pattern, _agent_pattern)
    _pattern_pronoun_verb = "%s %s %s" %(_agent_pattern, _pronoun_pattern, _verb_pattern)
    
    def __init__(self, *args, **kwargs):
        #super.__init__(*args, **kwargs)
        pass
<<<<<<< HEAD
        
=======
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
     
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
<<<<<<< HEAD
        search_pattern_agent_verb = re.findall(self._pattern_agent_verb+'|'+self._pattern_pronoun_verb, phrase_gr)
        
        # regex result for [pronome reto, pronome obliquo atono, verbo]
        #search_pattern_pronoun_verb = re.findall(self._pattern_pronoun_verb, phrase_gr)
=======
        search_pattern_agent_verb = re.findall(self._pattern_agent_verb, phrase_gr)
        # regex result for [pronome reto, pronome obliquo atono, verbo]
        search_pattern_pronoun_verb = re.findall(self._pattern_pronoun_verb, phrase_gr)
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519

        return search_pattern_agent_verb#, search_pattern_pronoun_verb
    
    
    def new_patterns(self, pattern_gr, verb_gi, **kwargs):
        '''creates new phrases from the following patterns 
       [pronome reto, verbo, pronome reto] ou [pronome reto, pronome obliquo atono, verbo]'''
        patterns_gr = []
        patterns_gi = []
        
<<<<<<< HEAD
        # pattern_gr[-1]  == '' -> [pronome reto, verbo, pronome reto] 
        # or pattern_gr[0] == '' -> [pronome reto, pronome obliquo atono, verbo]
               
        # [pronome reto, verbo, pronome reto] -> 1
        if pattern_gr[-1] == '':
=======
        # norm is an int 1 -> [pronome reto, verbo, pronome reto] 
        # or 2 -> [pronome reto, pronome obliquo atono, verbo]
        t_type = kwargs.get('norm')
               
        # [pronome reto, verbo, pronome reto] -> 1
        if t_type == 1:
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
            
            verb = pattern_gr[1]
            
            # Combinations involving all possible dictionary keys of agensts_dict
            combinations = product(self._agents_dict.keys(), self._agents_dict.keys(), repeat=1)


<<<<<<< HEAD
            for combination in combinations:
                # creating phrases of type: [EU, TU ...]
                # The other loops are necessary in these following cases: [ELE, ELA, ELES ELAS]
                for index_1, directional_1  in enumerate(self._agents_dict[combination[0]]):
                    
                    for index_2, directional_2 in enumerate(self._agents_dict[combination[1]]):
                        
                        gr = f'{directional_1} {verb} {directional_2}'
                        gi = f'{combination[0]}_{verb_gi}_{combination[1]}'
=======
            for item in combinations:
                # creating phrases of type: [EU, TU ...]
                # The other loops are necessary in these following cases: [ELE, ELA, ELES ELAS]
                for index_1, item_1  in enumerate(self._agents_dict[item[0]]):
                    
                    for index_2, item_2 in enumerate(self._agents_dict[item[1]]):
                        
                        gr = f'{item_1} {verb} {item_2}'
                        gi = f'{item[0]}_{verb_gi}_{item[1]}'
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
                        patterns_gr.append(gr)
                        patterns_gi.append(gi)
        
        # [pronome reto, pronome obliquo atono, verbo] -> 2
<<<<<<< HEAD
        elif pattern_gr[0] == '':
            
            verb = pattern_gr[-1]
            # Combinations involving all possible dictionary keys of pronouns_dict
            combinations = product(self._agents_dict.keys(), self._pronouns_dict.keys(), repeat=1)
            
            for combination in combinations:
                # creating phrases of type: [EU, TU ...]
                # The other loops are necessary in these following cases: [ELE, ELA, ELES ELAS]
                for index_1, directional_1  in enumerate(self._agents_dict[combination[0]]):
                    for index_2, directional_2 in enumerate(self._pronouns_dict[combination[1]]):
=======
        elif t_type == 2:
            
            verb = pattern_gr[2]
            # Combinations involving all possible dictionary keys of pronouns_dict
            combinations = product(self._agents_dict.keys(), self._pronouns_dict.keys(), repeat=1)
            
            for item in combinations:
                # creating phrases of type: [EU, TU ...]
                # The other loops are necessary in these following cases: [ELE, ELA, ELES ELAS]
                for index_1, item_1  in enumerate(self._agents_dict[item[0]]):
                    for index_2, item_2 in enumerate(self._pronouns_dict[item[1]]):
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519

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
            
<<<<<<< HEAD
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
=======
        elif kwargs.get('pronoun_verb'):
            search_pattern = kwargs.get('pronoun_verb')
            
        strings = []
        
        # Transforms the pattern in a string to check
        # for what comes before and after it in the phrase
        for pattern in search_pattern: 
            line = ''
            for index, part in enumerate(pattern):
                if not index:
                    line +=part
                else:
                    line += ' '+part
            strings.append(line)    
        return strings
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
    
    def assembly_phrase(self,phrase,*args,**kwargs):
        '''Creates new phrases with => before_part + pattern + after_part 
        for each combination in new_patterns method [pronome reto -> verbo -> pronome reto] 
        or [pronome reto -> pronome obliquo -> verb]'''
 
        new_phrase_gr = phrase[0]
        new_phrase_gi = phrase[1]
        combination_gr = kwargs.get('combination_gr')
        combination_gi = kwargs.get('combination_gi')
        
<<<<<<< HEAD
        if kwargs.get('search_pattern'): 
            search_pattern = kwargs.get('search_pattern')  
            # Transforms search_pattern in a string  
            search_pattern_to_string = self.for_string(search_pattern = search_pattern)

        #print(f'assembly_phrase: \nGR:{combination_gr}\nGI:{combination_gi}')
        #print(f'search_pattern_to_string:{search_pattern_to_string}')
=======
        
        if kwargs.get('agent_verb'): 
            search_pattern = kwargs.get('agent_verb')  
            # Transforms search_pattern in a string  
            search_pattern_to_string = self.for_string(agent_verb=search_pattern)
        
        else:    
            search_pattern = kwargs.get('pronoun_verb')
            # Transforms search_pattern in a string
            search_pattern_to_string = self.for_string(pronoun_verb=search_pattern)
        
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
        try:
            # Gets all patterns in GI
            gi_verbs = re.findall(self._gi_pattern, new_phrase_gi)
            
            # Creates new phrases with new directionalities elements for both gr and gi
            for i, part_string in enumerate(search_pattern_to_string):
                
                new_phrase_gr = re.sub(part_string,combination_gr[i], new_phrase_gr)
                new_phrase_gi = re.sub(gi_verbs[i], combination_gi[i], new_phrase_gi)
        
        except Exception as e:
            print(f'Error assembly_phrase regex.\n',e)
<<<<<<< HEAD
            
        return (new_phrase_gr,new_phrase_gi)
    
    def augmentation(self, gr_gi_tuple, max_new_sentences=50):
=======
        
        return (new_phrase_gr,new_phrase_gi)
    
    def augmentation(self, gr_gi_tuple, limit=50):
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
        """[Does the augmentation for both gr, gi]
        
        Arguments:
            gr_gi_tuple {(string, string)} -- [tuple containing (gr_phrase, gi_phrase)]
<<<<<<< HEAD
        
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
=======
        
        Keyword Arguments:
            limit {int} -- [Limits the amount of new phrases generated for
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
        search_pattern_agent_verb, search_pattern_pronoun_verb = self.find_pattern(phrase_gr)
        
        
        # Since a phrase may have multiple patterns in it, a limit is set to get only 2 patterns 
        # to create new phrases, due to the fact for each pattern 64 new phrases are generated
        # so the combination is 64 ^ NumberOfPatterns
        random.shuffle(search_pattern_agent_verb)
        random.shuffle(search_pattern_pronoun_verb)
        
        # after the shuffle the limit of 2 patterns is set
        search_pattern_agent_verb = search_pattern_agent_verb[:2]
        search_pattern_pronoun_verb = search_pattern_pronoun_verb[:2]
        
        # find all verbs in GI 
        gi_verbs = re.findall(self._gi_verb_pattern, gr_gi_tuple[1])
        
        #* [pronome reto -> verbo -> pronome reto]
        if search_pattern_agent_verb:
            
            # Creates new phrases for each pattern
            for i, patterns_in_phrase in enumerate(search_pattern_agent_verb):
                gr,gi = self.new_patterns(patterns_in_phrase, 
                                          gi_verbs[i],
                                          norm = 1)
                
                new_patterns_gr.append(gr)
                new_patterns_gi.append(gi)          
                
        # [pronome reto -> pronome obliquo -> verbo]
        if search_pattern_pronoun_verb:
            
            # Creates new phrases for each pattern
            for i, patterns_in_phrase in enumerate(search_pattern_pronoun_verb):
                gr,gi = self.new_patterns(patterns_in_phrase,
                                     gi_verbs[i],
                                     norm = 2)
                
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
                new_patterns_gr.append(gr)
                new_patterns_gi.append(gi)            
        
              
        try:
            # Combinating patterns of the newly created phrases
            combination_patterns_gr = product(*new_patterns_gr)
            combination_patterns_gi = product(*new_patterns_gi)
            
<<<<<<< HEAD
            for combination_gr in combination_patterns_gr:
                # New Patterns for GI 
                combination_gi = next(combination_patterns_gi)
=======
        # Combinating patterns of the newly created phrases
        combination_patterns_gr = product(*new_patterns_gr, repeat=1)
        combination_patterns_gi = product(*new_patterns_gi, repeat=1)
        try: 
            for item_gr in combination_patterns_gr:
                
                # New Patterns for GI 
                item_gi = next(combination_patterns_gi)
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
                
                # Generates new phrases [befores_string + pattern + after_string] 
                # if the following pattern is encountered 
                # [pronome reto -> pronome obliquo -> verbo]
<<<<<<< HEAD
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
=======
                if search_pattern_pronoun_verb:
                    new_phrases.append(self.assembly_phrase(gr_gi_tuple,
                                                agent_verb = search_pattern_pronoun_verb,
                                                combination_gr = item_gr,
                                                combination_gi = item_gi))
                
                # Generates new phrases [befores_string + pattern + after_string] 
                # if the following pattern is encountered 
                # [pronome reto -> verbo -> pronome reto]
                if search_pattern_agent_verb:
                    new_phrases.append(self.assembly_phrase(gr_gi_tuple,
                                            agent_verb = search_pattern_agent_verb,
                                            combination_gr = item_gr,
                                            combination_gi = item_gi)) 
        except:
            print('No pattern was found')
            return None
        
        # Shuffle to return {limit ( default_val = 50 )} random phrases
        random.shuffle(new_phrases)
        return new_phrases[:limit]
    
    
    def process(self,data,limit=50):
        # Used to do the augmentation in phrases
        new_phrases = []
        for phrase in data:
            new_phrases.extend(self.augmentation(phrase, limit=limit))
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
            
        return new_phrases 