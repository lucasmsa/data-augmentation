import re
from itertools import product, combinations

regex_latin ='[A-ZÁÉÍÓÚÀÂÊÔÃÕÜÇa-záéíóúàâêôãõüç]+'

# agentes
agent_pattern = r'\b(EU|TU|ELE|ELA|NÓS|VÓS|ELES|ELAS)\b'


agents_dict = {

    '1S': ['EU'],
    '2S': ['TU'], 
    '3S': ['ELE', 'ELA'],
    '1P': ['NÓS'],
    '2P': ['VÓS'],
    '3P': ['ELES', 'ELAS']

}
# verbos
verb_pattern = r'\b({0}R)\b'.format(regex_latin)
# pronome obliquo atono
pronoun_pattern = r'\b(ME|TE|LHE|VOS|NOS|LHES)\b'

pronouns_dict = {

    'ME': '1S',
    'TE': '2S',
    'LHE':'3S',
    'NOS': '1P',
    'VOS': '2P',
    'LHES': '3P',
    '1S': 'ME',
    '2S': 'TE',
    '3S': 'LHE',
    '1P': 'NOS',
    '2P': 'VOS',
    '3P': 'LHES'

}

pattern_agent_verb = "%s %s %s" %(agent_pattern, verb_pattern, agent_pattern)
pattern_pronoun_verb = "%s %s %s" %(agent_pattern, pronoun_pattern, verb_pattern)

phrases = ['EU ME REMEXER MUITO', 'OI EU ABRAÇAR TU PASSARO TU TRABALHAR EU QUIMO', 'NOSSA EU ABRAÇÉRAAR ELE BALEIA', 'COALA CAPIM EU ABRAÇAR VÓS ANIMAL']

behind_ahead = r'(.+){0}(.+)'.format(pattern_agent_verb)
search_pattern_agent_verb = re.findall(pattern_agent_verb, phrases[1])
search_results = re.finditer(behind_ahead, phrases[1])

#print(search_pattern_agent_verb[0])

list_new_phrases_s = []
list_new_phrases_noun = []

phrases = ['OI EU ABRAÇAR TU PASSARO TU TRABALHAR EU QUIMO']
for phrase in phrases:

  # resultado do regex para o padrão [agente -> verbo -> receptor]
  search_pattern_agent_verb = re.findall(pattern_agent_verb, phrase)
  # resultado do regex para o padrão [agente -> pronome -> verbo]
  search_pattern_pronoun_verb = re.findall(pattern_pronoun_verb, phrase)
  #print("--> ", search_pattern_agent_verb)

  if search_pattern_agent_verb:
    # para cada padrão encontrado na frase
    for patterns_in_phrase in range(len(search_pattern_agent_verb)):
          
      # TODO: vou receber uma frase no padrão [('EU', 'ABRAÇAR', 'TU'), ('TU', 'TRABALHAR', 'EU')], fazer um regex para 
      # TODO: reconhecer o padrão do search_pattern_agent_verb e agrupar em look-behind e look-ahead, e estes serao usados 
      # TODO: na criação da frase tratada
      
      '''Transformando a padrão em search_pattern_agent_verb em string para pesquisar a parte de trás e da frente do padrão'''
      string = ''
      for index, part in enumerate(search_pattern_agent_verb[patterns_in_phrase]):
          if not index:
            string +=part
          else:
              string += ' '+part
      
      # padrão para o reconhecimento das partes de trás e da frente do padrão 
      ###behind_ahead = r'(.+){0}(.+)'.format(pattern_agent_verb)
      behind_ahead = r'(.+){0}(.+)'.format(string)

      behind_ahead_results = re.findall(behind_ahead, phrase)
      #print("behind_ahead<-- ", behind_ahead_results)

      # partes de trás
      before_pattern = behind_ahead_results[0][0]
      # verbo
      verb = search_pattern_agent_verb[patterns_in_phrase][1]
      # parte após o padrão 
      after_pattern = behind_ahead_results[0][-1]

      # combinação com todos as possibilidades do dicionário
      combinations = product(agents_dict.keys(), agents_dict.keys(), repeat=1)

      for item in combinations:
        # criação de frases do tipo [1S, 2S ...]
        list_new_phrases_s.append(f'{before_pattern} {item[0]} {verb} {item[1]} {after_pattern}')

        # criação de frases do tipo [EU, TU ...]
        # os for's são necessários nos casos de [ELE, ELA, ELES ELAS]
        for index_1, item_1  in enumerate(agents_dict[item[0]]):

          for index_2, item_2 in enumerate(agents_dict[item[1]]):

            list_new_phrases_noun.append(f'{before_pattern}{item_1} {verb} {item_2}{after_pattern}')

    #elif search_pattern_pronoun_verb:
for item in list_new_phrases_noun:
    print(item)
print(len(list_new_phrases_noun))
