#! /usr/bin/env python
#coding=utf-8

"""
@title: chinese word segmentation with crf++
@description: 
@author: Antony Zhongqing Wang, Shoushan Li
@email: wangzq.antony@gmail.com

"""


from __future__ import division
from seg import *
from specialchar import SpecialChar 

trainPath='./pku/train/training_new.utf8'
testPath='./pku/test/test_gold_new.utf8'

sc=SpecialChar()

writeSeedWords(trainPath,'seed.txt')

#sc.replace(trainPath,'train.txt')
#testSCList=sc.replace(testPath,'test.txt')

writeFromatFile(trainPath,'train.txt',tag=fourTag)
writeFromatFile(testPath,'test.txt',tag=fourTag)

#writeFromatFile('train.txt','train.txt',tag=fourTag)
#writeFromatFile('test.txt','test.txt',tag=fourTag)

train('train.txt')

test('test.txt')
#sc.recovery('result.txt',testSCList)
    
print 'F Measure: %f' %score(testPath)
