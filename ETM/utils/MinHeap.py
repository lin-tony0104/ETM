class MinHeap:
    def __init__(self):
        self.heap = []
        self.index_dict = {}  # 物件 -> index

    def insert(self, val):
        self.heap.append(val)
        i = len(self.heap) - 1
        self.index_dict[val] = i
        self._bubble_up(i)

    def pop_min(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        if len(self.heap) == 1:
            val = self.heap.pop()
            del self.index_dict[val]
            return val

        min_val = self.heap[0]
        last_val = self.heap.pop()
        self.heap[0] = last_val
        self.index_dict[last_val] = 0
        del self.index_dict[min_val]
        self._trickle_down(0)
        return min_val


    def _bubble_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i] < self.heap[parent]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _trickle_down(self, i):
        size = len(self.heap)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i
            if left < size and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < size and self.heap[right] < self.heap[smallest]:
                smallest = right
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.index_dict[self.heap[i]] = i
        self.index_dict[self.heap[j]] = j


if __name__ == "__main__":
    h = MinHeap()

    #測試 insert
    h.insert(5)
    h.insert(3)
    h.insert(8)
    h.insert(1)
    assert h.heap == [1,3,8,5]

    #測試 index_dict
    assert h.index_dict[1] == 0
    assert h.index_dict[3] == 1
    assert h.index_dict[8] == 2
    assert h.index_dict[5] == 3
   
    #測試 pop_min
    assert h.pop_min() == 1
    assert h.pop_min() == 3
    assert h.heap == [5, 8] or h.heap == [8, 5]  # 根據 swap 結果可能不同順序
    assert set(h.index_dict.keys()) == {5, 8} 

    #測試 空heap報錯
    h=MinHeap()
    try:
        h.pop_min()
    except IndexError as e:
        assert str(e) == "Heap is empty"
    
    print("all pass")

