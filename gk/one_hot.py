from nltk import word_tokenize

def create_vocabularies(data):
    list_distint_words = []
    for word in data:
        if word not in list_distint_words:
            list_distint_words.append(word)
    vocabularies = {}
    for index, word in enumerate(list_distint_words):
        vocabularies[word] = index
    return vocabularies

def get_onehot_vector(sentence, vocabulary):
    onehot = []
    for word in sentence.split():
        onehot_word = [0] * len(vocabulary)
        if word in vocabulary:
            onehot_word[vocabulary[word]] = 1
        onehot.append(onehot_word)
    return onehot

raw = "The chance for the two leaders to speak privately may also have addressed US frustration about the quality of communication with Chinese officials."


