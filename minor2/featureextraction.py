import numpy as np
from nltk import RegexpTokenizer, sent_tokenize, SnowballStemmer
from nltk.corpus import stopwords
import os
import re, math
from collections import Counter

WORD = re.compile(r'\w+')

stop = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

def removestop(s):
    text = s
    text = ' '.join([word for word in text if word not in stop])
    return text

def stem(s):
    text=""
    for word in s.split():
        text=text+stemmer.stem(word)+" "

    return text


def sentencemaker(s,var):
    tokenizer = RegexpTokenizer(r'\w+')
    sent_tokenize_list = sent_tokenize(s)
    l=len(sent_tokenize_list)
    fo = open("Documents/Text2/"+var, "w", encoding="utf-8")
    for sentence in sent_tokenize_list:
        v = tokenizer.tokenize(sentence)
        v=removestop(v)
        v=stem(v)
        fo.write(v+"\n")
    fo.close()



def applynlp(var):
    fo = open("Documents/Text/"+var, "r", encoding="utf-8")
    str2 = fo.read()
    str2 = str2.strip()
    str2 = str2.lower()
    fo.close()
    var2=var
    sentencemaker(str2,var2)

def titlesimilarity(sent,title):   #title should be stop word removed and stemmed
    title=title.split() #can be made global to reduce time
    title=set(title)
    sent=sent.split()
    sandt=0
    for i in sent:
        if i in title:
            sandt+=1
    f1=sandt/len(title)
    #print(sent)
    #print(f1)

sentencehash = {}
maxsentencelen=0
def sentencemap(filename):
    with open("Documents/Text2/"+filename, "r", encoding="utf-8") as f:
        s = f.readlines()
    s = [x.strip() for x in s]
    global maxsentencelen
    for i in s:
        if len(i)>=maxsentencelen:
            maxsentencelen=len(i)
    #print(s)
    global sentencehash
    ctr = 0
    for i in s:
        sentencehash[ctr] = i
        ctr += 1


def positionsent(sent, sentencehash):
    if sentencehash[0]==sent or sentencehash[len(sentencehash.keys())-1]==sent:

        f2=1
        #print(f2)
        return f2
    else:
        f2=0
        #print(f2)
        return f2
'''
doclenhash={}
def preprocesstfidf(text, name):
    text = text.strip().split()
    global doclenhash
    if name not in doclenhash.keys():
        doclenhash[name] = len(text)
    print(doclenhash)
    wordcount = {}
    for i in text:
        if i in wordcount.keys():
            wordcount[i] += 1
        else:
            wordcount[i] = 1
    print(wordcount)
    return wordcount

def tf2(sent, wordcount, name, doclenhash):
    sent = sent.strip().split()
    for i in sent:
        tf = np.log((wordcount[i] + 1)) / np.log(doclenhash[name])
        print(tf)

'''
def tfidf(sent,name):
    #print(sent)
    #print(name)
    sent = sent.strip().split()
    N=289
    tfidf=0
    for i in sent:
        tf = (d1hash[i][name] + 1) / docs_len[name]
        idf = np.log(N / (len(d1hash[i].keys())))
        tfidf+=tf*idf
    #print(tfidf)
    return tfidf


docs_len={}
d1hash={}
def makestructd1hash(name):
    global docs_len
    global d1hash
    fo = open("Documents/Text2/"+name, "r", encoding="utf-8")
    str2 = fo.read()
    fo.close()
    list = str2.strip().split()
    for i in list:
        if d1hash.get(i, "null") != "null":
            wordcounthash = d1hash.get(i)
            if d1hash.get(i).get(name, "not") != "not":
                d1hash.get(i)[name] = d1hash.get(i).get(name) + 1

            else:

                wordcount = 1
                wordcounthash[name] = wordcount
                d1hash[i] = wordcounthash

        else:
            d1hash[i] = {}
            wordcount = 1
            d1hash[i][name] = wordcount
    docs_len[name] = len(list)
    #print(docs_len)
    #print(d1hash)

def thematic(text):
    global funclist
    global docinput
    #print(docinput)
    #print(len(docinput))
    dict = {}
    set1 = set()
    s1 = text
    for i in s1.split():
        if i in dict:
            dict[i] += 1
        else:
            dict[i] = 1
    #print(dict)
    lis = sorted(dict, key=dict.get)
    #print(lis)

    k = len(lis)

    for i in range(0, 10):
        set1.add(lis[k - 1])
        k -= 1

    #print(set1)
    ctr=0
    for i in s1.split('\n'):
        set2 = set()
        for j in i.split():
            set2.add(j)
        m = len(set1.intersection(set2))
        m /= len(set1)
        f3 = m
        #print(f3)
        #print(docinput)
        docinput[ctr][1]=f3
        ctr+=1


def num_data(s1):
    count = 0;
    for i in s1.split():
        if i.isdigit():
            count += 1
    return count



def sentencelength(sent):
    global maxsentencelen
    f4 = len(sent.strip().split())
    f4 = f4/maxsentencelen
    return f4


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def sen_sen(text):
    global funclist
    global docinput
    text=text.strip()
    for i in text.split('\n'):
        lis = []
        sum1 = 0
        ctr=0
        for j in text.split('\n'):
            if i != j:
                vector1 = text_to_vector(i)
                vector2 = text_to_vector(j)
                lis.append(get_cosine(vector1,vector2))
                #print(lis)
                sum1 = sum(i for i in lis)
                max1 = max(lis)
                if max1!=0:
                    f4=(sum1/max1)
                else:
                    f4=0
                docinput[ctr][5] = f4
                ctr += 1





'''
val=os.listdir("Documents/Text")
val= sorted(val)
for x in val:
    applynlp(x)
'''

alldocsinput=[]
docinput = []
funclist = [0,0,0,0,0,0]
name= os.listdir("Documents/Text2")
name = sorted(name)
tr=1
for k in name:
    filename = k
    makestructd1hash(filename)
    sentencehash={}
    docinput=[]
    docinput1=[]
    sentencemap(filename)
    #print(d1hash)
    #print(sentencehash)
    with open("Documents/Text2/"+filename, "r", encoding="utf-8") as f:
        s = f.readlines()
    s = [x.strip() for x in s]
    for i in s:
        funclist = [0, 0, 0, 0, 0, 0]
        #print(i)
        funclist[0] = tfidf(i,filename)
        funclist[2] = positionsent(i,sentencehash)
        funclist[3] = sentencelength(i)
        funclist[4] = num_data(i)
        docinput.append(funclist)
    f = open("Documents/Text2/"+filename, "r", encoding="utf-8")
    s = f.read()
    s = s.strip()
    thematic(s)
    sen_sen(s)
    print(docinput)
    fp = open("Documents/Features/"+filename,"w",encoding="utf-8")
    for a in docinput:
        for b in a:
            fp.write(str(b)+"   ")
        fp.write("\n")



    alldocsinput.append(docinput)
    print("doc ends" + str(tr))
    tr += 1
    #print(alldocsinput)
    #print(len(alldocsinput))

'''f=open("ex2.txt", "r", encoding="utf-8")
s = f.read()
thematic(s)'''