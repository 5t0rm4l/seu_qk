# -*- coding: utf-8 -*-
#!/usr/bin/python 

import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib 
import string  
import re
import time
import sys
import configparser

reload(sys)
sys.setdefaultencoding("utf-8")

def read_from_config(filepath):
    cf = configparser.ConfigParser()
    cf.read(filepath)
    uid = cf.get("global", "user_id")
    pwd = cf.get("global", "passwd")

    jhkcdm = cf.get("global", "jhkcdm")
    mkbh = cf.get("global", "mkbh")
    xkkclx = cf.get("global", "xkkclx")
    course_id = cf.get("global", "course_id")

    select_xkkclx = cf.get("global", "select_xkkclx")
    select_jhkcdm = cf.get("global", "select_jhkcdm")
    select_mkbh = cf.get("global", "select_mkbh")
    select_dxdbz = cf.get("global", "select_dxdbz")
    return (uid, pwd, jhkcdm, mkbh, xkkclx, course_id, select_xkkclx, select_jhkcdm, select_mkbh, select_dxdbz)


def loginIn(userName, passWord, inputCaptcha = True):
    #设置cookie处理器
	cj = cookielib.LWPCookieJar()
	cookie_support = urllib2.HTTPCookieProcessor(cj)
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
	urllib2.install_opener(opener)  
    #获取验证码
    
	for i in range(10):
		try:
			image = urllib2.urlopen('http://xk.urp.seu.edu.cn/jw_css/getCheckCode', timeout = 10)
			break
		except Exception, e:
			print e
			continue
	else:
		return (False, "验证码获取失败", '')

	f = open('code.jpg','wb')
	f.write(image.read())
	f.close()

	if inputCaptcha == True:  # manually input the capthcha
	#读取验证码
		code = raw_input(u'请打开我所在目录下的code.jpg，并在这里敲入里面的四位数字验证码：'.encode('gbk'))
		

    #构造post数据
	posturl = 'http://xk.urp.seu.edu.cn/jw_css/system/login.action' 
	header ={   
		'Host' : 'xk.urp.seu.edu.cn',   
		'Proxy-Connection' : 'keep-alive',
		'Origin' : 'http://xk.urp.seu.edu.cn',
		'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
		'Referer' : 'http://xk.urp.seu.edu.cn/jw_css/system/login.action'
		}
	data = {
		'userId' : userName,
		'userPassword' : passWord, #你的密码，  
		'checkCode' : code,           #验证码 
		'x' : '33',     #别管
		'y' : '5'       #别管2
		}
    
    #post登录数据
	(state, text) = postData(posturl,header,data)
	url = ''
	if state == True:
		if (text.find('选课批次') != -1):  # a bad label; the url returned should be the best
			print u"登录成功"
			function = re.search(r'onclick="changeXnXq.*\)"', text); # find the function whose parameter are wanted
			function = function.group()		
			parameters = re.search(r"'(.*)','(.*)','(.*)'\)", function) # url parameters
			url = "http://xk.urp.seu.edu.cn/jw_css/xk/runXnXqmainSelectClassAction.action?Wv3opdZQ89ghgdSSg9FsgG49koguSd2fRVsfweSUj=Q89ghgdSSg9FsgG49koguSd2fRVs&selectXn=" + parameters.group(1) + "&selectXq=" + parameters.group(2) + "&selectTime=" + parameters.group(3)
		else:
			state = False
			errorMessage = re.search(r'id="errorReason".*?value="(.*?)"', text)
			text = errorMessage.group(1)
	else:
		text = "网络错误，登录失败" 
	return (state, text, url, code)


def selectSemester(semesterNum, url):
    print u"切换学期菜单中......"
    time.sleep(5)
    #构造选择学期的包
    
    geturl = re.sub('selectXq=.', 'selectXq='+str(semesterNum), url)
    
    header = {  'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',        
    }
    data = {}
    #get获取学期课程
    (state, text) = getData(geturl,header,data)
    if state == True:
        if text.find("数据异常") != -1:  # switch to an unavailable semester
            state = False
            text = "目前无法选择学期" + str(semesterNum)
    return (state, text)


