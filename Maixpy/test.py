text_list = "this is a sentence use to test the specail enviroment of K210"
sentence_list = []
sentence = ""
singel_letter = 0
for word in text_list:
    singel_letter += len(word) + 1
    if singel_letter < 30:
        sentence = sentence +  word + " "
    else:
        sentence_list.append(sentence)
        singel_letter = 0
        sentence = ""
        sentence = sentence +  word + " "

print(sentence_list)