#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Andy Freeman
# Date: 2025/3/24
# Description: Keep Hungry Keep Foolish

import logging
import random

def self_defined_sort(l):
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            if l[i] > l[j]:
                l[i], l[j] = l[j], l[i]

    print(l)

def quick_sort(l):
    # 类型检查
    if not isinstance(l, list):
        raise TypeError('error Type, pls check')

    def _quick_sort(sub_list):
        if len(sub_list) <= 1:
            return sub_list
        else:
            # 随机选择基准值以提高性能
            pivot = random.choice(sub_list)
            less = [x for x in sub_list if x < pivot]
            equal = [x for x in sub_list if x == pivot]
            greater = [x for x in sub_list if x > pivot]
            return _quick_sort(less) + equal + _quick_sort(greater)

    # 调用内部函数并返回结果
    return _quick_sort(l)

# 示例调用
if __name__ == "__main__":
    sorted_list = quick_sort([3, 6, 8, 10, 1, 2, 1])
    print(sorted_list)
