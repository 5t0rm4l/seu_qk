# -*- coding: utf-8 -*-
#!/usr/bin/python  

###########################################################################################
# “另行选择“构造窗口的js源码 找到调用时对应的
# selectOthers(jhkcdm,xkkclx,mkbh,ind)就可以自己构造出请求的网页了
# eg: http://xk.urp.seu.edu.cn/jw_css/xk/runViewsecondSelectClassAction.action?select_jhkcdm=00034&select_mkbh=rwskl&select_xkkclx=45&select_dxdbz=0
# selectOthers(jhkcdm,xkkclx,mkbh,ind){
# ....
#  var retObj = window.showModalDialog("runViewsecondSelectClassAction.action?Wv3opdZQ89ghgd88wjff43Dsdf4Fsd4SSg9FsgG49koguSd2fRVsfweSUj=" + new Date() + 
#  "&select_jhkcdm=" + jhkcdm + "&select_mkbh=" + mkbh+"&select_xkkclx="+xkkclx+"&select_dxdbz=0",obj,sFeatures);
#  ...
# }

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
sys.setdefaultencoding("gbk")

def read_from_config(filepath):
    cf = configparser.ConfigParser()
    cf.read(filepath)
    uid = cf.get("global", "userID")
    pwd = cf.get("global", "password")
    return (uid, pwd)

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
		code = raw_input(u'请打开我所在目录下的code.jpg，并在这里敲入里面的四位数字验证码：')
		

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
	return (state, text, url)

def selectSemester(semesterNum, url):
    print u"切换学期菜单中......"
    time.sleep(5)
    #构造选择学期的包
    # !!!NOTICE: SELECTTIME manually set this url is not a wise choice
    # geturl ='http://xk.urp.seu.edu.cn/jw_css/xk/runXnXqmainSelectClassAction.action?Wv3opdZQ89ghgdSSg9FsgG49koguSd2fRVsfweSUj=Q89ghgdSSg9FsgG49koguSd2fRVs&selectXn=2014&selectXq='+str(semesterNum)+'&selectTime=2014-05-30%2013:30~2014-06-07%2023:59'
    
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

def Mode1(semesterNum, url):
    (state, text) = selectSemester(semesterNum, url)
    if state == False:
        print text.decode('utf-8')
        print u'切换到学期' + str(semesterNum) + u"失败"
        return
    else:
        print u'切换到学期' + str(semesterNum) + u"成功"
    #寻找可以“服从推荐”的课程
    print u"==============开始选课=============="
    courseList = []
    pattern = re.compile(r'\" onclick=\"selectThis\(\'.*\'')
    pos = 0
    m = pattern.search(text,pos)
    while m:
        pos = m.end()
        tempText = m.group()
        parameters = re.search(r"selectThis\('(.*?)','(.*?)','(.*?)'", tempText)
        course = [parameters.group(1),parameters.group(2),parameters.group(3),1]
        courseList.append(course)
        m=pattern.search(text,pos)  #寻找下一个
    times = 0
    success = 0
    total = len(courseList)
    while True:
        if total == 0:
            print u"目前没有课可以选择"
            break
        time.sleep(3)#sleep
        times = times +1
        print u"\n第"+str(times)+u"次选课，已经成功选择"+str(success)+u"门"
        for course in courseList:
            if course[3] == 1:
            #构造选课post
                posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh='+course[1]+'&select_xkkclx='+course[2]+'&select_jhkcdm='+course[0]
                headers = { 'Host' : 'xk.urp.seu.edu.cn',
                        'Proxy-Connection' : 'keep-alive',
                        'Content-Length' : '2',
                        'Accept' : 'application/json, text/javascript, */*',
                        'Origin':'http://xk.urp.seu.edu.cn',
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                        }
                data = {'{}':''
                }
                #post选课包，并获取返回状态
                (state, text) = postData(posturl,headers,data)
                if state == False:
                    text = '网络错误'
                else:
                    if text.find('isSuccess":"false') != -1:
                        state = False
                        text = re.search(r'errorStr":"(.*?)"', text).group(1)
                if state == True:
                    course[3] = 0
                    success += 1
                    total -= 1
                    print u"Nice, 课程"+str(course[0])+u" 选择成功"
                else:
                    print u"课程"+str(course[0])+u" 选课失败，" + text.decode('utf-8')

def postRw(courseNo):
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh='+courseNo+'&select_xkkclx=45&select_jhkcdm=00034&select_mkbh=rwskl'
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
    (state, text) = postData(posturl,headers,data)
    return (state, text)

def checkRwState(text):
    if text.find('true') != -1:  #选课成功
        return 0
    if text.find('名额已满') != -1:
        return 1
    if text.find('冲突') != -1:
        return 2
    return -1

