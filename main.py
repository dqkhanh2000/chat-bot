import underthesea
import re

def split_sentence(data):
  result = []
  list_sent = underthesea.sent_tokenize(data)
  for sent in list_sent:
      sent = sent.lower()
      sent = re.sub(r'[!@#$%^&*()_+\/\d\.\,;:\'"`~\\\?-]', '', sent)
      result.append(sent)
  return result
      
      

def list_word(list_sent, stop_word):
    list_word = []
    for sent in list_sent:
       for word in underthesea.word_tokenize(sent):
           if word not in stop_word:
               list_word.append(word)
    return list_word

# loading stop word
def loading_stopWord():
    stopWord = []    
    with open('./Data/stopWord.txt', 'r', encoding='utf-8') as f:
        for s_line in f:
            stopWord.append(s_line.strip())
    return stopWord

    
# -*- coding: utf-8 -*-
if __name__ == '__main__':  
    f = open("./Data/data.txt", "r", encoding='utf-8')
    rawdata = f.read()
    list_sent = split_sentence(rawdata)
    stopWord = loading_stopWord()
    list_word = list_word(list_sent, stopWord)
    print(list_word)