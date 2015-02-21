#! /usr/bin/env python
# *-*coding:utf-8*-*
import sys,re,urllib2

from BeautifulSoup import BeautifulSoup

base_url = 'http://kaigoouen.net'
hopstepjump = {
	'hop':{
		'index':2,
		'last_page':25,
	},
	'step':{
		'index':3,
		'last_page':39,
	},
	'jump':{
		'index':4,
		'last_page':46,
	},
}

#### support ####
br = u'\n'

page_break = u".. raw:: pdf\n\n   PageBreak"

def header_line(txt):
	return u'='*30 + br	# use absolute width

#### for make .rst files ####
def sphinx_head(txt):
	title_line = header_line(txt)
	return br.join([br,txt,title_line]).encode('utf-8')


def sphinx_listtable(img,txt):
	table = u".. list-table::" + br
	image = u"   * - %s" % img
	text = u"     - | %s" % txt

	return br.join([table,image,text,br]).encode('utf-8')


def sphinx_image(src):
	option = u":width: 200pt"
	return u".. image:: %s" % src + br + u"          %s" % option


def sphinx_text(text):
	text = text.decode('utf-8').replace(u"<br />",br)
	if br in text:
		texts = text.splitlines()
		text = reduce(lambda x,y: x +  br + u"       | " + y,texts)

	return text


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
					image = sphinx_image(src)

					text = texts.next().renderContents()
					text = sphinx_text(text)

					print( sphinx_listtable(image,text) )

				print(page_break)					

		htmldata.close()
		p += 1
