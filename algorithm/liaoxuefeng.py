#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Andy Freeman
# Date: 2025/6/27
# Description: Keep Hungry Keep Foolish


"""
杨辉三角定义如下：

          1
         / \
        1   1
       / \ / \
      1   2   1
     / \ / \ / \
    1   3   3   1
   / \ / \ / \ / \
  1   4   6   4   1
 / \ / \ / \ / \ / \
1   5   10  10  5   1
把每一行看做一个list，试写一个generator，不断输出下一行的list：
# 期待输出:
# [1]
# [1, 1]
# [1, 2, 1]
# [1, 3, 3, 1]
# [1, 4, 6, 4, 1]
# [1, 5, 10, 10, 5, 1]
# [1, 6, 15, 20, 15, 6, 1]
# [1, 7, 21, 35, 35, 21, 7, 1]
# [1, 8, 28, 56, 70, 56, 28, 8, 1]
# [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
"""


def traigles(num):
    n, l1, l2 = 1, [], []
    while n <= num:
        l2 = []
        if n == 1:
            l1 = [1]
            l2 = l1
        else:
            for i in range(n):
                if i == 0 or i == n - 1:
                    l2.append(1)
                else:
                    l2.append(l1[i - 1] + l1[i])
            l1 = l2
        n += 1
        # print(l2)
        yield l2


if __name__ == '__main__':
    for i in traigles(10):
        print(i)
