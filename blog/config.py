#配置完此文件请重启django
# 设置验证码字符个数
CAPTCHA_LENGTH = 4
# 项目上线时设置 DEBUG = False
DEBUG =True
#允许所有域名访问
ALLOWED_HOSTS = ['*']
# 设置图片中的文字
# 0 为随机英文字母  1 为英文单词  2 为数字表达式
CAPTCHA_CHALLENGE_FUNCT = 2
#设置MYSQL默认False
MYSQL=False
#数据库名称
MYSQLDBNAME='blog_db'
#数据库用户
MYSQLDBUSER='root'
#数据库密码
MYSQLDBPASSWD=''
#数据库主机
MYSQLDBHOST='127.0.0.1'
#数据库端口
MYSQLDBPORT='3306'
#设置语言
LANGUAGE_CODE= 'zh-hans'
#设置时区
TIME_ZONE = 'Asia/Shanghai'
# 邮件配置信息
EMAIL_USE_SSL = True
# 邮件服务器，如果是 163 改成 smtp.163.com
EMAIL_HOST = 'smtp.qq.com'
# 邮件服务器端口
EMAIL_PORT = 465
# 发送邮件的账号
EMAIL_HOST_USER = ''
# SMTP服务密码
EMAIL_HOST_PASSWORD = ''
#单单机器人本地状态 默认为True
DANDANLOCAL = True
#单单机器人APIKEY
DANDANAPIKEY = ""
#单单机器人APISECRET
DANDANAPISECRET = ""
#是否以utc时区存储时间到数据库
USE_TZ = False
