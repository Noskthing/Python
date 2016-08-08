# -*- coding: UTF-8 -*-

import urllib2
import re
import urllib
import thread
import time

class QSBK:
	"""docstring for QSBK"""
	def __init__(self):
		
		self.pageIndex = 1

		# init header
		self.user_Agent = 'Mozilla/4.0(compatible;MSIE 5.5;Windows NT'
		self.headers = {'User-Agent':self.user_Agent}

		# save context
		self.stories = []

		# whether run
		self.enable = False


	# get content in pageIndex
	def getPage(self,pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page/'+str(pageIndex)
			# create request
			request = urllib2.Request(url,headers = self.headers)
			# get response
			response = urllib2.urlopen(request)
			# make html content coding by utf-8
			pageCode = response.read().decode('utf-8')

			return pageCode
		except urllib2.URLError, e:
			if hasattr(e,'reason'):
				print e.reason
				return None

	def getPageItems(self,pageIndex):

		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print 'fail to get pageCode'
			return None
		pattern = re.compile('<div class="author clearfix">.*?href.*?<img src.*?title=.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>',re.S)
		items = re.findall(pattern,pageCode)

		# print  items[0][2]
		pageStories = []
		
		for item in items:
			
			replaceBr = re.compile('<br/>')
			contentText = re.sub(replaceBr,"\n",item[1])
			pageStories.append([item[0].strip(),contentText.strip(),item[2].strip()])
		return pageStories

	def loadNextPage(self):
		if self.enable == True:
			if len(self.stories) < 2:
				pageStories = self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex += 1

	def  getOneStory(self,pageStories,page):
		for pagestory in pageStories:
			input = raw_input()
			self.loadNextPage()
			if input == 'Q':
				self.enable = False
				print u'已退出糗事百科段子的阅读'
				return
			print u'第%s页 发布人%s 发布了%s的段子 获得了%s个赞' %(page,pagestory[0],pagestory[1],pagestory[2])


	def startRead(self):
		print u'开始阅读糗事百科的段子,点击键盘阅读下一个,按Q退出...'
		self.enable = True
		self.loadNextPage()

		nowPage = 0
		while self.enable:
			if len(self.stories) > 0:
				pageStories = self.stories[0]
				del self.stories[0]
				nowPage += 1
				self.getOneStory(pageStories,nowPage)



spider = QSBK()
spider.startRead()


