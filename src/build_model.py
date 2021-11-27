# -*- coding: utf-8 -*-
from gensim.models.fasttext import FastText
import json

# path data
pathdata = './output/data.txt'

def read_data(path):
    train_data = []
    sents = open(path, 'r').readlines()
    for sent in sents:
        if len(sent) < 4:
            continue
        train_data.append(json.loads(sent))
    return train_data

if __name__ == '__main__':
    train_data = read_data(pathdata)

    model_fasttext = FastText(window=10, min_count=2, workers=4, sg=1)
    model_fasttext.build_vocab(train_data)
    model_fasttext.train(train_data, total_examples=model_fasttext.corpus_count, epochs=10)

    model_fasttext.wv.save("./model/fasttext_gensim.model")
