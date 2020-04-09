from directionality import Directionality_Augmentation

# Frases para testes 
phrases = [('EU TE MOSTRAR CIDADE [PONTO]', '1S_MOSTRAR_2S CIDADE [PONTO]'),
           ('ELE PEDIR ELA SE ELA CONHECER [PONTO]', '3S_PERGUNTAR_3S CONHECER [PONTO]')]

da = Directionality_Augmentation()

words_list = da.process(phrases, limit=50)
print(words_list)

count = 0
for element in words_list:   
    for words in element:
        count += 1
        print(words)

print(count)