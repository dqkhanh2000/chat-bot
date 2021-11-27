from sklearn import svm
from lib import *
import numpy as np
x = read_svm_file("svm_data.txt")
y = read_svm_file("svm_label.txt")
m = svm.SVC()
m.fit(x, y)
model = load_model("model/model.bin")
data = load_json_data("question.json")

while True:
  sent = input("you: ")
  sent = process_sentence(sent)
  vec = model.get_sentence_vector(sent).tolist()
  id = m.predict([vec])[0]
  print(id)
  # print(f'bot: {data[id-1]["answer"][0]}')