from underthesea  import word_tokenize
import re
import json
import time
import fasttext

STOP_WORD = []

def loading_stop_word():
    stopWord = []    
    with open('./stop_word.txt', 'r', encoding='utf-8') as f:
        for s_line in f:
            stopWord.append(s_line.strip())
    return stopWord

def process_sentence(sentence):
  global STOP_WORD
  if(len(STOP_WORD) == 0):
    STOP_WORD = loading_stop_word()
  words = ''
  for word in word_tokenize(sentence.lower()):
      word = re.sub(r'[^\s^a-z^đ^ý^ỳ^ỷ^ỹ^ỵ^ú^ù^ủ^ũ^ụ^ư^ứ^ừ^ử^ữ^ự^í^ì^ỉ^ĩ^ị^á^à^ả^ã^ạ^ă^ắ^ằ^ẳ^ẵ^ặ^â^ấ^ầ^ẩ^ẫ^ậ^é^è^ẻ^ẽ^ẹ^ê^ế^ề^ể^ễ^ệ^ó^ò^ỏ^õ^ọ^ô^ố^ồ^ổ^ỗ^ộ^ơ^ớ^ờ^ở^ỡ^ợ]', '', word)
      word = word.strip()
      if (" " not in word and len(word) > 7) or (len(word) == 0):
              continue
      # if word not in STOP_WORD:
      words += word.replace(" ", "_") + " "
  # print(words)
  return words.strip()

def process_vec(vec):
  output = ''
  for i, dimen in enumerate(vec):
      output += f'{i+1}:{dimen} '
  return output

def load_json_data(json_path):
  file = open(json_path, "r", encoding="utf-8")
  data = json.load(file)
  file.close()
  return data

def read_svm_file(path):
  file = open(path, "r")
  list = file.readlines()
  data = []
  for line in list:
    data.append(json.loads(line))
  return data

def load_model(model_path):
  print("LOADING WORD2VEC MODEL")
  start_time = time.time()
  model = fasttext.load_model(model_path)
  print(f"LOAD DONE {time.time() - start_time}s")
  return model