def postData(posturl,headers,postData):
    postData = urllib.urlencode(postData)  #Post数据编码   
    request = urllib2.Request(posturl, postData, headers)#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程 
    text = ''
    for i in range(10):
        try:
            response = urllib2.urlopen(request, timeout = 5)
            text = response.read()
            break
        except Exception, e:
            print 'fail to get response'
            print 'trying to open agian...'
            continue
    else:
        return (False, "数据发送失败")
    return (True, text)


def getData(geturl,header,getData, returnUrl = False):
    getData = urllib.urlencode(getData)
    request = urllib2.Request(geturl, getData, header)
    text = ''
    url = ''
    for i in range(10):
        try:
            response = urllib2.urlopen(request, timeout = 5)
            text = response.read()
            url = response.geturl()
            break
        except Exception, e:
            print e
            print 'trying to open agian...'
            continue
    else:
        if returnUrl == False:
            return (False, "获取数据失败")
        else:
            return (False, "获取数据失败", '')

    if returnUrl == False:
        return (True, text)
    else:
        return(True, text, url)


def stateCheck(textValue):    
    text = textValue
    if (text.find('成功选择') != -1) or (text.find('服从推荐') != -1):
        return 0
    if text.find('已满') != -1:
        return 1
    if text.find('失败') != -1:
        return 2


def I_just_wanna_this_one(semesterNum, url, apilist, postlist, jxbbh):
    (state, text) = selectSemester(semesterNum, url)
    if state == False:
        print text.decode('utf-8')
        print u'切换到学期' + str(semesterNum) + u"失败"
        return
    else:
        print u'切换到学期' + str(semesterNum) + u"成功"
    print u"==============开始选课=============="
    
    header1 = {
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Accept' : 'application/json, text/javascript, */*',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }   
    data1 = {}
    api = "http://xk.urp.seu.edu.cn/jw_css/xk/runViewsecondSelectClassAction.action?select_jhkcdm="+ apilist[0] +"&select_mkbh="+ apilist[2] +"&select_xkkclx="+ apilist[1] +"&select_dxdbz=0"
    (state, text) = getData(api, header1,data1)
    if state == False:
        print u"打开课程列表页面失败"
        return

    #构造数据包
    posturl = "http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh=" + jxbbh + "&select_xkkclx=" + postapi[0] + "&select_jhkcdm=" + postapi[1] + "&select_mkbh=" + postapi[2] + "&dxdbz=" + postapi[3]
    
    headers = { 
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Content-Length' : '2',
                'Accept' : 'application/json, text/javascript, */*',
                'Origin':'http://xk.urp.seu.edu.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }
    data = {
            '{}':''
            }
    print u"我开始选课了,课程编号：" + apilist[3]
    times = 0
    while True :
        #判断是否选到课
        times = times+1
        (state, text) = getData(api,header1,data1)
        if state == False:
            print "打开课程列表页面失败"
            return
        pattern2 = ('已选(.{0,200})align=\"')
        result = re.findall(pattern2,text,re.S)
        #print result
        success = len(result) #为0为不成功 继续
        if (success != 0) and (result[0].find(apilist[3])!=-1):
            print u"Nice，已经选到课程:"+apilist[3]
            break
        #发送选课包
        print u"第"+str(times)+"次尝试选择课程"+apilist[3]+u",但是没选到！"
        (state, text) = postData(posturl,headers,data)
        time.sleep(3)#sleep
    return



if __name__ == "__main__":
    semester = input(u'选择学期编号(短学期:1，秋季:2，春季:3)-> '.encode('gbk'))

    inputCaptcha = True
    userName, passWord, jhkcdm, mkbh, xkkclx, course_id, select_xkkclx, select_jhkcdm, select_mkbh, select_dxdbz= read_from_config('config.ini')
    (state, text, url, code) = loginIn(userName, passWord, inputCaptcha)
    failTimes = 0
    if inputCaptcha == True and state == False:
        print text.decode('utf-8')
    if state == True:
    	urlapi = [jhkcdm, xkkclx, mkbh, course_id]
        postapi = [select_xkkclx, select_jhkcdm, select_mkbh, select_dxdbz]
        I_just_wanna_this_one(semester,url, urlapi, postapi, course_id)
    else:
        print u"要不试试退出后重新打开一下本程序？"
    input(u'按任意键退出...'.encode('gbk'))


