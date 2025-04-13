#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Andy Freeman
# Date: 2025/4/5
# Description: Keep Hungry Keep Foolish

'''
2.1 二分查找 (Binary Search)

题目描述：
给定一个已排序的数组和一个目标值，使用二分查找（Binary Search）查找该目标值的位置。如果目标值存在，返回其索引；如果不存在，返回 -1。

题目解析：
- 问题的核心：我们可以将数组分成两半，通过比较目标值与中间元素的大小来缩小查找范围。每次将数组大小减半，直到找到目标值或数组为空。
- 二分查找的时间复杂度是 O(log n)，由于每次查找会将搜索范围减少一半。

控制流图设计思路：
1. 开始：初始化 `low = 0` 和 `high = len(arr) - 1`。
2. 循环：在 `low <= high` 的条件下进行循环：
    - 计算中间元素 `mid = (low + high) // 2`。
    - 如果 `arr[mid] == target`，返回 `mid`（目标元素找到了）。
    - 如果 `arr[mid] < target`，说明目标在右边，更新 `low = mid + 1`。
    - 如果 `arr[mid] > target`，说明目标在左边，更新 `high = mid - 1`。
3. 结束：如果 `low > high`，返回 -1（未找到目标）。

控制流图：
- 开始 -> 初始化 `low` 和 `high` -> 判断 `low <= high`
  - 是 -> 计算 `mid` -> 判断 `arr[mid] == target`
    - 是 -> 返回 `mid` -> 结束
    - 否 -> 判断 `arr[mid] < target`
      - 是 -> 更新 `low = mid + 1` -> 继续循环
      - 否 -> 更新 `high = mid - 1` -> 继续循环
  - 否 -> 返回 -1 -> 结束
'''
def binary_search(arr, target):
    if not arr or not target or not isinstance(arr, list):
        raise TypeError('Error Type, pls check')
    
    start_index = 0
    end_index = len(arr)-1
    
    while start_index <= end_index:
        mid_index = (start_index + end_index) // 2
        if arr[mid_index] == target:
            return mid_index
        elif arr[mid_index] > target:
            end_index = mid_index - 1
        else:
            start_index = mid_index + 1
    return -1

'''
2.2 深度优先搜索 (DFS)

题目描述：
给定一个图，使用深度优先搜索（DFS）遍历所有节点。

题目解析：
- DFS基本思想：从图中的一个起始节点开始，访问该节点并标记为已访问，然后递归访问该节点的所有未访问邻居节点。DFS可以通过栈来实现，也可以用递归实现。
- 时间复杂度：O(V + E)，其中V是图中的顶点数，E是图中的边数。

控制流图设计思路：
1. 开始：选择一个起始节点，将其标记为已访问。
2. 递归：对于每个未访问的邻居节点，递归进行DFS。
3. 结束：当没有未访问的邻居时，DFS结束。

控制流图：
- 开始 -> 标记当前节点为已访问 -> 遍历所有邻居节点
  - 未访问 -> 递归调用DFS
  - 已访问 -> 跳过
- 结束：当所有节点都被访问过时。
'''
def deep_first_search(graph, start_node):
    direction = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    row = len(graph)
    col = len(graph[0])
    visited = [[0 for _ in range(col)] for _ in range(row)]
    count = 0
    def _dfs(node):
        nonlocal count
        count += 1
        x, y = node
        visited[x][y] = 1
        print(f'{count} : {node} : {graph[x][y]}')
        for dx, dy in direction:
            nx, ny = x + dx, y + dy
            if 0 <= nx < row and 0 <= ny < col and visited[nx][ny] == 0:
                new_node = (nx, ny)
                _dfs(new_node)

    _dfs(start_node)

'''
问题描述： 给定一个二维迷宫，其中 0 表示可以通过的路径，1 表示障碍物或墙壁。
起点为 (0, 0)，终点为 (m-1, n-1)，要求找到从起点到终点的一条路径。
'''
def dfs_maze(maze, start, end):
    """
    使用深度优先搜索寻找迷宫中从起点到终点的路径
    
    Args:
        maze (List[List[int]]): 二维迷宫,0表示通路,1表示墙
        start (tuple): 起点坐标 (x,y)
        end (tuple): 终点坐标 (x,y)
    
    Returns:
        List[tuple]: 从起点到终点的路径,如果不存在则返回空列表
    """
    # 输入验证
    if not maze or not start or not end:
        raise ValueError('迷宫、起点或终点不能为空')
    if not isinstance(maze, list) or not isinstance(maze[0], list):
        raise TypeError('迷宫必须是二维列表')
    if not isinstance(start, tuple) or not isinstance(end, tuple):
        raise TypeError('起点和终点必须是元组类型')
        
    # 检查起点和终点是否有效
    row, col = len(maze), len(maze[0])
    if not (0 <= start[0] < row and 0 <= start[1] < col and
            0 <= end[0] < row and 0 <= end[1] < col):
        raise ValueError('起点或终点超出迷宫范围')
    if maze[start[0]][start[1]] == 1 or maze[end[0]][end[1]] == 1:
        return []

    # 初始化
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右下左上,顺时针方向
    visited = set()
    path = []
    
    def is_valid(x, y):
        """检查坐标是否有效且可通行"""
        return (0 <= x < row and 0 <= y < col and 
                maze[x][y] == 0 and (x, y) not in visited)

    def _dfs(current):
        if current == end:
            return True
            
        visited.add(current)
        path.append(current)
        
        for dx, dy in directions:
            next_x, next_y = current[0] + dx, current[1] + dy
            if is_valid(next_x, next_y):
                if _dfs((next_x, next_y)):
                    return True
                    
        path.pop()
        return False

    return path if _dfs(start) else []
