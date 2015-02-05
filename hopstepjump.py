#! /usr/bin/env python
# *-*coding:utf-8*-*
import sys,re,urllib2

from BeautifulSoup import BeautifulSoup

base_url = 'http://kaigoouen.net'
hopstepjump = {
	'hop':{
		'title':u'ホップ',
		'index':2,
		'last_page':25,
	},
	'step':{
		'title':u'ステップ',
		'index':3,
		'last_page':39,
	},
	'jump':{
		'title':u'ジャンプ',
		'index':4,
		'last_page':46,
	},
}

#### support ####
br = u'\n'
def header_line(txt):
	return u'='*len(txt)*2 + br

#### for make .rst files ####
def sphinx_title(txt):
	return ( header_line(txt) + txt + br + header_line(txt) + br ).encode('utf-8')

def sphinx_index(txt):
	return (u'.. contents:: %s\n   :local:' % txt).encode('utf-8')

def sphinx_head(txt):
	title_line = header_line(txt)
	return br.join([br,txt,title_line]).encode('utf-8')

def sphinx_body_image(name,url,txt):
	name = u'|%s|' % name

	txt = txt.decode('utf-8')

	image = u'\n.. {name} image:: {url}\n'.format(name=name,url=url)

	option = u'   :alt: 参考画像' + br*2

	line = u'='*len(name) + u'  ' + u'='*len(txt) + br

	if br in txt:
		txts = txt.replace(u'<br />',br).splitlines()
		txt = reduce(lambda x,y: x + u'\n{name_space}  | '.format( name_space=u' '*len(name) ) + y,txts)

	return (image + option + line + name + u'  | ' + txt + br + line).encode('utf-8')


#### main ####
if __name__ == '__main__':

	try:
		choice = sys.argv[1]
		page = hopstepjump[choice]
	except IndexError:
		print("[エラー]：オプションが必要です（'hop'か'step'か'jump'のいずれか）。")
		exit("    - 例： 'python %s hop'" % sys.argv[0])
	except KeyError:
		print("[エラー]：オプションが違います（'hop'か'step'か'jump'のいずれか）。")
		exit("    - 例： 'python %s hop'" % sys.argv[0])

	print( sphinx_title(page['title']) )

	print( sphinx_index(u'目次') )

	p = 1
	while p <= page['last_page']:
		url = base_url + '/program/gymnastics/gymnastics_{index}_{page}.html'.format(index=page['index'],page=p)

		htmldata = urllib2.urlopen(url)

		soup = BeautifulSoup( unicode(htmldata.read(),'utf-8') )

		for box in soup.findAll('div',{'class':'box02'}):

			lessons = box.find('div',{'class':'box02_txt_%s' % choice})

			if lessons is not None:

				title = box.contents[1].contents[0]['alt']
				print( sphinx_head(title) )

				texts = lessons.findAll('div',{'class':'%s_txt' % choice})
				images = lessons.findAll('div',{'class':'%s_image' % choice})
				texts = iter(texts)

				for image in images:
					src = base_url + image.contents[0]['src']
					name = re.search(r'pic_\d+',src).group(0)
					text = texts.next().renderContents()
					print( sphinx_body_image(name,src,text) )

		htmldata.close()
		p += 1
