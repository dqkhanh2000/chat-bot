from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from lib import *
import numpy as np
import random
model = None
classifierModel = None
labels = None

def load_data():
  global model, classifierModel, data, labels
  x = read_svm_file("svm_data.txt")
  y = read_svm_file("svm_label.txt")
  classifierModel = KNeighborsClassifier(n_neighbors=5)
  classifierModel.fit(x, y)
  labels = classifierModel.classes_
  model = load_model("model/model.bin")
  data = load_json_data("question.json")

def get_response(sent):
  question = process_sentence(sent)
  vec = model.get_sentence_vector(question).tolist()
  predict_scores =  classifierModel.predict_proba([vec])[0]
  label, score = get_labels(predict_scores)
  answers = data[label-1]["answer"]
  answer = random.choices(answers)[0]
  js = '{"answer": "%s", "confident": %s}' % (answer, score)
  return js
  
def get_labels(predict_scores):
  global labels
  max_score = predict_scores[0]
  label = labels[0]
  
  for i in range(1, len(predict_scores)):
    if predict_scores[i] > max_score:
      max_score = predict_scores[i]
      label = labels[i]
    return (label, max_score)