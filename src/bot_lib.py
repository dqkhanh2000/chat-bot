
from lib import *
from classification import predict, get_model
import numpy as np
import random
from constant import *

model = None
labels = None
question_data = None

def load_data():
  global model, question_data, labels
  model = load_word2vec_model(WORD2VEC_MODEL_PATH)
  question_data = load_json_data(f"{CLASSIFICATION_DATA_PATH}/question.json")
  labels = read_data_file(f"{CLASSIFICATION_DATA_PATH}/index.txt")
  get_model()

def get_response(sent):
  question = process_sentence(sent)
  vec = model.get_sentence_vector(question).tolist()
  index, score = predict(vec)
  answers = question_data[index]["answer"]
  answer = random.choices(answers)[0]
  js = '{"answer": "%s", "confident": %s}' % (answer, score)
  return js
  