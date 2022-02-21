"""Logging: tracking events while running a program"""

import os
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

class LogFname:
    def __init__(self,log_dir: str, filename: str):
        self.__par_dir = log_dir
        self.__now = datetime.now()
        self.__fname = filename

    @property
    def __get_current_date(self):
        return self.__now.strftime('%y-%m-%d')


    @property
    def __get_tree_dir(self):
        return os.path.join(self.__par_dir,self.__get_current_date)

    @property
    def __get_tree_fname(self):
        return os.path.join(self.__get_tree_dir,self.__fname)

    def make_log_fname(self):

        if not os.path.isdir(self.__get_tree_dir):
            os.makedirs(self.__get_tree_dir)
        return self.__get_tree_fname


class LogHandler():
    def __init__(self):
        self.__format = logging.Formatter(
            fmt='[%(asctime)s  File %(filename)s:: function %(funcName)s::line no %(lineno)d  %(name)s] %(levelname)s: %(message)s',
            datefmt='%I:%M:%S %p')

    def file(self, log_dir:str, fname:str, level:str):
        self.__file_handler = logging.FileHandler(
            filename=LogFname(log_dir,fname).make_log_fname(),
            mode='a')
        self.__file_handler.setFormatter(fmt=self.__format)
        self.__file_handler.setLevel(level=level)
        return self.__file_handler

    def rotating_file(self, log_dir:str, fname:str, level:str, max_bytes:int, backup_count:int):
        self.__rotating_file_handler = RotatingFileHandler(
            filename=LogFname(log_dir,fname).make_log_fname(),
            mode='a', maxBytes=max_bytes, backupCount=backup_count)
        self.__rotating_file_handler.setFormatter(fmt=self.__format)
        self.__rotating_file_handler.setLevel(level=level)
        return self.__rotating_file_handler

    def stream(self,level:str):
        self.__stream_handler = logging.StreamHandler()
        self.__stream_handler.setFormatter(fmt=self.__format)
        self.__stream_handler.setLevel(level=level)
        return self.__stream_handler
    
class LogManager():

    def __init__(
        self, filename:str,
        log_dir='logs', logger_level='INFO',
        file_level='ERROR', rotating_file_level = None,
        stream_level=None, max_bytes=2000, backup_count=10
        ):

        self.name = __name__
        self.dir_log = log_dir
        self.fname = filename
        self.logger_level = logger_level
        self.file_level = file_level
        self.rotating_file_level = rotating_file_level
        self.max_bytes= max_bytes
        self.backup_count = backup_count
        self.stream_level = stream_level
       

    @property
    def logger(self):
        self.__logger = logging.getLogger(name=self.name)
        self.__logger.setLevel(level=self.logger_level)

        if self.file_level:
            self.__logger.addHandler(LogHandler().file(self.dir_log,self.fname,self.file_level))

        if self.rotating_file_level:
            self.__logger.addHandler(
                LogHandler().rotating_file(self.dir_log, self.fname,
                self.rotating_file_level, self.max_bytes, self.backup_count )
                )

        if self.stream_level:
            self.__logger.addHandler(LogHandler().stream(self.stream_level))

        return self.__logger

if __name__ == '__main__':
    log_manager = LogManager(filename='app.log',file_level='WARNING').logger
    try:
        log_manager.info('Trying to open the file')
        file = open('file.txt','r')
        try:
            log_manager.info('Trying to read the file content')
            content = file.readline()
        finally:
            file.close()
    except IOError as e:
        log_manager.error(str(e))
