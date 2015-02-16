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
	return u'='*30 + br	# use absolute width

#### for make .rst files ####
def sphinx_title(txt):
	return ( header_line(txt) + txt + br + header_line(txt) + br ).encode('utf-8')

def sphinx_head(txt):
	title_line = header_line(txt)
	return br.join([br,txt,title_line]).encode('utf-8')

def sphinx_body_image(url,txt):
	txt = txt.decode('utf-8').replace(u'<br />',br)

	image = u'.. image:: %s' % url

	line = u'='*56 + u'  ' + u'='*80 + br	# use absolute width

	if br in txt:
		txts = txt.splitlines()
		txt = reduce(lambda x,y: x + u'\n{space}  | '.format(space=u' '*56) + y,txts)	# use absolute width

	return (line + image + u'{space}  | '.format(space=u' '*(56-len(image))) + txt + br + line).encode('utf-8')	# use absolute width


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
					text = texts.next().renderContents()
					print( sphinx_body_image(src,text) )

		htmldata.close()
		p += 1
