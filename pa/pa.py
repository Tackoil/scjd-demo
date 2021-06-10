import jieba.analyse
import json
import math

with open('doc.json', encoding='utf-8') as d:
    ps = json.load(d)['contents']

'''
d = 0
w = 0
word_list = {}
for p in ps:
    d += 1
    plist = jieba.lcut(p)
    pdict = {}
    for c in plist:
        w += 1
        if c in pdict:
            pdict[c] += 1
        else:
            pdict[c] = 1
    for pk in pdict.keys():
        if pk in word_list:
            word_list[pk]['tf'] += pdict[pk]
            word_list[pk]['df'] += 1
        else:
            word_list[pk] = {'tf': pdict[pk], 'df': 1}

def tfidf(x):
    t = word_list[x]
    return t['tf']/w * math.log(d / t['df'])

r =  sorted(word_list, key=tfidf)
print(d, w, r)
'''

corpus = "".join(ps)
keywords_textrank = jieba.analyse.textrank(corpus, topK=20, withWeight=True)
for k in keywords_textrank:
    print("['{}', {}],".format(k[0], math.ceil(k[1]*100)))