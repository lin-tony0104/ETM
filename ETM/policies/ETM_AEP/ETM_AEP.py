#ETM_AEP => ETM_AdmitEvictPolicy

from policies.BasePolicy import BasePolicy
from .cache import Cache,cache_obj
from .ETM import ETM

from collections import deque, defaultdict
import numpy as np
import random
import torch





class evict_policy:
    def __init__(self, cache):
        self.cache = cache

    def evict(self):
        victim = self.cache.pop_min()
        return victim


# admit用到的特徵
#   obj_size, obj_pop, obj_val
#   cache_avg_obj_size, cache_avg_obj_pop, cache_avg_val
#   val_gap ([obj_val - avg_val] 用來判斷是否能拉高平均)
# admit的訓練方法
#   
class admit_policy:
    def __init__(self, cache):
        self.cache = cache
        
        

    def admit(self, obj):
        return True  #永遠admit
    
    def train(self):
        pass
    


#策略
class ETM_AEP_policy(BasePolicy):
    def __init__(self,config):
        self.cache=Cache(config["cache_size"])
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.etm=ETM(config['ETM']).to(self.device)
        self.optimizer = torch.optim.Adam(self.etm.parameters(), lr=0.001)
        print("Using ",self.device," for ETM_AEP")


        self.L, self.K, self.B = config['ETM']['L'], config['ETM']['K'], config['ETM']['B']
        self.L_hist=deque([0]*self.L ,maxlen=self.L) #長度L的sliding window
        self.batch=[]
        self.batch_pool=deque(maxlen=config['batch_pool_size'])
        self.n_sample = config['n_sample']


        self.admit_policy=admit_policy(self.cache)
        self.evict_policy=evict_policy(self.cache)
        #DEBUG
        self.request_count = 0
        


    def request(self, o_id, o_size, o_features):
        o_id= int(o_id)  # 確保o_id是整數
        o_size = int(o_size)  # 確保o_size是整數
        o_pop= float(o_features[0]) #熱門度
        o_val= o_pop / o_size #價值密度 


        #DEBUG 
        self.request_count += 1

        #快取決策
        obj=cache_obj(o_id,o_size,o_val)
        if obj.o_size>self.cache.size:
            raise ValueError("物件大小大於整體快取大小")
        
        
        #hit
        if obj in self.cache:
            self.cache.update_obj(obj) #更新位置
            return True #hit
        else:
        #miss
            #admit
            if self.admit_policy.admit(obj):
                while(self.cache.remaining_space < obj.o_size):
                    self.evict_policy.evict()
                self.cache.insert(obj)
            # not admit
            else:
                #noting to do 
                pass 
            return False #miss






