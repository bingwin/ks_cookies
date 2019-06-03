'''
Created on 2018年7月30日

@author: EDZ
'''

import logging

class Logger():
    def __init__(self, logname, loglevel, logger):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        
        format_dict = {
               logging.DEBUG : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
               logging.INFO : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
               logging.WARNING : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
               logging.ERROR : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
               logging.CRITICAL : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            }

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(loglevel)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(filename=logname, encoding='utf-8')
        fh.setLevel(loglevel)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(loglevel)

        # 定义handler的输出格式
        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = format_dict[loglevel]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    
    def getlog(self):
        return self.logger
    