'''
2.3 广度优先搜索 (BFS)

题目描述：
给定一个图，使用广度优先搜索（BFS）遍历所有节点。

题目解析：
- BFS基本思想：从图中的一个起始节点开始，首先访问该节点的所有邻居节点（按层次），然后再依次访问邻居节点的邻居，直到所有节点都被访问。
- BFS通常通过队列来实现。
- 时间复杂度：O(V + E)，与DFS类似，V是顶点数，E是边数。

控制流图设计思路：
1. 开始：选择一个起始节点，将其标记为已访问并入队。
2. 队列：从队列中取出当前节点，访问该节点的所有未访问邻居，并将其入队。
3. 结束：直到队列为空时，BFS结束。

控制流图：
- 开始 -> 入队起始节点 -> 队列非空？
  - 是 -> 出队节点 -> 遍历所有邻居节点
    - 未访问 -> 入队并标记为已访问
  - 否 -> 结束

'''


'''

2.4 寻找数组中的最大/最小元素

题目描述：
给定一个数组，找出该数组中的最大元素或最小元素。

题目解析：
- 问题核心：遍历数组中的每个元素，保持一个最大值或最小值的变量，不断更新该变量。
- 时间复杂度：O(n)，因为需要遍历数组中的每个元素。

控制流图设计思路：
1. 开始：初始化一个最大/最小值为数组的第一个元素。
2. 遍历：遍历数组中的每个元素，更新最大值/最小值。
3. 结束：返回最大值或最小值。

控制流图：
- 开始 -> 初始化最大/最小值 -> 遍历数组
  - 比较当前元素与最大/最小值
    - 更新最大/最小值
- 结束：返回最大/最小值

'''


'''

2.5 查找缺失的数字 (例如：1到N的数组中缺失一个数字)

题目描述：
给定一个包含1到N的整数数组（但是缺少了一个数字），找到缺失的数字。

题目解析：
- 思路：可以通过求和公式 `S = n * (n + 1) / 2` 计算1到N的总和，然后与数组元素的和进行比较，差值即为缺失的数字。
- 时间复杂度：O(n)，遍历数组一次。

控制流图设计思路：
1. 开始：计算1到N的总和。
2. 遍历：计算数组中所有元素的和。
3. 计算差值：用总和减去数组和，得到缺失的数字。
4. 结束：返回缺失的数字。

控制流图：
- 开始 -> 计算总和S -> 遍历数组计算数组和
- 计算差值 -> 返回差值

'''


'''

2.6 寻找重复元素 (例如：寻找数组中重复的数字)

题目描述：
给定一个数组，找到其中重复的元素。

题目解析：
- 思路：可以通过哈希表（或集合）来记录已经遇到的元素，每次遇到重复的元素时就返回。
- 时间复杂度：O(n)，通过哈希表或集合，查找和插入的平均时间复杂度为O(1)。

控制流图设计思路：
1. 开始：初始化一个空的集合来存储已访问的元素。
2. 遍历：遍历数组中的每个元素，检查该元素是否已在集合中。
    - 如果存在，则说明该元素重复，返回该元素。
    - 如果不存在，则将其添加到集合中。
3. 结束：遍历结束后，如果没有发现重复元素，可以返回一个指示没有重复的标志。

控制流图：
- 开始 -> 初始化空集合 -> 遍历数组
  - 如果元素在集合中 -> 返回该元素
  - 如果元素不在集合中 -> 将其添加到集合
- 结束

'''

if __name__ == '__main__':
    # l = [3,4,5,6,7]
    # target = 7
    # result = binary_search(l, target)
    # print(result)

    # graph = [[0, 1, 2, 3, 4],
    #       [10, 11, 12, 13, 14],
    #       [20, 21, 22, 23, 24],
    #       [30, 31, 32, 33, 34],
    #       [40, 41, 42, 43, 44],
    #       [50, 51, 52, 53, 54],
    #       [60, 61, 62, 63, 64]]
    # deep_first_search(graph, (3, 2))

    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0]
    ]
    start = (0, 0)
    end = (4, 4)
    print(dfs_maze(maze, start, end))