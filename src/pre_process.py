import json
from underthesea  import word_tokenize
import re
import time
from langdetect import detect
import threading
import math
import io

path = "./"

def split_sent_to_word(sentence, stop_word):
    words = []
    for word in word_tokenize(sentence):
        word = re.sub(r'[^\s^a-z^đ^ý^ỳ^ỷ^ỹ^ỵ^ú^ù^ủ^ũ^ụ^ư^ứ^ừ^ử^ữ^ự^í^ì^ỉ^ĩ^ị^á^à^ả^ã^ạ^ă^ắ^ằ^ẳ^ẵ^ặ^â^ấ^ầ^ẩ^ẫ^ậ^é^è^ẻ^ẽ^ẹ^ê^ế^ề^ể^ễ^ệ^ó^ò^ỏ^õ^ọ^ô^ố^ồ^ổ^ỗ^ộ^ơ^ớ^ờ^ở^ỡ^ợ]', '', word)
        word = word.strip()
        if (" " not in word and len(word) > 7) or (len(word) == 0):
                continue
        if word not in stop_word:
            
            words.append(word.lower())
    return words

def create_vocab(document, stop_word, start_line = 0):
    line = -1
    count = -1
    print("-----------------------------------------------------")
    print("OPENING OUTPUT FILE")
    file_index = -1
    file_name = path + "/output/word_" + str(file_index) + ".txt"
    stop = 10000

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

def run_in_thread(start_line, end_line, path, file_name, document, stop_word):
    # output_data = open(path+"/output/"+file_name+".txt", "wb")
    output_info = open(path+"/thread_info/"+file_name+"info.txt", "w")
    output_data = io.FileIO(path+"/output/"+file_name+".txt", 'w')
    writer = io.BufferedWriter(output_data,buffer_size=100000000)

    print(f"START PROCESS {file_name}............")
    start_time = time.time()

    for line in range(start_line, end_line+1):
        if line < len(document):
            sentence = document[line]
            
            output_info.write(f"Processing line {line}\n")

            sentence = sentence.lower()
            words = split_sent_to_word(sentence, stop_word)
            if(len(words) == 0):
                continue
            s = json.dumps(words, ensure_ascii=False)
            writer.write(f"{s}\n")
            writer.flush()

    end_time = time.time()
    duration = end_time - start_time
    print(f"write to {file_name} in {duration} seconds")
    writer.close()
    output_data.close()
    output_info.close()

if __name__ == "__main__":

    start_time = time.time()
    print("OPENING DATA FILE...")
    file = open("./data/a.txt", "r")
    print("READING DATA FILE...")
    data = file.readlines()
    end_time = time.time()
    duration = end_time - start_time
    print(f"READ DATA DONE (in {duration})")

    start_time = end_time
    stop_word = loading_stopWord()
    # words = create_vocab(data, stop_word)
    # end_time = time.time()
    # duration = end_time - start_time
    # print(f"DONE (in {duration})")

    threads = []
    total_line = len(data)
    line_in_file = 10000
    total_file = math.floor(total_line/line_in_file) +1
    print(total_file)

    for index in range(0, total_file):
        start_line = index * line_in_file
        end_line = start_line + line_in_file
        file_name = f"word_{index}"
        t = threading.Thread(target=run_in_thread, args=(start_line, end_line, path, file_name, data, stop_word, ))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


    end_time = time.time()
    duration = end_time - start_time
    print(f"DONE (in {duration})")

 