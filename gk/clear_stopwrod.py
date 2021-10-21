import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

lemma = WordNetLemmatizer()

def remove_stop_word (list_word):
    removed_stop_words = []
    stop_words = []
    for word in list_word:
        if word not in stopwords.words():
            removed_stop_words.append(word)
        else:
            if word not in stop_words:
                stop_words.append(word)
    return (removed_stop_words, stop_words)

def create_vocabularies(list_words):
    list_distint_words = []
    for word in list_words:
        if word not in list_distint_words:
            list_distint_words.append(word)
    vocabularies = {}
    for index, word in enumerate(list_distint_words):
        vocabularies[word] = index
    return vocabularies

def process_sentence(sentence):
    processed = sentence.lower().replace(".", "")
    word_tokens = word_tokenize(processed)
    lematizations = [lemma.lemmatize(word) for word in word_tokens]
    return lematizations

def get_onehot_vector(sentence, vocabulary):
    list_word = process_sentence(sentence)
    onehot = []
    for word in list_word:
        onehot_word = [0] * len(vocabulary)
        if word in vocabulary:
            onehot_word[vocabulary[word]] = 1
        onehot.append(onehot_word)
    return onehot

def get_bag_of_word_vector(sentence, vocabulary):
    list_word = process_sentence(sentence)
    vector = [0] * len(vocabulary)
    for word in list_word:
        if word in vocabulary:
            vector[vocabulary[word]] += 1
    return vector

if __name__ == "__main__":
    os.system('cls||clear')
    raw = "The chance for the two leaders to speak privately may also have addressed US frustration about the quality of communication with Chinese officials."
    print("The raw documnet:")
    print(raw)
    processed = raw.lower().replace(".", "")
    word_tokens = word_tokenize(processed)

    removed_stop_words, stop_words = remove_stop_word(word_tokens)
    print(f"stop word has removed: {stop_words}")
    print(f"list word after remove stop word: {removed_stop_words}")
    
    lematizations = [lemma.lemmatize(word) for word in removed_stop_words]
    print(f"list word after lematizations: {removed_stop_words}")

    tagged = pos_tag(lematizations)
    print(f"list word with pos tag: {tagged}")

    vocab = create_vocabularies(lematizations)

    sentence = "The chance for the two leaders to speak privately"
    one_hot = get_onehot_vector(sentence, vocab)
    bow = get_bag_of_word_vector(sentence, vocab)

    print(f"the vocabularies: {vocab}")
    print(f"the sentence: {sentence}")


    print(f"vectore one hot of the sentence{one_hot}")
    print(f"vectore bag of word of the sentence{bow}")