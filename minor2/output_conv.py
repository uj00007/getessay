import os

from nltk import SnowballStemmer, RegexpTokenizer, sent_tokenize
from nltk.corpus import stopwords

stop = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")


def convert(y):
    lis = []
    lis1 = []
    fp = open("SummFinal/" + y, "r", encoding="utf-8")
    fo = open("Documents/Text2/" + y, "r", encoding="utf-8")
    str1 = fp.read()
    str2 = fo.read()
    for i in str1.split('\n'):
        i.strip()
        lis.append(i)
    for j in str2.split('\n'):
        j.strip()
        for k in lis:
            flag = 0
            if j == k:
                print("match")
                lis1.append(1)
                flag = 1
                break
        if flag == 0:
            lis1.append(0)
    print(lis1)

    fd = open("SummFinal/final.txt", "a", encoding="utf-8")
    for i in lis1:
        fd.write(str(i))
        fd.write("  ")
    fd.write("\n")


def removestop(s):
    text = s
    text = ' '.join([word for word in text if word not in stop])
    return text


def stem(s):
    text = ""
    for word in s.split():
        text = text + stemmer.stem(word) + " "

    return text


def sentencemaker(s, var):
    tokenizer = RegexpTokenizer(r'\w+')
    sent_tokenize_list = sent_tokenize(s)
    l = len(sent_tokenize_list)
    fo = open("SummFinal/" + var, "w", encoding="utf-8")
    for sentence in sent_tokenize_list:
        v = tokenizer.tokenize(sentence)
        v = removestop(v)
        v = stem(v)
        fo.write(v + "\n")
    fo.close()


def applynlp(var):
    fo = open("Summ/" + var, "r", encoding="utf-8")
    str2 = fo.read()
    str2 = str2.strip()
    str2 = str2.lower()
    fo.close()
    var2 = var
    sentencemaker(str2, var2)


val = os.listdir("Summ")
val = sorted(val)
fd = open("SummFinal/final.txt", "w", encoding="utf-8")
fd.write("")
for x in val:
    #applynlp(x)
    convert(x)
