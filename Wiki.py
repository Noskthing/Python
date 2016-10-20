import urllib2
from bs4 import BeautifulSoup
import re
import random
import datetime

def getWikiLinks(url):
	request = urllib2.Request('http://en.wikipedia.org' + str(url))
	response = urllib2.urlopen(request) 
	html = response.read()

	bsObj = BeautifulSoup(html,'lxml')

	return bsObj.find('div',{'id':'bodyContent'}).findAll('a',href = re.compile('^(/wiki/)((?!:).)*$'))
		

links = getWikiLinks('/wiki/Jacob_Vargas')

while  len(links) > 0:
	newLink = links[random.randint(0,len(links) - 1)].attrs['href']
	print newLink
	links = getWikiLinks(newLink)


	http://weibo.com/u/1000030364?profile_ftype=1&is_all=1#_0
	http://weibo.com/u/1000030364?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=2#feedtop