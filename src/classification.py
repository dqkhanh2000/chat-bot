from lib import *
from sklearn.model_selection import train_test_split
from tensorflow import keras
import numpy as np
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers import Dropout, Flatten
from keras.layers.embeddings import Embedding
from prepare_classification_data import *
import os.path
from constant import *

classification_model = None

def get_model():
  global classification_model
  if classification_model is None:
    data_his = read_data_file(f"{CLASSIFICATION_DATA_PATH}/vec.txt")
    process_classification_data(print_log=False)
    data_new = read_data_file(f"{CLASSIFICATION_DATA_PATH}/vec.txt")
    has_change = False
    if len(data_his) != len(data_new):
      has_change = True
      
    else:
      for i in range(len(data_his)):
        if compare_array(data_his[i], data_new[i]):
          has_change = True
          break
    print(f"has change data: {has_change}")
    if has_change:
      model = train()
    else:
      model = load_model_from_file()
    
    classification_model = model
  else:
    model = classification_model
  return model

def train():
  data = np.array(read_data_file(f"{CLASSIFICATION_DATA_PATH}/vec.txt"))
  data = np.reshape(data, (data.shape[0], 1, data.shape[1]))
  label = np.array(read_data_file(f"{CLASSIFICATION_DATA_PATH}/label.txt"))
  num_label = len(np.unique(label))
  
  x_train, x_test, y_train, y_test = train_test_split(data, label, test_size=0.3, random_state=42)
  
  units = 128
  output_size = num_label
  
  model = Sequential()
  model.add(LSTM(units, input_shape=(1, WORD2VEC_DIM), activation='relu',return_sequences=True))
  model.add(keras.layers.BatchNormalization())
  model.add(Dropout(0.3))
  model.add(LSTM(128,activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(64,activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(32,activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(output_size,activation='softmax'))
  model.compile(
      loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
      optimizer="adam",
      metrics=["accuracy"],
  )
  model.summary()
  model.fit(
    x_train, y_train, validation_data=(x_test, y_test), batch_size=10, epochs=50
  )
  model.save(CLASSIFICATION_MODEL_PATH)
  return model
  
def load_model_from_file():
    if os.path.exists(CLASSIFICATION_MODEL_PATH):
      model = keras.models.load_model(CLASSIFICATION_MODEL_PATH)
    else:
      model = train()
    return model
  
def predict(vector):
  model = get_model()
  pred = model.predict(np.array([[vector]]))
  label = pred.argmax()
  acc = pred[0][label]
  return (label, acc)
  
  
if __name__ == "__main__":
  train()
  # w2v_model = load_word2vec_model("model/model.bin")
  # print(w2v_model.get_word_vector("0"))
  # get_model()
  # data = read_data_file("vec.txt")
  # label = read_data_file("label.txt")
  # for i in range(len(data)):
  #   print(label[i], predict(data[i]))