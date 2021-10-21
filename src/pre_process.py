from underthesea  import word_tokenize
import re

def split_sent_to_word(sentence):
    words = []
    for word in word_tokenize(sentence):
        words.append(word.lower())
    return words


def split_to_sentences(document):
    result = []
    for sentence in document:
        sentence = sentence.lower()
        sentence = re.sub(r'[!@#$%^&*()_+\/\d\.\,;:\'"`~\\\?-]', '', sentence)
        result.extend(split_sent_to_word(sentence))
    return result

def loading_stopWord():
    stopWord = []    
    with open('./Data/stopWord.txt', 'r', encoding='utf-8') as f:
        for s_line in f:
            stopWord.append(s_line.strip())
    return stopWord

if __name__ == "__main__":
  file = open("demo-full.txt", "r")
  data = file.readlines()

  words = split_to_sentences(data)
  print(words)

 