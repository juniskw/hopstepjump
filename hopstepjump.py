#! /usr/bin/env python
# *-*coding:utf-8*-*

from BeautifulSoup import BeautifulSoup
import re,urllib2

base_url = 'http://kaigoouen.net/'
image_url = base_url + 'img/'

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

#### support ####
br = "\n"
def header_line(txt):
	return "="*len(txt)*2 + br

#### for make .rst files ####
def sphinx_title(txt):
	title_line = header_line(txt)
	return txt + br + title_line + br

def sphinx_body(img,txt):
	pass


#### main ####
if __name__ == '__main__':
	page = pages['hop']
	url = page['url']

	htmldata = urllib2.urlopen(url)

	soup = BeautifulSoup( unicode(htmldata.read(),'utf-8') )

	box = soup.findAll('div',{'class':'box02'})[1]

	title = box.contents[1].contents[0]['alt']
	print( sphinx_title(title) )


	htmldata.close()
