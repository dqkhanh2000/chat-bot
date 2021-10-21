import math

def tf (word, doc):
    list_world = doc.lower().replace(".", "").split()
    count = list_world.count(word.lower().replace(".", ""))
    return count/len(list_world)

def idf (word, data_processed):
    total_doc = len(data_processed)
    total_doc_has_word = 0
    for doc in data_processed:
        if doc.count(word.lower().replace(".", "")) > 0:
            total_doc_has_word += 1
    return math.log(total_doc/total_doc_has_word)

def tf_idf_word (word, doc, data_processed):
    return tf(word, doc) *  idf(word, data_processed)

def tf_idf_doc (doc, data_processed):
    list_world = []
    for word in doc.lower().replace(".", "").split():
        if word not in list_world:
            list_world.append(word)
    
    vect = [tf_idf_word(word, doc, data_processed) for word in list_world]
    return vect

def tf_idf (data_processed):
    vect = []
    for doc in data_processed:
        vect.extend(tf_idf_doc(doc, data_processed))
    return vect

if __name__ == "__main__":
    D1 = "Dog bites man."
    D2 = "Man has run."
    D1_processed = D1.lower().replace(".", "")
    D2_processed = D2.lower().replace(".", "")
    process_data = [D1_processed, D2_processed]

    word = "friendship"
    print(f"tf idf of {word} in D1: tf={tf(word, D1_processed)}, idf={idf(word, process_data)}, tf_idf={tf_idf_word(word, D1_processed, process_data)}")
    print(f"tf idf of {D1_processed}: tf_idf={tf_idf_doc(D1_processed, process_data)}")
    print(f"tf idf of data: tf_idf={tf_idf(process_data)}")