from sklearn import svm
from lib import *
import numpy as np
x = read_data_file("vec.txt")
y = read_data_file("label.txt")
m = svm.SVC()
m.fit(x, y)
model = load_word2vec_model("model/model.bin")
data = load_json_data("question.json")

while True:
  sent = input("input text: ")
  # sent = process_sentence(sent)
  vec = model.get_nearest_neighbors(sent)
  # id = m.predict([vec])[0]
  print(vec)
  # print(f'bot: {data[id-1]["answer"][0]}')