import os
import multiprocessing
import json

path = "./data"
root_folder = os.listdir(path)

list_path = []
for folder in root_folder:
  if(folder.find(".txt") != -1):
    continue
  folder_path = path+"/"+folder
  list_file = os.listdir(folder_path)
  print(len(list_file))
  if len(list_file) < 13:
    continue
  for index, file in enumerate(list_file):
    if index > 14:
      break
    file_path = folder_path+"/"+file
    list_path.append(file_path)

def process_line(line):
  sent = ''
  try:
    sents = json.loads(line)
    for word in sents:
      sent += word.replace(" ", "_") + " "
  except:
    print("LỖI RỒI ANH ƠI: "+ line)
  sent.strip()
  return sent

def process_data(file_path, output_file):  
  file = open(file_path, "r")
  lines = file.readlines()
  length = len(lines)
  tmp = file_path.split("/")
  file_name = tmp[len(tmp)-1]
  for i, line in enumerate(lines):
   # print(f"write {i}/{length} of file {file_name}")
    sent = process_line(line)
    if len(sent) < 1:
      continue
    output_file.write( sent.strip() +"\n")
  file.close()

print(list_path)
output_file = open(path+"/data.txt", "w", encoding="utf-8")
length = len(list_path)
for index,file in enumerate(list_path):
  print(f"process file {file} {index}/{length}")
  process_data(file, output_file)
print("XONG RỒI MẤY ANH ƠI")
output_file.close() 