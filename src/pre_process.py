import json
from underthesea  import word_tokenize
import re
import time
from langdetect import detect

path = "./"

def split_sent_to_word(sentence, stop_word):
    words = []
    for word in word_tokenize(sentence):
        word = re.sub(r'[^\s^a-z^đ^ý^ỳ^ỷ^ỹ^ỵ^ú^ù^ủ^ũ^ụ^ư^ứ^ừ^ử^ữ^ự^í^ì^ỉ^ĩ^ị^á^à^ả^ã^ạ^ă^ắ^ằ^ẳ^ẵ^ặ^â^ấ^ầ^ẩ^ẫ^ậ^é^è^ẻ^ẽ^ẹ^ê^ế^ề^ể^ễ^ệ^ó^ò^ỏ^õ^ọ^ô^ố^ồ^ổ^ỗ^ộ^ơ^ớ^ờ^ở^ỡ^ợ]', '', word)
        word = word.strip()
        if (" " not in word and len(word) > 7) or (len(word) == 0):
                continue
        if word not in stop_word and detect(word) == 'vi':
            
            words.append(word.lower())
    return words

def create_vocab(document, stop_word, start_line = 0):
    line = -1
    count = -1
    print("-----------------------------------------------------")
    print("OPENING OUTPUT FILE")
    file_index = -1
    file_name = path + "/output/word_" + str(file_index) + ".txt"
    stop = 500

    output = False

    start_time = time.time()
    for line in range(start_line, len(document)):
        sentence = document[line]
        count += 1
        if( line < start_line):
            continue
        print(f"Processing line {line}")
        if (line % stop == 0 or count > stop or output == False) :

            end_time = time.time()
            duration = end_time - start_time
            start_time = end_time

            if(output):
                print(f"write {count} line to {file_name} in {duration} seconds")
                output.close()
            
            file_index = int(line/stop)
            file_name = path + "/output/word_" + str(file_index) + ".txt"
            if count != stop:
                output = open(file_name, "a", encoding="utf-8")
            else :
                output = open(file_name, "w", encoding="utf-8")

            count = 0
        sentence = sentence.lower()
        words = split_sent_to_word(sentence, stop_word)
        if(len(words) == 0):
            continue
        s = json.dumps(words, ensure_ascii=False)
        output.write(f"{s}\n")
    output.close()

def loading_stopWord():
    stopWord = []    
    with open('./stop_word.txt', 'r', encoding='utf-8') as f:
        for s_line in f:
            stopWord.append(s_line.strip())
    return stopWord


if __name__ == "__main__":

    start_time = time.time()
    print("OPENING DATA FILE...")
    file = open("./data/demo-full.txt", "r")
    print("READING DATA FILE...")
    data = file.readlines()
    end_time = time.time()
    duration = end_time - start_time
    print(f"READ DATA DONE (in {duration})")

    stop_word = loading_stopWord()
    words = create_vocab(data, stop_word, 342)

 