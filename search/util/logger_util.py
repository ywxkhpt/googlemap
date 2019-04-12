#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志记录类
"""
import logging
import logging.config
from path_util import *


def log_util():
    path = path_dir_parent(__file__)
    logging_path = os.path.join(path + '/configure/logging.ini')
    logging.config.fileConfig(logging_path)


if __name__ == "__main__":
    log_util()
