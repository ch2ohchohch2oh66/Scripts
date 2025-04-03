#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Andy Freeman
# Date: 2025/3/24
# Description: Keep Hungry Keep Foolish

import logging
import random
from copy import deepcopy
from heapq import merge

'''
1. 排序算法
快速排序 (Quick Sort)
归并排序 (Merge Sort)
插入排序 (Insertion Sort)
冒泡排序 (Bubble Sort)
堆排序 (Heap Sort)
选择排序 (Selection Sort)
计数排序 (Counting Sort)
'''


'''
1.1 快速排序 (Quick Sort)
快速排序是一种分治法算法，平均时间复杂度为O(n log n)，最坏情况为O(n²)，但常常表现得非常好。其核心思想是通过一个基准值将数组分成左右两部分，左边的值小于基准，右边的值大于基准，然后递归地对左右两部分进行排序。
步骤：
从数组中选择一个元素作为基准值（通常选择第一个、最后一个或中间的元素）。
将比基准值小的元素移动到基准值的左边，比基准值大的元素移动到右边。
递归地对左右两个子数组进行相同的操作。
'''
def quick_sort(l):
    if not isinstance(l, list):
        raise TypeError('Error Type, pls check')
    if len(l) <= 1:
        return l
    pivot = random.choice(l)
    less = [x for x in l if x < pivot]
    equal = [x for x in l if x == pivot]
    greater = [x for x in l if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)

'''
1.2 归并排序 (Merge Sort)
归并排序是一种分治法算法，其基本思想是将一个数组分成两个子数组，分别对它们进行排序，然后将排序后的子数组合并成一个有序的数组。时间复杂度是O(n log n)，是一个稳定的排序算法。
步骤：
将数组分割成两半，分别递归排序。
合并两个已排序的子数组。
重点在于：merge(*iterables, key=None, reverse=False)方法的输入是有序可迭代参数，比如[3,6,7],[1,5,9],则会合并输出一个有序的可迭代对象。
关键思路：递归拆分给定的可迭代类型参数，直到拆分为len(l)==2的场景，则下一步merge(l1,l2)，从而实现最小单元的可迭代参数的有序合并，依次类推，返回更多有序参数的有序合并结果。
'''
def merge_sort(l):
    if not isinstance(l, list):
        raise TypeError('Error Type, pls check')
    if len(l) <= 1:
        return l
    m = len(l) // 2
    left = merge_sort(l[:m])
    right = merge_sort(l[m:])
    return merge(left, right)


'''
1.3 插入排序 (Insertion Sort)
插入排序是一种简单的排序算法，它的基本思路是将数组分成已排序和未排序两部分，然后将未排序的元素逐一插入已排序部分。时间复杂度为O(n²)，适合小规模数据。
步骤：
从第二个元素开始，与前面的元素进行比较，找到合适的位置插入。
重复该过程直到数组排序完成。
'''
def insert_sort(l):
    if len(l) <= 1:
        return l
    result = l[0:1]
    temp = l[1:]
    for i in range(len(temp)):
        for j in range(len(result)):
            if temp[i] <= result[j]:
                result.insert(j, temp[i])
                break
            elif j == len(result) - 1:
                result.insert(j+1, temp[i])
        print(result)
    return result





'''
1.4 冒泡排序 (Bubble Sort)
冒泡排序通过重复地交换相邻的元素，直到整个数组有序。它的时间复杂度为O(n²)，在性能上不如快速排序和归并排序，适合小数据量排序。
步骤：
从头到尾扫描一遍数组，将相邻元素比较并交换位置，使得大的元素逐渐“冒泡”到数组的尾部。
对剩余的部分重复相同的过程，直到整个数组排序完成。
'''

'''
1.5 堆排序 (Heap Sort)
堆排序是一种基于比较的排序算法，它利用堆数据结构来排序。时间复杂度是O(n log n)，是一个不稳定的排序算法。
步骤：
构建最大堆。
将堆顶元素与数组的最后一个元素交换，并且重新调整堆，重复这个过程直到排序完成。
'''

'''
1.7 计数排序 (Counting Sort)
计数排序是一种非比较型排序算法，适用于排序范围较小的整数。时间复杂度为O(n + k)，其中n是元素个数，k是元素范围。它是一个稳定的排序算法。
步骤：
创建一个计数数组，记录每个元素的出现次数。
根据计数数组填充输出数组。
'''

# 示例调用
if __name__ == "__main__":
    l = [9, 3, 6, 8, 10, 1, 2, 1]
    sort_result = insert_sort(l)
    print(sort_result)

