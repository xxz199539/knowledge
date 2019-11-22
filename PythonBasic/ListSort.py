# -*- coding:utf-8 -*=


class SortList(object):

    def __init__(self, aList):
        for param in aList:
            if not (isinstance(param, int) or isinstance(param, float)):
                raise Exception("want int or float")
        self.aList = aList

    # 选择排序
    def select_sort(self):
        for i in range(len(self.aList)):
            max_index = i
            for j in range(i, len(self.aList)):
                if self.aList[j] > self.aList[max_index]:
                    self.aList[j], self.aList[max_index] = self.aList[max_index], self.aList[j]
        return self.aList

    # 插入排序
    def insert_sort(self):
        for i in range(len(self.aList)):
            for j in range(i, len(self.aList)):
                if self.aList[i] > self.aList[j]:
                    self.aList[i:j + 1] = [self.aList[j]] + self.aList[i:j]
        return self.aList

    # 快速排序
    def quick_sort(self, start, end):
        if start >= end:
            return
        i, j = start, end
        base = self.aList[i]
        while i < j:
            while (i < j) and (self.aList[j] >= base):
                j -= 1
            self.aList[i] = self.aList[j]
            while (i < j) and (self.aList[i] <= base):
                i += 1
            self.aList[j] = self.aList[i]
        self.aList[i] = base
        self.quick_sort(start, i - 1)
        self.quick_sort(i + 1, end)
        return self.aList

    # 希尔排序
    def shell_sort(self):
        gap = len(self.aList) // 2
        while gap > 0:
            for i in range(gap, len(self.aList)):
                while i >= gap and self.aList[i - gap] > self.aList[i]:
                    self.aList[i - gap], self.aList[i] = self.aList[i], self.aList[i - gap]
                    i -= gap
            gap //= 2
        return self.aList

    # 归并排序
    def merge_sort(self, aList=None):

        def merge(left, right):
            res = []
            l, r = 0, 0
            while l < len(left) and r < len(right):
                if left[l] < right[r]:
                    res.append(left[l])
                    l += 1
                else:
                    res.append(right[r])
                    r += 1
            res += left[l:]
            res += right[r:]
            return res

        sort_list = aList if aList else self.aList
        if len(sort_list) <= 1:
            return sort_list
        num = len(sort_list) // 2
        left = self.merge_sort(sort_list[:num])
        right = self.merge_sort(sort_list[num:])
        return merge(left, right)
