import re
from underthesea import word_tokenize
from unidecode import unidecode
import os
if __name__ == "__main__":
    os.system("cls")
    raw = '= + Sau khi & & được GIẢI PHÓNG VÀO ( ) < > . , & * = + NGÀY 10 THÁNG  10 NĂM 1954, Hà  NỘI TRỞ THÀNH thủ đô của ! # $ ^ Việt Nam Dân chủ Cộng hòa & +.'
    processed = re.sub('[()<>.,!#$^&*=+]','',raw).strip().lower()
    processed = re.sub('[\s]{2,}',' ',processed)
    print(f"clean: {processed}")
    print(f"word tokenization: {word_tokenize(processed)}")
    print(f"no unicode: {unidecode(processed)}")