#! /usr/bin/env python
#coding=utf-8

"""
@title: sentiment classification with svm-light
@description: 
@author: Antony Zhongqing Wang, Shoushan Li
@email: wangzq.antony@gmail.com

"""



from __future__ import division
from document import createDomain
from svmclassify import svm_classify 

domain=createDomain('kitchen')
trains=domain[0][200:]+domain[1][200:]
tests=domain[0][:200]+domain[1][:200]
svm_classify(trains,tests)