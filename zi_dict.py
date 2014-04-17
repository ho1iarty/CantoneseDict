#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-04-16 16:23:18
# @Author  : Ho1iarty (ho1iarty@gmail.com)
# @Version : 0.1
import os
import urllib, urllib2
from pyquery import PyQuery as pq, PyQuery
from progressbar import Bar, Percentage, ProgressBar
import re
import sqlite3 as lite
import time
import logging

logging.basicConfig(filename = os.path.join(os.getcwd(), 'zi_dict.log'),
	level = logging.DEBUG, filemode = 'w', 
	format = '%(asctime)s - %(levelname)s: %(message)s') 

def parseDict(con,cur):
	with open('gbk_zi') as fileObj:
		total = fileObj.readlines()
		pbar = ProgressBar(widgets=['Processing: ', Percentage(),Bar()], maxval=len(total))
    		pbar.start()
		for (index,line) in enumerate(total):
			line = line.strip()
			if len(line):
				req = urllib2.Request(url="http://www.iso10646hk.net/jp/database/index.jsp",
                      data=urllib.urlencode({'env': 'dbmix','mode': 'characters','charset': 'unicode','ch': line}),
                      headers={"Content-type": "application/x-www-form-urlencoded"})
				try:
					response = urllib2.urlopen(req,timeout=180)
					doc = pq(response.read())
					tables = doc('table.font-family')
					if len(tables)<=0:
						logging.info("No results. Skip this line. %s, %d." % (line, index+1))
						continue
					result = pq(tables[1])
					result.remove('tr:first')
					result.remove('select')
					result.remove('[href="#anchorResult"]')
					# print result.html().encode('utf-8')
					word = ''
					yin = []
					for tr in result('tr'):
						td_str = pq(tr).remove('td:gt(1)').text().encode('utf-8')
						zi_or_pin = re.sub('\[.*?\]','',td_str).strip()
						ziyin_list = re.split('\s+',zi_or_pin)
						if len(ziyin_list)>1:
							if len(word):
								# print word+'---'+' '.join(yin)
								cur.execute("INSERT INTO DICT_ZI VALUES(\'"+word+"\',\'"+' '.join(yin)+"\')")
								word=''
								del yin[:]
							word = ziyin_list[0]
							yin.append(ziyin_list[1])
						else:
							yin.append(zi_or_pin)
					if len(word):
						# print word+'---'+' '.join(yin)
						cur.execute("INSERT INTO DICT_ZI VALUES(\'"+word+"\',\'"+' '.join(yin)+"\')")
				except Exception, e:
					con.commit() # commit when error happened
					# print "Timeout. Skip this line.\n", line, index
					logging.info("Error Happended. Skip this line. %s, %d." % (line, index+1))
					logging.exception(e)
			# end if
        		pbar.update(index)
			time.sleep(0.8) # wait for a second before next request
			if index%500 == 0: # commit after inserting some records
				con.commit()
		# end for
		pbar.finish()

def main():
	con = lite.connect('jyut_zh.dict')
	with con:
	    cur = con.cursor()    
	    cur.execute("DROP TABLE IF EXISTS DICT_ZI")
	    cur.execute("CREATE TABLE DICT_ZI(ZI TEXT, YIN TEXT)")
	    parseDict(con,cur)

if __name__ == '__main__':
	main()