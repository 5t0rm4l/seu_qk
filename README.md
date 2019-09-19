# seu_jwc_qk

## 依赖
暂时使用python2
configparser 读取.ini文件:
`pip install configparser`

## 使用方法
1. 修改`config.ini`文件，填上自己的一卡通与密码
2. `python(2) qk_win.py/qk_linux.py` 

## Todo
验证码自动识别

## 其他
1. 代码最初来自https://github.com/SnoozeZ/seu-jwc-fker
2. 新增了指定一门特定体育课的功能
3. 由于选修课学分下个学期就修够了，到了大三也没有自选的体育课了
（刚写完就得知这个痛苦的消息），所以这个脚本已经对我没用了，估计是不会更新了。。。以上

## 真香更新
1. 引入了适用于抢任意一门课的脚本，放在pro文件夹下面
2. 使用方法： 见pro/README.txt
3. 声明： 没打算做成傻瓜式操作，使用比较麻烦，要自己找接口的参数，方法见第二条。另外有空或许会移植到python3，不过现在已经能用了是不是:-)