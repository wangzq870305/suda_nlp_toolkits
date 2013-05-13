#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from document import createDomain
from maxent import me_classify 

domain=createDomain('kitchen')
trains=domain[0][200:]+domain[1][200:]
tests=domain[0][:200]+domain[1][:200]
me_classify(trains,tests)