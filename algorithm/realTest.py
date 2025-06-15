#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Andy Freeman
# Date: 2025/4/28
# Description: Keep Hungry Keep Foolish

"""
题目描述：
### 问题
伍兹先生是廷伯兰市的一名电工，他在八条街灯的线路连接上出现了错误。这些错误会导致一盏街灯在其相邻的街灯在夜间要么都亮（用1表示），要么都不亮（用0表示）时熄灭。否则，这盏街灯将正常亮起。道路两端的街灯只有一个相邻街灯，所以道路一端的街灯在夜间总是熄灭。某一天街灯的状态被记录下来，不考虑同一天内的变化。

由于这个故障，人们在夜间驾车时遇到了困难。他们已向联邦公路管理局提出投诉。基于此投诉，局长要求提供一份M天后街灯状态的报告。

编写一个算法，输出给定M天后街灯的状态。

### 输入
第一行输入是一个整数 `currentState_size`，表示街灯的数量（记为N）。
接下来一行是由N个用空格分隔的整数组成的 `currentState`，表示街灯当前的状态（即0或1）。
最后一行是一个整数 `days`，表示经过的天数（记为M）。

### 输出
打印出八个用空格分隔的整数，表示M天后街灯的状态。

### 约束条件
1 ≤ `days` ≤ 10⁶

### 示例
**输入**：
8
1 1 1 0 1 1 1 1
2

**输出**：
0 0 0 0 0 1 1 0

**解释**：
位置0处的街灯，其相邻街灯是位置0（假设）和1处的街灯。所以第二天，它将为1。
位置1处的街灯，其相邻街灯都是1。所以第二天，它将为0。
位置2处的街灯，其相邻街灯是位置0和1处的街灯。所以第二天，它将为1。
位置3处的街灯是0，且其相邻街灯都是1。所以第二天，该位置的街灯将为0。
类似地，我们可以求出其余街灯第二天的状态。
所以第一天后街灯的状态是1 0 1 0 0 1 0 1。
两天后街灯的状态是0 0 0 0 0 1 1 0。
"""
def update_lights(currentState, days):
    n = len(currentState)
    for _ in range(days):
        new_state = [0] * n
        for i in range(n):
            if i in [0, n - 1]:
                new_state[i] = 1
            else:
                if currentState[i - 1] == currentState[i + 1]:
                    new_state[i] = 0
                else:
                    new_state[i] = 1
        currentState = new_state
    return currentState


# 参数校验
try:
    currentState_size = int(input("请输入个数："))
    currentState_str = input("请输入状态：").split()
    if len(currentState_str) != currentState_size:
        raise ValueError("currentState的元素个数和currentState_size不相等")
    currentState = []
    for num_str in currentState_str:
        num = int(num_str)
        if num not in [0, 1]:
            raise ValueError("currentState中的元素只能是0或1")
        currentState.append(num)
    days = int(input("请输入天数："))
    if not (1 <= days <= 10 ** 6):
        raise ValueError("days的取值应在1到10的6次方之间")
except ValueError as e:
    print(f"参数错误: {e}")
    exit(1)

result = update_lights(currentState, days)
print(' '.join(map(str, result)))

"""
### 题目翻译
一家公司在N个销售点销售其产品。所有销售点通过一系列道路相互连接。从任何一个销售点到另一个销售点都只有一条路。每个销售点都有唯一的ID。每当某一产品的库存达到最低水平时，K个销售点会请求额外库存。公司会从仓库向这些请求的销售点发送产品。为了节省燃料，仓库主管指示司机迈克沿着最短且最直接的路径向销售点配送产品，且任何一条路都不能走两次。

编写一个算法，帮助迈克在不重复经过任何道路的单次行程中，向尽可能多的销售点配送库存。

### 输入
第一行输入是一个整数 `num`，表示包括仓库在内的销售点总数（N）。
第二行输入是一个整数 `koutletsCount`，表示请求额外库存的销售点数量（K）。
第三行是由K个用空格分隔的整数组成，代表请求额外库存的销售点ID。
第四行是两个用空格分隔的整数 `numR` 和 `conOutlet`，`numR` 表示包括仓库在内的销售点之间道路的总数（M），`conOutlet` 表示与一条道路相连的销售点数量（X），且 `numR` 总是等于 `num - 1`，`conOutlet` 总是等于2。
接下来的M行，每行由X个用空格分隔的整数组成，代表通过道路相连的两个销售点。

### 输出
输出一个整数，表示迈克在单次行程中，不重复经过任何道路所能到达的最大销售点数量。

### 约束条件
0 ≤ `koutletsCount` ≤ `num` ≤ 10⁵
1 ≤ `num` ≤ 10⁵
1 ≤ A, B ≤ `num`；其中A、B代表通过道路相连的销售点
`numR` = `num` - 1

### 示例
**输入**：
4
3
2 3 4
3 2
3 2
1 2
1 3
1 4

**输出**：
2

**解释**：
在单次行程中，迈克只能到达两个销售点，例如[2, 3] 或 [2, 4] 或 [3, 4] ，因为要到达第三个销售点，他就必须重复走某条路，而这是不允许的。所以，输出为2。
"""

from collections import defaultdict


def dfs(node, target_set, visited, graph):
    visited.add(node)
    count = 1 if node in target_set else 0
    max_count = count
    for neighbor in graph[node]:
        if neighbor not in visited:
            sub_count = dfs(neighbor, target_set, visited, graph)
            max_count = max(max_count, count + sub_count)
    return max_count


num = int(input())
koutletsCount = int(input())
requested_outlets = set(map(int, input().split()))
numR, conOutlet = map(int, input().split())
graph = defaultdict(list)
for _ in range(num - 1):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

visited = set()
max_count = 0
for start in requested_outlets:
    visited.clear()
    count = dfs(start, requested_outlets, visited, graph)
    max_count = max(max_count, count)

print(max_count)


"""
### 代码解释
1. **图的构建**：
使用 `defaultdict(list)` 构建图结构 `graph` ，通过输入的道路连接信息，将每个销售点与其相邻销售点进行关联。
2. **深度优先搜索（DFS）函数**：
定义 `dfs` 函数，用于从一个起始节点开始进行深度优先搜索。函数接受当前节点 `node`、目标销售点集合 `target_set`、已访问节点集合 `visited` 和图结构 `graph` 作为参数。在函数内部，首先将当前节点标记为已访问，然后判断当前节点是否在目标集合中，统计当前节点的贡献。接着遍历当前节点的邻居节点，对未访问的邻居节点递归调用 `dfs` 函数，计算从该路径能到达的目标销售点的最大数量。
3. **主逻辑**：
通过输入获取销售点总数、请求库存的销售点数量及ID、道路信息等。然后以每个请求库存的销售点为起始点，调用 `dfs` 函数进行搜索，记录每次搜索能到达的最大目标销售点数量，最终输出这个最大值。 
"""
