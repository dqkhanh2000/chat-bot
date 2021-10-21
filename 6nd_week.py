from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk import word_tokenize,sent_tokenize, pos_tag
from nltk.corpus import stopwords
from spellchecker import SpellChecker
from nltk.stem import PorterStemmer, WordNetLemmatizer
from unidecode import unidecode
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

spell = SpellChecker()
ps = PorterStemmer()
lemma = WordNetLemmatizer()

def split_to_sentences(data):
    document = sent_tokenize(data)
    result = []
    for sentence in document:
        sentences = ''
        for word in sentence:
            sentences += word.lower()
        result.append(sentences)
    return result

def split_data_to_word(data):
    words = []
    for sentence in data: 
        words.extend(word_tokenize(sentence))
    return words

def split_sent_to_word(sentence):
    words = []
    for word in word_tokenize(sentence):
        words.append(word.lower())
    return words

def remove_stop_word(data):
    document = []
    stop_words = []
    for word in data:
        if word not in stopwords.words():
            document.append(word.lower())
        else:
            if word.lower() not in stop_words:
                stop_words.append(word.lower())
    return (document, stop_words)

def spell_check_and_correction(list_word):
    words = []
    incorrect_words = []
    for word in list_word:
        word_after_correction = spell.correction(word)
        if word_after_correction != word:
            incorrect_words.append(word)
        words.append(word_after_correction)
    return (words, incorrect_words)

def steming(list_word):
    stem_word_list = []
    for word in list_word:
        stem_word_list.append(ps.stem(word))
    return stem_word_list

def lemmazation(list_word):
    lemma_word_list = []
    for word in list_word:
        lemma_word_list.append(lemma.lemmatize(word))
    return lemma_word_list

def create_pos_tag(list_word):
    return pos_tag(list_word)

def remove_special_charactor(list_word):
    list = []
    for word in list_word:
        new_word = re.sub('[^(\w|\d|\s)]', ' ', word)
        list.append(new_word)
    return list

def pre_processing_sentences(sentences):
    list_words = split_sent_to_word(sentences)
    list_words, _ = spell_check_and_correction(list_words)
    list_words = remove_special_charactor(list_words)
    list_words = lemmazation(list_words)

    return list_words

def Vietnamese_without_accents(data):
    return unidecode(data)

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

def one_hot_encoding(list_sent, vocabulary):
    
    one_hots = []
    for sentence in list_sent:
        sentence_one_host = get_onehot_vector(sentence, vocabulary)
        one_hots.append(sentence_one_host)
    return one_hots

def bag_of_word(list_sent, vocabulary):
    bag_of_words = []
    for sentence in list_sent:
        sent_vector = [0] * len(vocabulary)
        processed_word = pre_processing_sentences(sentence)
        for word in processed_word:
            if word in vocabulary:
                index = vocabulary[word]
                sent_vector[index] += 1
        print(sent_vector)
        bag_of_words.append(sent_vector)
    
    return bag_of_words   

def bag_of_n_gram(list_sent):
    process_data = [doc.lower().replace(".", "") for doc in list_sent]
    count_vect = CountVectorizer(ngram_range=(1, 3))
    bow_rep = count_vect.fit_transform(process_data)
    print("Our vocabulary: ", count_vect.vocabulary_)
    print("BoW representation for first sentence: ", bow_rep[0].toarray())

def TF_IDF(list_sent):
    process_data = [doc.lower().replace(".", "") for doc in list_sent]
    tfidf = TfidfVectorizer()
    bow_rep_tfidf = tfidf.fit_transform(process_data)
    # IDF for all words in the vocabulary
    print("IDF for all words in the vocabulary", tfidf.idf_)
    print("-" * 10)
    # All words in the vocabulary.
    print("All words in the vocabulary", tfidf.get_feature_names())
    print("-" * 10)

    print("TFIDF representation for all documents in our corpus\n", bow_rep_tfidf.toarray())
    print("-" * 10)

def Word2Vec(list_sent):
    process_data = [doc.lower().replace(".", "") for doc in list_sent]
    tagged_data = [TaggedDocument(words=word_tokenize(word.lower()), tags=[str(i)]) for i, word in enumerate(process_data)]
    model_dbow = Doc2Vec(tagged_data, vector_size=20, min_count=1, epochs=2, dm=0)
    print(model_dbow.infer_vector(['V. League']))  # feature vector of man eats food

if __name__ == '__main__':
    f = open("english_data.txt", "r")
    raw = f.read()
    # data = pre_processing(raw)
    sent_token = split_to_sentences(raw)
    # print(sent_token)
    # word_token = split_data_to_word(sent_token)

    # data, stop_words = remove_stop_word(word_token)
    # print(data)
    # print(stop_words)
    # data, incorect_words = spell_check_and_correction(data)
    # print(data)
    # print(incorect_words)

    # data = remove_special_charactor(data)
    # print(data)

    # pos_tag = create_pos_tag(data)
    # print(pos_tag)

    # stems = steming(data)
    # print(stems)
    # data = lemmazation(data)
    # # print(data)

    # vocabulary = create_vocabularies(data)
    # # print(vocabulary)

    # one_hot = one_hot_encoding(sent_token, vocabulary)
    # # print(one_hot)
    # bag_of_words = bag_of_word(sent_token, vocabulary)
    # # bag_of_n_gram(sent_token)
    # # TF_IDF(sent_token)
    print(Word2Vec(sent_token))