def Mode2(semesterNum, url):
    (state, text) = selectSemester(semesterNum, url)
    if state == False:
        print text.decode('utf-8')
        print u'切换到学期' + str(semesterNum) + u"失败"
        return
    else:
        print u'切换到学期' + str(semesterNum) + u"成功"
    print u"==============开始选课=============="
    #获取人文课页面
    geturl1 = 'http://xk.urp.seu.edu.cn/jw_css/xk/runViewsecondSelectClassAction.action?select_jhkcdm=00034&select_mkbh=rwskl&select_xkkclx=45&select_dxdbz=0'
    header1 = {
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Accept' : 'application/json, text/javascript, */*',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }   
    data1 = {}
    (state, text) = getData(geturl1,header1,data1)
    if state == False:
        print u"打开课程列表页面失败"
        return

    #获取所有的课程编号
    pattern = ('\"8%\" id=\"(.{0,20})\" align')
    courseList = re.findall(pattern,text,re.S)
    #print courseList 
    courseCtList =[]
    #找出并去掉冲突的课程
    for course in courseList:
        (state, backText) = postRw(course)
        if state == True:  # ewww bad name here
            state = checkRwState(backText)
        else:
            state = -1  # network error or something else
        if state == 2:
            courseCtList.append(course)
        if state == 0:
            print u"Nice 选到了一门课："+course
            return   #成功了
    #print courseCtList
    courseTemp = [i for i in courseList if (i not in courseCtList)]
    #print courseTemp
    times = 0
    while True:
        times = times + 1
        #找出已满的课程
        pattern = ('已满.+?(\"8%\" id=\")(.{0,20})\" align')
        courseYmList = [i[1] for i in re.findall(pattern,text,re.S)]
        #print courseYmList
        #找出可以选的课程编号
        courseAva = [i for i in courseTemp if (i not in courseYmList) ]
        print courseAva
        #选课了
        if len(courseAva) == 0:
            print u"第"+str(times)+u"次刷新，每门课都选不了.."
        else:
            for course in courseAva:
                (state, text) = postRw(course)
                if state == True:
                    state = checkRwState(text)
                else:
                    state = -1
                if state == 0:
                    print u"Nice 选到了一门课："+course
                    return
                if state == 1:
                    print u"人品不好 眼皮子底下的课被抢了"
        #刷新人文选课界面
        (state, text) = getData(geturl1,header1,data1)
        if text.count('已选') == 3:  # in case of multi-instances
            print u"已经选到一门课了"
            break

        if state == False:
            print u"打开课程列表页面失败"
            return
        
        time.sleep(3)

def I_just_wanna_this_one(semesterNum,courseName, url, apilist):
    (state, text) = selectSemester(semesterNum, url)
    if state == False:
        print text.decode('utf-8')
        print u'切换到学期' + str(semesterNum) + u"失败"
        return
    else:
        print u'切换到学期' + str(semesterNum) + u"成功"
    print u"==============开始选课=============="
    #获取人文课页面
    
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
    #构造RE  
    #print text

    pattern = (courseName + '.*?(\"8%\" id=\"(.{0,20})\" align)')  # possible problem here??
    #获取课程编号
    try:
        courseNo = re.findall(pattern,text,re.S)[0][1]
    except IndexError:
        print "未找到有关课程，换个关键字再试一次？"

    #构造数据包
    posturl = "http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh="+courseNo+"&select_xkkclx="+apilist[1]+"&select_jhkcdm="+apilist[0]+"&select_mkbh=" + apilist[2]
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
    print u"我开始选课了,课程编号："+courseNo
    times = 0
    while True :
        #判断是否选到课
        times = times+1
        (state, text) = getData(posturl,header1,data1)
        if state == False:
            print "打开课程列表页面失败"
            return
        pattern2 = ('已选(.{0,200})align=\"')
        result = re.findall(pattern2,text,re.S)
        #print result
        success = len(result) #为0为不成功 继续
        if (success != 0) and (result[0].find(courseNo)!=-1):
            print u"Nice，已经选到课程:"+courseNo
            break
        #发送选课包
        print u"第"+str(times)+"次尝试选择课程"+courseNo+u",但是没选到！"
        (state, text) = postData(posturl,headers,data)
        time.sleep(3)#sleep
    return



if __name__ == "__main__":
    print u"\n\n"
    print u"===================================================================== "
    print u"                      ## 东大抢课脚本 ##"
    print u"              鲁迅说过，如果你抢到了课，你就会很快乐；"
    print u"              如果你抢到了课让别人没课可抢，双倍快乐。"
    # print u"     Goto https://github.com/Avalon to get more update"
    print u"===================================================================== "
    print u"  选择模式："
    print u"1. 同院竞争臭表脸模式：只值守主界面本院的所有“服从推荐”课程"
    print u"2. 暴力模式：值守子界面“人文社科类”任意一门课程，有剩余就选上"
    print u"3. 孤注一掷模式：只值守你指定的一门人文课"
    print u"4. 孤注一掷模式：只值守你指定的一门体育课"
    print u"AlERT! 模式3, 4只能检索英文，中文编码不成功，所以，，，就先这样"
    api = []
    mode = 4
    mode = input(u'\n选择使用哪种模式(1-4)-> ')
    # userId = raw_input(u'请输入一卡通号(如:213111111)：')
    # passWord = raw_input(u'请输入密码(如:65535)：')
    semester = input(u'选择学期编号(短学期:1，秋季:2，春季:3)-> ')

    inputCaptcha = True
    userName, passWord = read_from_config('config.ini')
    (state, text, url) = loginIn(userName, passWord, inputCaptcha)
    failTimes = 0
    if inputCaptcha == True and state == False:
        print text.decode('utf-8')

    if state == True:
        if 1 == mode:
            Mode1(semester, url)
        if 2 == mode:
            Mode2(semester, url)
        if 3 == mode:
            courseName = raw_input(u'请输入你想值守的人文课名称或者其关键词(如:音乐鉴赏)-> ')
            try:
                courseName.decode('utf-8')
            except:
                courseName.decode('gbk').encode('utf-8')  #handle the input from cmd
            api = ['00034','45','rwskl','15']
            I_just_wanna_this_one(semester,courseName, url, api)
        if 4 == mode:
            courseName = raw_input(u'请输入你想值守的体育课名称或者其关键词(如:棒垒球)-> ')
            try:
                courseName.decode('utf-8')
            except:
                courseName.decode('gbk').encode('utf-8')  #handle the input from cmd
            api = ['18M04000','34','18010014','13']
            I_just_wanna_this_one(semester,courseName, url, api)
    else:
        print u"要不试试退出后重新打开一下本程序？"
    input(u'按任意键退出...')


