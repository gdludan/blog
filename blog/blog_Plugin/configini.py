#! /usr/bin/python3
# -*- coding:UTF-8 -*-
# time : 2019/4/14  17:35
# file : configini.py
# By 卤蛋
import configparser
import os

config = configparser.ConfigParser()
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
configPath = path + '\\config.ini'

# 读配置文件，返回读取到的内容，当没有读取内容时返回value


def iniread(filename, section, option, value='', encoding='utf-8'):
    config = configparser.ConfigParser()
    config.read(filename, encoding=encoding)
    tempstr = config.get(section, option)
    return tempstr if(tempstr) else value

# 写配置文件，返回True为写入成功，返回False则为失败


def iniwrite(filename, section, option, value='', encoding='utf-8'):
    config = configparser.ConfigParser()
    config.read(filename, encoding=encoding)

    def sectionIsOnFile(section):
        for key, value in config.items():
            if section == key:
                return True
        return False
    if sectionIsOnFile(section):
        try:
            config.set(section, option, value)
            config.write(open(filename, 'w', encoding=encoding))
            return True
        except BaseException:
            print('写入文件失败')
            return False
    else:
        try:
            config.add_section(section)
            config.set(section, option, value)
            config.write(open(filename, 'w', encoding=encoding))
            return True
        except BaseException:
            print('写入文件失败')
            return False

# 读写配置文件(ini)


class configIni(object):
    def __init__(self, configPath=path + '\\config.ini', encoding='utf-8'):
        self.configPath = configPath
        self.config = config
        self.encoding = encoding
        self.config.read(self.configPath, encoding=self.encoding)

    def __str__(self):
        str1 = ''
        i = 0
        for key, value in self.items():
            for k, v in value.items():
                i = i + 1
                temp = '###' * 4 + ' ' + str(i) + ' ' + '###' * 4
                str1 = str1 + temp + '\n配置节名称：' + key +\
                    '\n配置项名称：' + k + '\n配置项的值：' + v + '\n'
        return str1

    # 获取一个配置节内的配置项的值，返回True为成功，否则为不成功
    # 当无法获取到值时，返回value，建议value值设置成初始化的内容
    def getIni(self, section, option, value=''):
        try:
            str = self.config.get(section, option)
        except BaseException:
            return value
        else:
            return str if(str != '') else value

    # 检查配置节是否已存在文件内，返回True为存在，否则为不存在
    def sectionIsOnFile(self, section):
        for key, value in self.items():
            if section == key:
                return True
        return False

    # 检查配置项是否已存在文件内，返回True为存在，否则为不存在
    def optionIsOnFile(self, section, option):
        for key, value in self.items():
            for k, v in value.items():
                if option == k and section == key:
                    return True
        return False

    # 设置已经存在的配置节内的配置项的值，返回True为成功，否则为不成功
    def setIni(self, section, option, value=''):
        try:
            if not self.sectionIsOnFile(section):
                print('配置节[{}]不存在'.format(section))
                return False
            self.config.set(section, option, value)
            self.config.write(
                open(
                    self.configPath,
                    'w',
                    encoding=self.encoding))
            return True
        except BaseException:
            print('写入文件失败')
            return False

    # 添加一个配置节，不存在时，创建一个配置节，返回True为成功，否则为不成功
    def add_section(self, section):
        if not self.sectionIsOnFile(section):
            try:
                self.config.add_section(section)
                self.config.write(
                    open(
                        self.configPath,
                        'w',
                        encoding=self.encoding))
            except BaseException:
                print('写入文件失败')
                return False
        return True

    # 添加一个值，配置节不存在时，创建一个配置节，返回True为成功，否则为不成功
    def add(self, section, option, value, config=None):
        if config:
            self.config = config
        try:
            if not self.sectionIsOnFile(section):
                self.config.add_section(section)
                self.config.set(section, option, value)
                self.config.write(
                    open(
                        self.configPath,
                        'w',
                        encoding=self.encoding))
            else:
                self.config.set(section, option, value)
                self.config.write(
                    open(
                        self.configPath,
                        'w',
                        encoding=self.encoding))
            return True
        except BaseException:
            print('写入文件失败')
            return False

    # 返回配置文件内所有的配置节名称
    def sections(self): return self.config.sections()

    # 返回配置文件内所有的配置项名称
    def options(self, section): return self.config.options(section)

    # 返回配置文件内可遍历的(键,值)元组数组
    def items(self): return self.config.items()

    # 返回一个类表格的字符串
    def table(self):
        str = '--' * 28 + '\n配置节名称\t配置项名称\t值\n' + '--' * 28
        for key, value in self.items():
            for k, v in value.items():
                str1 = '\t' if(len(key) > 4) else '\t\t'
                str2 = '\t' if(len(k) > 4) else '\t\t'
                str = str + '\n[' + key + ']' + str1 + k + str2 + v
        return str
