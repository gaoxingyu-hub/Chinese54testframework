#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/16 18:55
# @Author  : chuan.yang
# @File    : data_checker.py
# @Desc    : check data format is correct
import re

class ThDataChecker:
    @classmethod
    def is_ip(self,inputs):
        format = '((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))'
        pattern = re.match(format, inputs)
        if pattern is not None:
            return True
        else:
            return False