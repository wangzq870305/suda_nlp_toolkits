#! /usr/bin/env python
#coding=utf-8
from __future__ import division
import codecs
import re

def readfileUTF8(filename):
    return codecs.open(filename,'r','utf8').read()

def writefileUTF8(filename,allStr):
    if not isinstance(allStr,unicode):
        allStr=unicode(allStr,'utf8')
    codecs.open(filename,'w','utf8').write(allStr)
    
class SpecialChar:
    def __init__(self):
	# numE
	full_0=self.B2Q('0')
	full_9=self.B2Q('9')
	self.numE=re.compile('[0-9'+full_0+'-'+full_9+']+')

	# numC
	D_chars=['一','二','三','四','五','六','七','八','九','十','○','百','千','万','萬','億','亿']
	D_chars=[unicode(x,'utf8') for x in D_chars if not isinstance(x,unicode)]
	self.numC=re.compile('[%s]+' %''.join(D_chars))
	
	# punSeg
	P_chars=['—', '“', '”', '，', '。', '、', '（', '）' ,'：', '《', '》', '（', '）', '「' ,'」', '『','』', '…' ,'？' ,'●' ,'！', '!', '；', ';' ,':','\t','...','"',')','(']
	P_chars=[unicode(x,'utf8') for x in P_chars if not isinstance(x,unicode)]
	self.punSeg=re.compile('[%s]+' %''.join(P_chars))
	
	# charE
	full_a=self.B2Q('a')
	full_z=self.B2Q('z')
	full_A=self.B2Q('A')
	full_Z=self.B2Q('Z')
	self.charE=re.compile('[a-zA-Z'+full_a+'-'+full_z+full_A+'-'+full_Z+']+')
	
	self.replaceChars=['A','B','C','D']
	
    def createSCList(self,text):
	return [self.charE.findall(text),self.punSeg.findall(text),self.numC.findall(text),self.numE.findall(text)]
    
    def recovery(self,path,scList):
	text=readfileUTF8(path)		
	for i in range(len(scList)-1,0,-1):
	    text=self.replaceRecovery(text,self.replaceChars[i],scList[i])
	writefileUTF8(path,text)
    
    def replace(self,ipath,opath):
	text=readfileUTF8(ipath)
	
	text=self.charE.sub(self.replaceChars[0],text)
	text=self.punSeg.sub(self.replaceChars[1],text)
	text=self.numC.sub(self.replaceChars[2],text)
	text=self.numE.sub(self.replaceChars[3],text)
	writefileUTF8(opath,text)
	
	return self.createSCList(readfileUTF8(ipath))
	    
    def replaceRecovery(self,newallstr,replacedstr,recordList):
	allstrlist=newallstr.split(replacedstr)
	allstr=''
	allstr=''.join([x+y for x,y in zip(allstrlist[0:-1],recordList)])
	allstr+=allstrlist[-1]
	return allstr
    
    def B2Q(self,uchar):
	inside_code=ord(uchar)
	if inside_code<0x0020 or inside_code>0x7e: 
		return uchar
	if inside_code==0x0020:
		inside_code=0x3000
	else:
		inside_code+=0xfee0
	return unichr(inside_code)