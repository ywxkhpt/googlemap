#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
获取当前文件所在目录
"""

import os


def path_dir(file_path):
    return os.path.dirname(file_path)


def path_dir_parent(file_path):
    return os.path.dirname(os.path.dirname(file_path))


def path_dir_children(file_path, dir_name):
    return os.path.dirname(file_path) + "/" + dir_name


if __name__ == "__main__":
    print(__file__)
    print(path_dir(__file__))
    print(path_dir_parent(__file__))
    print(path_dir_children(__file__, "children"))
