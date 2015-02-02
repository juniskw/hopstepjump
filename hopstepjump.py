#! /usr/bin/env python
# *-*coding:utf-8*-*

from BeautifulSoup import BeautifulSoup
import re,urllib2

base_url = 'http://kaigoouen.net'
hopstepjump = {
	'hop':{
		'index':2,
		'last_page':25,
	},
	'step':{
		'index':3,
		'last_page':0,
	},
	'jump':{
		'index':4,
		'last_page':0,
	},
}

#### support ####
br = "\n"
def header_line(txt):
	return "="*len(txt)*2 + br

#### for make .rst files ####
def sphinx_title(txt):
	title_line = header_line(txt)
	return br + txt + br + title_line + br

def sphinx_body_image(name,url,txt):
	name = str('|%s|' % name)	# strしないとunicode型になりUnicodeDecodeError

	image = '\n.. {name} image:: {url}\n'.format(name=name,url=url)

	option = '   :alt: 参考画像' + br*2	#

	line = '='*len(name) + '  ' + '='*len(txt.decode('utf-8')) + br

	# if '\n' in text: 改行前後で分けて' '*len(name)+'  |'の後に次の行
	if '\n' in txt:
		txts = txt.split('\n')
		txt = reduce(lambda x,y: x + '\n{name_space}  |'.format( name_space=' '*len(name) ) + y,txts)

	return image + option + line + name + '  |' + txt + br + line


#### main ####
if __name__ == '__main__':
	page = hopstepjump['hop']

	p = 1
	while p <= page['last_page']:
		url = base_url + '/program/gymnastics/gymnastics_{index}_{page}.html'.format(index=page['index'],page=p)

		htmldata = urllib2.urlopen(url)

		soup = BeautifulSoup( unicode(htmldata.read(),'utf-8') )

		for box in soup.findAll('div',{'class':'box02'}):

			lessons = box.find('div',{'class':'box02_txt_hop'})

			if lessons is not None:

				title = box.contents[1].contents[0]['alt']
				print( sphinx_title(title) )

				texts = lessons.findAll('div',{'class':'hop_txt'})
				images = lessons.findAll('div',{'class':'hop_image'})
				texts = iter(texts)

				for image in images:
					src = base_url + image.contents[0]['src']
					name = re.search(r'pic_\d+',src).group(0)
					text = texts.next().renderContents()
					print( sphinx_body_image(name,src,text) )

		htmldata.close()
		p += 1
