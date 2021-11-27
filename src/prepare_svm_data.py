import json
from lib import *


def process_question(label_file, data_file, question_object, model):
    id = question_object["id"]
    questions = question_object["question"]
    print("--------")
    for question in questions:
        sentence = process_sentence(question)
        print(sentence)
        # if len(sentence) == 0:
        #     continue
        vec = model.get_sentence_vector(sentence).tolist()
        label_file.write(f"{id}\n")
        data_file.write(f"{json.dumps(vec)}\n")
        


if __name__ == "__main__":
    model = load_model("model/model.bin")
    label_file = open("svm_label.txt", "w")
    data_file = open("svm_data.txt", "w")
    data = load_json_data("question.json")
    for question_object in data:
        sent = process_question(label_file, data_file, question_object, model)
        # break
