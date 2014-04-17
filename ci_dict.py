#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-04-16 10:13:40
# @Author  : Ho1iarty (ho1iarty@gmail.com)
# @Version : 0.1

import sqlite3 as lite

def parseDict(cur):
	with open('JyutEnDict.u8') as fileObj:
		for line in fileObj.readlines():
			if len(line.strip())>0:
				line = line.replace("'","''");
				word = line[:line.index('[')-1]
				words = word.split(' ')
				yin = line[line.index('[')+1:line.index(']')]
				meaning = line[line.index(']')+3:-2]
				if meaning.endswith('/'):
					meaning = meaning[:-1]
				# print words[0]+'---'+words[1]+'---'+yin+'---'+meaning
				cur.execute("INSERT INTO DICT_CI VALUES(\'"+words[0]+"\',\'"+words[1]+"\',\'"+yin+"\',\'"+meaning+"\')")

def main():
	con = lite.connect('jyut_zh.dict')
	with con:
	    cur = con.cursor()    
	    cur.execute("DROP TABLE IF EXISTS DICT_CI")
	    cur.execute("CREATE TABLE DICT_CI(FAN TEXT, JIAN TEXT, YIN TEXT, YI TEXT)")
	    parseDict(cur)

if __name__ == '__main__':
	main()
	print 'DONE!'