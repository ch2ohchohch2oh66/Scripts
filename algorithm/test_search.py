#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 测试search.py中的所有函数

import pytest
import io
import sys
from algorithm.search import binary_search, deep_first_search, dfs_maze

class TestBinarySearch:
    def test_normal_case(self):
        # 正常情况测试
        assert binary_search([1, 2, 3, 4, 5], 3) == 2
        assert binary_search([1, 3, 5, 7, 9], 7) == 3
        assert binary_search([1, 2, 3, 4, 5], 1) == 0
        assert binary_search([1, 2, 3, 4, 5], 5) == 4
    
    def test_not_found(self):
        # 未找到目标值
        assert binary_search([1, 2, 3, 4, 5], 6) == -1
        assert binary_search([1, 3, 5, 7, 9], 4) == -1
    
    def test_single_element(self):
        # 单元素数组
        assert binary_search([1], 1) == 0
        assert binary_search([1], 2) == -1
    
    def test_duplicate_elements(self):
        # 重复元素(返回任意匹配位置)
        result = binary_search([1, 2, 2, 2, 3], 2)
        assert result in [1, 2, 3]
    
    def test_error_cases(self):
        # 错误情况测试
        with pytest.raises(TypeError):
            binary_search(None, 1)
        with pytest.raises(TypeError):
            binary_search([], None)
        with pytest.raises(TypeError):
            binary_search("not a list", 1)


class TestDeepFirstSearch:
    def test_normal_case(self, capsys):
        # 创建一个简单的图进行测试
        graph = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]
        # 捕获标准输出
        deep_first_search(graph, (0, 0))
        captured = capsys.readouterr()
        # 确保输出包含所有节点值
        for i in range(9):
            assert str(i) in captured.out
    
    def test_isolated_graph(self, capsys):
        # 测试只有一个节点的图
        graph = [[0]]
        deep_first_search(graph, (0, 0))
        captured = capsys.readouterr()
        assert "1 : (0, 0) : 0" in captured.out


class TestDfsMaze:
    def test_simple_path(self):
        # 简单迷宫
        maze = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        start = (0, 0)
        end = (2, 2)
        path = dfs_maze(maze, start, end)
        # 验证路径存在且起点终点正确
        assert len(path) > 0
        assert path[0] == start
        assert path[-1] == end
        # 验证路径连续性
        for i in range(len(path)-1):
            x1, y1 = path[i]
            x2, y2 = path[i+1]
            # 确保只移动一步且是上下左右四个方向
            assert abs(x1-x2) + abs(y1-y2) == 1
    
    def test_blocked_maze(self):
        # 被阻塞的迷宫
        maze = [
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]
        start = (0, 0)
        end = (2, 0)
        path = dfs_maze(maze, start, end)
        # 没有通路，期望返回空列表
        assert len(path) == 0
    
    def test_complex_maze(self):
        # 复杂迷宫
        maze = [
            [0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]
        start = (0, 0)
        end = (4, 4)
        path = dfs_maze(maze, start, end)
        # 验证路径存在
        assert len(path) > 0
        assert path[0] == start
        assert path[-1] == end
    
    def test_error_cases(self):
        # 错误输入测试
        with pytest.raises(ValueError):
            dfs_maze([], (0, 0), (1, 1))
        with pytest.raises(TypeError):
            dfs_maze("not a maze", (0, 0), (1, 1))
        with pytest.raises(TypeError):
            dfs_maze([[0, 0], [0, 0]], [0, 0], (1, 1))
        with pytest.raises(ValueError):
            # 超出边界的终点
            dfs_maze([[0, 0], [0, 0]], (0, 0), (5, 5))
        
        maze = [[0, 0], [0, 0]]
        # 起点是墙
        maze[0][0] = 1
        assert dfs_maze(maze, (0, 0), (1, 1)) == []


if __name__ == "__main__":
    pytest.main(["-v", "test_search.py"]) 