# -*- coding: UTF-8 -*-

import urllib2
import urllib
from bs4 import BeautifulSoup
# import sys
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

def getHTML(url):
	html = ''
	try:
		req = urllib2.Request(str(url)) 
		response = urllib2.urlopen(req) 
		html = response.read()
	except urllib2.URLError, e:
		print(e)
	

	try:
		bsObj = BeautifulSoup(html,'lxml')
		for child in bsObj.findAll('ul',class_='uk-nav uk-nav-side')[1].children:
			if str(type(child)) == "<class 'bs4.element.Tag'>":
				if 'style' in child.attrs:
					print child.attrs['style']
	except AttributeError as e:
		print e 
	
		

# getHTML('http://www.pythonscraping.com/pages/warandpeace.html')
getHTML('http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013747381369301852037f35874be2b85aa318aad57bda000')