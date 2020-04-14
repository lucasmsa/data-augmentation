from directionality import Directionality_Augmentation

test_phrases = [('EU TE MOSTRAR CIDADE [PONTO]', '1S_MOSTRAR_2S CIDADE [PONTO]'),
                ('ELE PEDIR ELA SE ELA CONHECER [PONTO]', '3S_PERGUNTAR_3S CONHECER [PONTO]'),
                ('EU TE DO_QUE CIDADE [PONTO]', '1S_DO_QUE_2S CIDADE [PONTO]')]

<<<<<<< HEAD

example = [('EU TE MOSTRAR CIDADE [PONTO] EU VOS PEDIR CIDADE [PONTO] LLLL ELE PERGUNTAR ELA SE ELA CONHECER [PONTO]',
            '1S_MOSTRAR_2S CIDADE [PONTO] 1S_PEDIR_2P CIDADE [PONTO] LLLL 3S_PERGUNTAR_3S CONHECER [PONTO]')]
example2 = [('EU TE MOSTRAR CIDADE [PONTO]',
            '1S_MOSTRAR_2S CIDADE [PONTO]')]

da = Directionality_Augmentation()

test_phrases = da.process(example2, max_new_sentences = 500000)

    
with open('example_3_patterns.txt', 'w') as f:
       for phrase in test_phrases:
            f.write(str(phrase)+'\n')
    


    
=======
da = Directionality_Augmentation()

words_list = da.process(phrases, limit=50)
print(words_list)

count = 0
for element in words_list:   
    for words in element:
        count += 1
        print(words)

print(count)
>>>>>>> 49932c578896d53ddaf801523ed511145f6fd519
