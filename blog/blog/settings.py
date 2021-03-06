"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import blog
import config
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kt70%hfkxh+n@w(2c5$o*355^j_)hlij=^4fp*o_)%p9=4xeyp'

# Application definition

INSTALLED_APPS = [
    'bootstrap_admin',
    'django.contrib.admin',  # 系统后台组件
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'index',  # 首页
    'api',  # api接口
    'user',  # 登陆和用户后台
    'search',  # 站内搜索
    'set_config',  # 用户配置
    'tools',  # 用户工具
    'captcha',  # 验证码
    'haystack',  # 添加haystack组件
    'xadmin',  # 添加xadmin系统后台组件
    'crispy_forms',  # xadmin组件依赖
    'reversion',  # xadmin组件依赖
    'tinymce',    # 添加此行
    'notifications',  # 通知
    'index.templatetags',  # 作为app注册自定义过滤器
]

DJANGO_NOTIFICATIONS_CONFIG = {
    'SOFT_DELETE': True,
    'USE_JSONFIELD': True
}

TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',  # 设置主题
    'width': '100%',
    'height': 400,
}

LOGIN_URL = '/user/login'

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True

# 配置haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        # 设置搜索引擎，文件是index的whoosh_cn_backend.py
        'ENGINE': 'index.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
        'INCLUDE_SPELLING': True,
    },
}

# 设置每页显示的数据量
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
# 当数据库改变时，会自动更新索引，非常方便
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# django_simple_captcha 验证码基本配置
# 设置验证码的显示顺序，一个验证码识别包含文本输入框、隐藏域和验证码图片，该配置是设置三者的显示顺序
# CAPTCHA_OUTPUT_FORMAT = ' %(text_field)s %(hidden_field)s%(image)s'
CAPTCHA_OUTPUT_FORMAT = ' %(image)s&ensp;%(text_field)s%(hidden_field)s'
# 设置图片噪点
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null',  # 设置样式
                           # 'captcha.helpers.noise_arcs',# 设置干扰线
                           # 'captcha.helpers.noise_arcs_random',  # 设置自定义的干扰线
                           # 'captcha.helpers.noise_dots',# 设置干扰点
                           )

# 此间隔中的随机旋转将应用于质询文本中的每个字母。
CAPTCHA_LETTER_ROTATION = (-45, 45)

# 验证码字体
# CAPTCHA_FONT_PATH
# 渲染文本的字体大小
CAPTCHA_FONT_SIZE = 24
# 图片大小
CAPTCHA_IMAGE_SIZE = (120, 30)
# 设置图片背景颜色
# CAPTCHA_BACKGROUND_COLOR = '#76EE00'
CAPTCHA_BACKGROUND_COLOR = blog.RGB()
CAPTCHA_CHALLENGE_FUNCTARRAY = ['captcha.helpers.random_char_challenge',  # 图片中的文字为随机英文字母,
                                'captcha.helpers.word_challenge',  # 图片中的文字为英文单词
                                'captcha.helpers.math_challenge',  # 图片中的文字为数字表达式
                                ]
CAPTCHA_CHALLENGE_FUNCT = CAPTCHA_CHALLENGE_FUNCTARRAY[blog.get_config(
    config.CAPTCHA_CHALLENGE_FUNCT, 2)]
# 设置字符个数
CAPTCHA_LENGTH = blog.get_config(config.CAPTCHA_LENGTH, 4)
# 设置超时(minutes)
CAPTCHA_TIMEOUT = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # 使用中文
    # 'index.middleware.cros.CORS',  # 允许跨域
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'index/templates'),
                 os.path.join(BASE_DIR, 'user/templates'),
                 os.path.join(BASE_DIR, 'search/templates'),
                 os.path.join(BASE_DIR, 'tools/templates'),
                 os.path.join(BASE_DIR, 'set_config/templates'),
                 os.path.join(BASE_DIR, 'notifications/templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'

# 数据库配置
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
if blog.get_config(config.MYSQL, False):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 'NAME': blog.get_config(
                config.MYSQLDBNAME, 'blog_db'), 'USER': blog.get_config(
                config.MYSQLDBUSER, 'root'), 'PASSWORD': blog.get_config(
                    config.MYSQLDBPASSWD, 'password'), 'HOST': blog.get_config(
                        config.MYSQLDBHOST, '127.0.0.1'), 'PORT': blog.get_config(
                            config.MYSQLDBPORT, '3306'), 'OPTIONS': {
                                "init_command": "SET default_storage_engine='INNODB'"}}}
    # 排除错误
    DATABASES['default']['OPTIONS']['init_command'] = "SET sql_mode='STRICT_TRANS_TABLES'"
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                             'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# 时区配置
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = blog.get_config(config.LANGUAGE_CODE, 'zh-hans')

# TIME_ZONE = 'UTC'
TIME_ZONE = blog.get_config(config.TIME_ZONE, 'Asia/Shanghai')

USE_I18N = True

USE_L10N = True

USE_TZ = blog.get_config(config.USE_TZ, False)


# SECURITY WARNING: don't run with debug turned on in production!
# 项目上线时设置 DEBUG = False
DEBUG = blog.get_config(config.DEBUG, True)
# 允许所有域名访问
ALLOWED_HOSTS = blog.get_config(config.ALLOWED_HOSTS, ['*'])

# 配置自定义用户表MyUser
AUTH_USER_MODEL = 'user.MyUser'

# 配置CONTENT_TYPE防止IE和EDGE浏览器不渲染html页面
DEFAULT_CONTENT_TYPE = 'text/html'

# 静态文件配置
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
# STATIC_ROOT用于项目部署上线的静态资源文件
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
# STATICFILES_DIRS用于收集admin的静态资源文件
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

# 文件上传地址
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/uploads/hp/')
MEDIA_ROOT_FILE = os.path.join(BASE_DIR, 'static/uploads/file/')

# 邮件配置信息
EMAIL_USE_SSL = blog.get_config(config.EMAIL_USE_SSL, True)
EMAIL_HOST = blog.get_config(config.EMAIL_HOST, 'smtp.qq.com')
EMAIL_PORT = blog.get_config(config.EMAIL_PORT, 465)
EMAIL_HOST_USER = blog.get_config(config.EMAIL_HOST_USER, '')
EMAIL_HOST_PASSWORD = blog.get_config(config.EMAIL_HOST_PASSWORD, '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# 蛋蛋机器人配置
DANDANLOCAL = blog.get_config(config.DANDANLOCAL, True)
DANDANAPIKEY = blog.get_config(config.DANDANAPIKEY, "")
DANDANAPISECRET = blog.get_config(config.DANDANAPISECRET, "")

# 阿里云OSS文件
oss = blog.get_config(config.oss, False)
AccessKeyId = blog.get_config(config.AccessKeyId, '')
AccessKeySecret = blog.get_config(config.AccessKeySecret, '')
endpoint = blog.get_config(config.endpoint,
                           'https://oss-cn-shenzhen.aliyuncs.com')
BucketName = blog.get_config(config.BucketName, '')
is_cname = blog.get_config(config.is_cname, False)
cname = blog.get_config(config.cname, '')
connect_timeout = blog.get_config(config.connect_timeout, 30)
if oss:
    import oss2
    auth = oss2.Auth(AccessKeyId, AccessKeySecret)
    if is_cname:
        bucket = oss2.Bucket(
            auth,
            cname,
            BucketName,
            connect_timeout=connect_timeout,
            is_cname=True)
    else:
        bucket = oss2.Bucket(
            auth,
            endpoint,
            BucketName,
            connect_timeout=connect_timeout,
            is_cname=False)
