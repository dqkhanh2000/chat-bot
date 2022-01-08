import json
from lib import *
from constant import *


def process_question(label_file, data_file, question_object, model, index_obj, print_log):
    id = question_object["id"]
    if index_obj.count(id) == 0:
        index_obj.append(id)
        
    questions = question_object["question"]
    if(print_log):
        print("--------")
    for question in questions:
        sentence = process_sentence(question)
        if(print_log):
            print(sentence)
        # if len(sentence) == 0:
        #     continue
        vec = model.get_sentence_vector(sentence).tolist()
        # vec = create_sentence_vec(model, sentence)
        label_file.write(f"{index_obj.index(id)}\n")
        data_file.write(f"{json.dumps(vec)}\n")
        
def process_classification_data(print_log = True):
    model = load_word2vec_model(WORD2VEC_MODEL_PATH)
    label_file = open(f"{CLASSIFICATION_DATA_PATH}/label.txt", "w")
    index_file = open(f"{CLASSIFICATION_DATA_PATH}/index.txt", "w")
    index_obj = []
    data_file = open(f"{CLASSIFICATION_DATA_PATH}/vec.txt", "w")
    data = load_json_data(f"{CLASSIFICATION_DATA_PATH}/question.json")
    for question_object in data:
        sent = process_question(label_file, data_file, question_object, model, index_obj, print_log)
        # break
    index_file.write(f"{json.dumps(index_obj)}\n")

if __name__ == "__main__":
    process_classification_data(False)
