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

#def sphinx_body_image(num,url,txt):
#	name = '|pic_%i|' % num
#
#	image = '.. {name} image:: {url}\n'.format('name'=name,'url'=url)
#	option = '   :alt: {alt}'.format('alt'=txt)
#
#	return image + option



#### main ####
if __name__ == '__main__':
	page = pages['hop']
	url = page['url']

	htmldata = urllib2.urlopen(url)

	soup = BeautifulSoup( unicode(htmldata.read(),'utf-8') )

	box = soup.findAll('div',{'class':'box02'})[1]	#forloop

	title = box.contents[1].contents[0]['alt']
#	print( sphinx_title(title) )

	lessons = box.find('div',{'class':'box02_txt_hop'})
	texts = lessons.findAll('div',{'class':'hop_txt'})
	images = lessons.findAll('div',{'class':'hop_image'})
	for text in texts:
		print( text.renderContents() )
	for image in images:
		print(image.contents[0]['src'])

	htmldata.close()
