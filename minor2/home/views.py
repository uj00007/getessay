from urllib import request

import numpy as np
from bs4 import BeautifulSoup
import requests
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
#from django.urls import reverse
from googleapiclient.discovery import build
from nltk import RegexpTokenizer, sent_tokenize, SnowballStemmer
import re,math
from collections import Counter
from nltk.corpus import stopwords

from home.forms import EssayForm
from time import time


my_api_key = "AIzaSyC1gkYHQMTPdbBYtYPHMk45rkdr4grKq1g"
my_cse_id = "009652909963488507983:kcai5g0i2zg"


def google_search(search_term, api_key, cse_id, **kwargs):
    print("hello")
    service = build("customsearch", "v1", developerKey="AIzaSyC1gkYHQMTPdbBYtYPHMk45rkdr4grKq1g")
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        essayform = EssayForm(request.POST)
        # check whether it's valid:
        if essayform.is_valid():
            print(essayform.cleaned_data['title'])
            print(essayform.cleaned_data['length'])
            query=essayform.cleaned_data['title']
            results = google_search(query, my_api_key, my_cse_id, num=10)
            for result in results:
                #print(result['link'])
                a=result['link']
            #return render(request,'success.html', {})

            return HttpResponseRedirect(reverse('home:essaysuc'))

    else:
        essayform = EssayForm()
    return render(request, 'index.html', {'form': essayform})

docinput = []
funclist = [0, 0, 0, 0, 0, 0]


def getdata(link,lim):
    sourcecode = requests.get(link)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    text=" "
    for line in soup.find_all('p'):
        text+=line.get_text()
        #print(str(text))
    #print(str(text))
    text=str(text)
    text = re.sub('[[0-9]+]','',text)
    text=text.replace(".",". ")
    #text=text.replace("[]","")
    sentencemaker(text)
    st=time()
    global docinput
    global funclist
    makestructd1hash("wikisumm.txt")
    et=time()
    print("time taken by d1hash creation")
    print(et-st)
    global sentencehash
    sentencehash = {}
    docinput = []
    docinput1 = []
    st=time()
    sentencemap("wikisumm.txt")
    et=time()
    print("time taken by sentencemap creation")
    print(et - st)
    st=time()
    with open("wikisumm.txt", "r", encoding="utf-8") as f:
        s = f.readlines()
    s = [x.strip() for x in s]
    for i in s:
        funclist = [0, 0, 0, 0, 0, 0]
        #print(i)
        funclist[0] = tfidf(i,"wikisumm.txt")
        funclist[2] = positionsent(i,sentencehash)
        funclist[3] = sentencelength(i)
        funclist[4] = num_data(i)
        docinput.append(funclist)

    f = open("wikisumm.txt", "r", encoding="utf-8")
    s = f.read()
    s = s.strip()
    thematic(s)
    et = time()
    print("time taken by featurefile creation")
    print(et - st)
    sen_sen(s)

    fp = open("wikisummfeat.txt", "w", encoding="utf-8")
    for a in docinput:
        for b in a:
            fp.write(str(b) + "   ")
        fp.write("\n")
    fp.close()


    st=time()
    fp = open('wikisummfeat.txt', 'r', encoding='utf-8')
    y = fp.read()
    y = y.strip()
    flist = []
    for i in y.split('\n'):
        list = []
        for j in i.split():
            list.append(j)
        lis = [float(k) for k in list]
        flist.append(lis)
    #print(len(flist))
    syn0 = np.load('syn0.npy')
    syn1 = np.load('syn1.npy')
    x = np.array(flist)
    #print(type(x))
    l0 = x
    l1 = nonlin(np.dot(l0, syn0))  # np.dot is matrix multiplication
    l2 = nonlin(np.dot(l1, syn1))
    #print("output after testing")
    #print(l2)
    et=time()
    print("time taken by neuralnet processing creation")
    print(et - st)
    l = []
    l = l2.tolist()
    #print(l)
    for i in range(0, len(l)):
        l[i].append(i + 1)
    print(l)
    print(len(l2))
    l = sorted(l, key=lambda x: (-x[0], x[1]))
    #print(l)
    l=l[0:lim]
    print(l)
    l = sorted(l, key=lambda x: (x[1], x[0]))
    print(l)
    print("check")
    #print(len(allsentencelist))
    #print(allsentencelist[524])
    text=" "
    for z in l:
        text=text+allsentencelist[z[1]-1]+""
        print(allsentencelist[z[1]-1])

    return text


a=""
def essaysuc(request):
    global a
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        essayform = EssayForm(request.POST)
        # check whether it's valid:
        if essayform.is_valid():
            print(essayform.cleaned_data['title'])
            print(essayform.cleaned_data['length'])
            query=essayform.cleaned_data['title']
            lim=essayform.cleaned_data['length']
            results = google_search(query, my_api_key, my_cse_id, num=10)

            for result in results:
                if 'wikipedia' in result['link']:
                    a=getdata(result['link'],lim)
            #return render(request,'success.html', {})

            return HttpResponseRedirect(reverse('home:essaysuc'))
    else:
        essayform = EssayForm()
        return render(request,'index.html', {'essay':a,'form':essayform})

allsentencelist=[]


def sentencemaker(s):
    global allsentencelist
    allsentencelist=[]
    tokenizer = RegexpTokenizer(r'\w+')
    sent_tokenize_list = sent_tokenize(s)
    l=len(sent_tokenize_list)
    fo = open("wikisumm.txt", "w", encoding="utf-8")
    for sentence in sent_tokenize_list:
        allsentencelist.append(sentence)
        v = tokenizer.tokenize(sentence)
        v=removestop(v)
        v=stem(v)
        fo.write(v+"\n")
    fo.close()

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
docs_len={}
d1hash={}
def makestructd1hash(name):
    global docs_len
    global d1hash
    fo = open(name, "r", encoding="utf-8")
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


sentencehash = {}
maxsentencelen=0
def sentencemap(filename):
    with open(filename, "r", encoding="utf-8") as f:
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


def tfidf(sent,name):
    #print(sent)
    #print(name)
    global d1hash
    global docs_len
    sent = sent.strip().split()
    N=289
    tfidf=0
    for i in sent:
        tf = (d1hash[i][name] + 1) / docs_len[name]
        idf = np.log(N / (len(d1hash[i].keys())))
        tfidf+=tf*idf
    #print(tfidf)
    return tfidf

def positionsent(sent, sentencehash):
    if sentencehash[0]==sent or sentencehash[len(sentencehash.keys())-1]==sent:

        f2=1
        #print(f2)
        return f2
    else:
        f2=0
        #print(f2)
        return f2

def sentencelength(sent):
    global maxsentencelen
    f4 = len(sent.strip().split())
    f4 = f4/maxsentencelen
    return f4

def num_data(s1):
    count = 0;
    for i in s1.split():
        if i.isdigit():
            count += 1
    return count


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


def nonlin(x, deriv =False):
    if deriv == True:
        return (x*(1-x))
    return 1/(1+np.exp(-x))
