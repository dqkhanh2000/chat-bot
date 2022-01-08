import json
from underthesea import word_tokenize
import re
import time
import multiprocessing
import math
import os
import getopt
import sys


path = "./"


def split_sent_to_word(sentence, stop_word = ""):
    words = ''
    for word in word_tokenize(sentence):
        word = re.sub(
            r'[^\s^a-z^đ^ý^ỳ^ỷ^ỹ^ỵ^ú^ù^ủ^ũ^ụ^ư^ứ^ừ^ử^ữ^ự^í^ì^ỉ^ĩ^ị^á^à^ả^ã^ạ^ă^ắ^ằ^ẳ^ẵ^ặ^â^ấ^ầ^ẩ^ẫ^ậ^é^è^ẻ^ẽ^ẹ^ê^ế^ề^ể^ễ^ệ^ó^ò^ỏ^õ^ọ^ô^ố^ồ^ổ^ỗ^ộ^ơ^ớ^ờ^ở^ỡ^ợ]', '', word)
        word = word.strip()
        if (" " not in word and len(word) > 7) or (len(word) == 0):
            continue
        # if word not in stop_word:

        words += word.replace(" ", "_") + " "
    return words.strip()


def create_vocab(document, stop_word, start_line=0):
    line = -1
    count = -1
    print("-----------------------------------------------------")
    print("OPENING OUTPUT FILE")
    file_index = -1
    file_name = path + "/output/word_" + str(file_index) + ".txt"
    stop = 20000000

    output = False

    start_time = time.time()
    for line in range(start_line, len(document)):
        sentence = document[line]
        count += 1
        if(line < start_line):
            continue
        print(f"Processing line {line}")
        if (line % stop == 0 or count > stop or output == False):

            end_time = time.time()
            duration = end_time - start_time
            start_time = end_time

            if(output):
                print(
                    f"write {count} line to {file_name} in {duration} seconds")
                output.close()

            file_index = int(line/stop)
            file_name = path + "/output/word_" + str(file_index) + ".txt"
            if count != stop:
                output = open(file_name, "a", encoding="utf-8")
            else:
                output = open(file_name, "w", encoding="utf-8")

            count = 0
        sentence = sentence.lower()
        words = split_sent_to_word(sentence, stop_word)
        if(len(words) == 0):
            continue
    # s = json.dumps(words, ensure_ascii=False)
    output.write(f"{words}\n")
    output.close()


def loading_stopWord():
    stopWord = []
    with open('./stop_word.txt', 'r', encoding='utf-8') as f:
        for s_line in f:
            stopWord.append(s_line.strip())
    return stopWord


def process_file(file_name, file_path, output_path, debug, max_line = 2000000):
    
    print(f"OPENING {file_name}...")
    start_time = time.time()
    file_data = open(file_path, "r", encoding="utf-8")
    print(f"READING {file_name}...")
    end_time = time.time()
    duration = end_time - start_time
    print(f"READ {file_name} DONE (in {duration})")
    
    output_file = open(output_path, "w", encoding="utf-8")

    if debug:
        print(f"START PROCESS {file_name}............")
        start_time = time.time()
    i = 0
    for i in range(max_line):
        line = file_data.readline()
        sentence = line.lower()
        words = split_sent_to_word(sentence)
        if(len(words) == 0):
            continue
        # s = json.dumps(words, ensure_ascii=False)
        output_file.write(f"{words}\n")
        i+=1
        if debug:
            sys.stdout.write('\r')
            percent = math.ceil(i / max_line * 100)
            sys.stdout.write(f"[{'='*int(percent/5):<20}] {percent}% {i}/{max_line} line")
            sys.stdout.flush()

    if debug:
        end_time = time.time()
        duration = end_time - start_time
        print(f"write to {file_name} in {duration/60} minutes")
    file_data.close()
    output_file.close()

def get_arg(argv):
    input_path = ''
    output_path = ''
    debug = False
    try:
        opts, args = getopt.getopt(argv,"hi:o:d",["input=","output=", "debug="])
    except getopt.GetoptError:
        print ('pre_process.py -i <input_folder> -o <output_file> -d <debug>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('pre_process.py -i <input_folder> -o <output_file>  -d <debug>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_path = arg
        elif opt in ("-o", "--output"):
            output_path = arg
        elif opt in ("-d", "--debug"):

            debug = True
            
            
    input_folder = "./data/" if input_path == '' else input_path
    output_file = "./output" if output_path == '' else output_path
    
    return (input_folder, output_file, debug)

def main(argv):
    
    input_path, output_path, debug = get_arg(argv)
    
    if not os.path.exists(input_path):
        raise Exception("Input folder does not exist")
        
    if not os.path.exists(output_path):
        os.mkdir(output_path)
        

    if os.path.isdir(input_path):
        list_file = os.listdir(input_path)
        print(f"Found {len(list_file)} in {input_path}")
        for file in list_file:
            if os.path.splitext(file)[1] != ".txt":
                continue
            data_path = os.path.join(input_path, file)
            output_file = os.path.join(output_path,file)
            process_file(file, data_path, output_file, debug)
    else :
        file = os.path.basename(input_path)
        output_file = os.path.join(output_path, file)
    
        process_file(file, input_path, output_file, debug)
        
    print("DONE")

if __name__ == "__main__":
    main(sys.argv[1:])