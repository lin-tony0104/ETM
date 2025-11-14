from utils.MinHeap import MinHeap

#obj類別
class Cache_obj():
    def __init__(self,o_id,o_size):
        self.o_id=str(o_id)
        self.o_size=int(o_size)
        self.o_val=0
    def __lt__(self, other):
        return self.o_val < other.o_val
    def __gt__(self, other):
        return self.o_val > other.o_val
    def __eq__(self, other):    # dict需實作 
        return self.o_id == other.o_id
    def __hash__(self):         # dict需實作
        return hash(self.o_id)

#cache類別  
class Cache(MinHeap):
    def __init__(self,cache_size):
        super().__init__()
        self.size=cache_size #快取大小
        self.used=0 #已用空間
        self.cache_dict={}
    @property
    def remaining_space(self):
        return self.size-self.used

    def insert(self, val):
        if val in self.cache_dict:
            raise ValueError("Already in cache") #重複插入
        super.insert(val)
        self.used+=val.o_size
        self.cache_dict[val]=val

    def pop_min(self):
        victim=super().pop_min()
        self.used-=victim.o_size
        del self.cache_dict[victim]
        return victim
    

    def update_obj(self, val):
        if val not in self.index_dict:
            raise KeyError("Object not found in heap")        
            
        idx = self.index_dict[val]
        parent = (idx - 1) // 2
        if idx > 0 and self.heap[idx] < self.heap[parent]:
            self._bubble_up(idx)
        else:
            self._trickle_down(idx)      

        
#實作in 功能
    def __contains__(self,val):
        return val.o_id in self.cache_dict

    

