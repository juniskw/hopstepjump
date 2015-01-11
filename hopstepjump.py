#! /usr/bin/env python
# *-*coding:utf-8*-*

from BeautifulSoup import BeautifulSoup
#from HTMLParser import HTMLParser
import re,urllib2


pages = {
	'hop':{
		'url':'http://kaigoouen.net/program/gymnastics/gymnastics_2_1.html',
		'page_count':25,
	},
	'step':{
		'url':'http://kaigoouen.net/program/gymnastics/gymnastics_3_1.html',
		'page_count':39,
	},
	'jump':{
		'url':'http://kaigoouen.net/program/gymnastics/gymnastics_4_1.html',
		'page_count':46,		  
	}
}


if __name__ == '__main__':
	page = pages['hop']
	url = page['url']

	htmldata = urllib2.urlopen(url)

	soup = BeautifulSoup( unicode(htmldata.read(),'utf-8') )

	print( soup.findAll('div',{'class':'box02'}) )

	htmldata.close()
