#! /usr/bin/env python
#coding=utf-8
from __future__ import division
import subprocess
import codecs
import math
from specialchar import SpecialChar 

# read utf8 file
def readfileUTF8(filename):
    return codecs.open(filename,'r','utf8').read()

# write utf8 file
def writefileUTF8(filename,allStr):
    if not isinstance(allStr,unicode):
        allStr=unicode(allStr,'utf8')
    codecs.open(filename,'w','utf8').write(allStr)

# calculate p(y|x)*log(p(y|x))
def h(p):
    if p!=0:		
	return p*math.log(p)
    else:
	return 0

# word boundary
def wbTag(word):
    if len(word)==1:
	text=['%s 1' %word]
    else:
	text=['%s 0' %w for w in word[0:-1]]+['%s 1' %word[-1]]
    return text
    
# 2-tag, B, E 
def twoTag(word):
    if len(word)==1:
	text=['%s B' %word]
    else:
	text=['%s B' %word[0]]+['%s E' %w for w in word[1:]]
    return text

# four-tag, B, M, E, S 
def fourTag(word):
    if len(word)==1:
	text=['%s S' %word]	
    elif len(word)==2:
	text=['%s B' %word[0],'%s E' %word[1]]
    else:
	text=['%s B' %word[0]]+['%s M' %w for w in word[1:-1]]+['%s E' %word[-1]] 	
    return text

# write format file
def writeFromatFile(ipath,opath,tag=twoTag):
    texts=[]
    lines=readfileUTF8(ipath).split('\n')
    for line in lines:
        text=[]
        for word in line.strip().split():
            text+=tag(word)
        texts.append('\n'.join(text))
    writefileUTF8(opath,'\n\n'.join(texts))

# write seed words from training data 
def writeSeedWords(ipath,opath):
    seedWords=[]
    lines=readfileUTF8(ipath).split('\n')
    for line in lines:
        for word in line.strip().split():
	    seedWords.append(word)
    writefileUTF8(opath,'\n'.join([word for word in set(seedWords)]))

# train crf model from train.txt
def train(path):
    retcode=subprocess.Popen(('crf_learn template.txt %s train.model' %path).split())      
    retcode.wait()
    if retcode < 0:
        print 'child is terminated'
    else:
        print 'vector modification successful'

# test test.txt by train.model and write the results with probability on result.output
def test(path):
    retcode=subprocess.Popen(('crf_test -m train.model %s' %path).split(),stdout=file('result.output','w'))      
    retcode.wait()
    if retcode < 0:
        print 'child is terminated'
    else:
        print 'vector modification successful'
    return recoverResults('result.output','result.txt')
   
# recover results
# S--1
# E--1
# B--0
# M--0
def recoverResults(ipath,opath):
    # each line a sentence
    sentences=[];sentence=''
    results=[]
    lines=readfileUTF8(ipath).split('\n')
    for line in lines:
	if len(line)<2:
            sentences.append(sentence)
            sentence=u''
        elif len(line)>2:
            c,kk,tag=line.split()
            if tag=='S':
                sentence+=u'%s ' %c
            else:
                sentence+=c
                if tag=='E':
                    sentence+=u' '
           
    writefileUTF8(opath,'\n'.join(sentences))



# score the result and resturn the F measure
def score(testPath):
    retcode=subprocess.Popen(('./score seed.txt %s result.txt ' %testPath).split(),stdout=file('score.txt','w'))      
    retcode.wait()
    if retcode < 0:
        print 'child is terminated'
    else:
        print 'vector modification successful'  
	
    # get the F measure
    lines=open('score.txt','r').read().split('\n')
    return float(lines[-6].split()[3])
	     