# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import sys
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')

class Tool:
	"""docstring for Tool"""
	removeImg = re.compile('<img.*?>| {7}|')
	#删除超链接标签
	removeAddr = re.compile('<a.*?>|</a>')
	#替换换行标签为\n
	replaceLine = re.compile('<tr>|<div>|</div>|</p')
	#叫表格指标<td>替换为\t
	replaeTD = re.compile('<td>')
	#讲段落开头替换为\n加两个空格
	replacePara = re.compile('<p.*?>')
	#讲换行符或者双换行符替换为\n
	replaceBR = re.compile('<br><br>|<br>')
	#将其余的标签提出
	removeExtraTag = re.compile('<.*?>')
	#去除空格
	replaceSpace = re.compile('&nbsp')
	
	def replace(self,content):
		content = re.sub(self.removeImg,'',content)
		content = re.sub(self.removeAddr,'',content)
		content = re.sub(self.replaceLine,'\n',content)
		content = re.sub(self.replaeTD,'\t',content)
		content = re.sub(self.replacePara,'\n',content)
		content = re.sub(self.replaceBR,'\n',content)
		content = re.sub(self.removeExtraTag,'',content)
		content = re.sub(self.replaceSpace,'',content)

		#移除多余的前后内容
		return content.strip()
		
#测试
class  BaiDuSpider:

	"""docstring for  BaiDuSpider"""
	def __init__(self, baseUrl,isSeeLZ):
		self.baseUrl = baseUrl
		self.isSeeLZ = '?see_lz=' + str(isSeeLZ)
		self.tool = Tool()
		self.file = None

	def  getPageContent(self,pageNum):
		try:
			#拼接url
			url = self.baseUrl + self.isSeeLZ + '&pn=' + str(pageNum)

			# print url
			#构建request
			request = urllib2.Request(url)
			#获取response
			response = urllib2.urlopen(request)

			# if pageNum == 1:
			# 	self.content = response.read()
			# print response.read()
			return response.read()

		except urllib2.URLError, e:
				if hasattr(e,'reason'):
					print u'连接百度贴吧失败，原因是',e.reason
					return None

# 获取帖子标题
	def getTitle(self):
		content = self.getPageContent(1)

		# print pageContent
		pattern = re.compile('<h3 class="core_title_txt.*?">(.*?)</h3>',re.S)
		result = re.search(pattern,content)

		if result:
			#测试一下匹配结果
			#替换掉空格标识符
			replaceSpace = re.compile('&nbsp;')
			title = re.sub(replaceSpace,' ',result.group(1).strip())
			return title
		else:
			return '食屎啦'

#获取帖子页数
	def  getPageNum(self):
		content = self.getPageContent(1)
		pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
		result = re.search(pattern,content)
		if result:
			return result.group(1).strip()
		else:
			return None

#获取正文
	def getContent(self,pageNum):
		content = self.getPageContent(pageNum)
		# print content
		pattern = re.compile('<div id="post_content_(.*?)>(.*?)</div>',re.S)
		items = re.findall(pattern,content)
		floor = 1;
		contents = []
		for item in items:
			# print item
			itemContent = str(floor) + u'楼------------------\n'+'\n'+self.tool.replace(str(item[1])) +'\n\n'
			contents.append(itemContent.encode('utf-8'))
		
			floor += 1
		return contents
		# print self.tool.replace(str(items[-1]))

#写入文件
	def setTitle(self,title):
		if title is not None:
			self.file = open(title + '.txt','w+')
			self.file.write(title + '\n\n')
		else:
			self.file = open('百度贴吧' + '.txt','w+')
			self.file.write('百度贴吧' + '\n\n')

	def  writeDataToFile(self,contents,pageNum):
		self.file.write('第 ' + str(pageNum) + '页\n')
		for item in contents:
			self.file.write(item)


#开始
	def start(self):

		print '开始录入帖子...'

		title = self.getTitle()
		print '帖子标题是 ' + title

		pageNum = self.getPageNum()
		print '共' + pageNum + '页'

		if pageNum == None:
			print 'URL已经失效，请重试'
			return

		self.setTitle(title)

		try:
			print '该帖子一共'+str(pageNum) + ' 页'
			for i in range(1,int(pageNum) + 1):
				print '正在写入第' + str(i) + '页...'
				pageContent = self.getContent(i)
				self.writeDataToFile(pageContent,int(i))
		except IOError, e:
			print '写入异常，原因是：' + e.message	
		finally:
			print '写入成功'


print '请输入帖子编号'


baseUrl = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))

isSeeLZ = raw_input(u'是否只看楼主，是输入1，否输入0')

if str(isSeeLZ) != '1' or str(isSeeLZ) != '0':
	print '输入不合法！'
	isSeeLZ = raw_input(u'是否只看楼主，是输入1，否输入0')


spider = BaiDuSpider(baseUrl,isSeeLZ)

#写在这里是为了告诉自己  不要试图去print一个没有返回值的函数  会莫名其妙多个None的。。。

# print spider.getPageNum()
spider.start()
