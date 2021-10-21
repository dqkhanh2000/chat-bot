from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


D1 = "Dog bites man."
D2 = "Man has run."

D1_processed = D1.lower().replace(".", "")
D2_processed = D2.lower().replace(".", "")
process_data = [D1_processed, D2_processed]

count_vect = CountVectorizer(ngram_range=(1, 3))
tfidf = TfidfVectorizer()
bow_rep = count_vect.fit_transform(process_data)
bow_rep_tfidf = tfidf.fit_transform(process_data)
print("Vocabulary: ", count_vect.vocabulary_)
print(tfidf.idf_)
print(tfidf.get_feature_names())
bag_of_gram_D1 = count_vect.transform([D1_processed])
print(bag_of_gram_D1.toarray())

print(tfidf.fit_transform([D1_processed]).toarray())