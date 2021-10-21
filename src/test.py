
from gensim.models import KeyedVectors

model = KeyedVectors.load("./model/fasttext_gensim.model")
a = model.most_similar(u"mẹ")

print(a)

# import gensim.models.keyedvectors as word2vec
# import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA

# import os

# model = word2vec.KeyedVectors.load('./model/fasttext_gensim.model')
# # model = word2vec.KeyedVectors.load('../model/fasttext_gensim.model')
