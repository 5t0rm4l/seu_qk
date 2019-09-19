## 根据“另行选择”页面更改config.ini配置文件

- 课程列表url的参数前三个元素在弹出窗口的url里面，最后一个元素课程编号在每个课程tr标签里面的最后一个td标签里面：`<td width="8%" id="xxxx" align="center">`
- post 的抢课接口为`runSelectclassSelectionAction.action?select_jxbbh=xxx&select_xkkclx=xxx&select_jhkcdm=xxx&select_mkbh=xxx&dxdbz=xxx`, 一共四个参数可以从源码Body开头的input标签里面找到
- eg.链接参数为select_jhkcdm=00034&select_mkbh=rwskl&select_xkkclx=45&select_dxdbz=0，课程编号为GR0003410201920, 开头标签为

'''
<input type="hidden" id="select_xkkclx" value="11">
<input type="hidden" id="select_jhkcdm" value="02084011">
<input type="hidden" id="select_mkbh" value="02084011">
<input type="hidden" id="select_xn" value="">
<input type="hidden" id="select_xq" value="">
<input type="hidden" id="select_dxdbz" value="0.com">
'''

## config.ini写为
[global]
user_id = xxx
passwd = xxx
jhkcdm = 00034
mkbh = rwskl
xkkclx = 45
course_id = GR0003410201920
select_xkkclx = 11
select_jhkcdm = 02084011
select_mkbh = 02084011
select_xkkclx = 0.com
### 对应洪海军老师的音乐鉴赏这门课

## 另外你填完参数会注意到有几个是相同的，我担心有的课会不一样所以也没去重
