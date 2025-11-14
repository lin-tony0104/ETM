#ETM_AEP =>ETM_AdmitEvictPolicy

from policies.BasePolicy import BasePolicy
from .cache import Cache,cache_obj
from .ETM import ETM

from collections import deque, defaultdict
import numpy as np
import random
import torch


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
        #DEBUG
        self.request_count = 0
        


    def request(self, o_id, o_size):
        o_id= int(o_id)  # 確保o_id是整數
        o_size = int(o_size)  # 確保o_size是整數
        #DEBUG
        self.request_count += 1
        #紀錄前L筆
        self.L_hist.append(o_id) #會自動維持L筆
        #紀錄batch
        self.batch.append(o_id)
        if len(self.batch) >= self.B + self.K + self.L:
            self.batch_pool.append(np.asarray(self.batch, dtype=np.int64))
            self.batch = []
            #train
            self.train(self.batch_pool,self.n_sample)
            print("======================= req_num: ",self.request_count)


        #取得熱門度預測值
        with torch.no_grad():
            hist_ids=torch.as_tensor(self.L_hist, dtype=torch.int64,device=self.device).unsqueeze(0)
            curr_ids=torch.as_tensor([o_id], dtype=torch.int64,device=self.device).unsqueeze(0)
            o_val = self.etm(hist_ids,curr_ids)
        
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
            if obj.o_val >= self.cache.cache_val:
                while(self.cache.remaining_space < obj.o_size):
                    #evict
                    self.cache.pop_min #驅逐val最小者
                self.cache.insert(obj)
            # not admit
            else:
                #noting to do 
                pass 
            return False #miss

    def train(self, batch_pool,n_sample=5):
        
        for _ in range(n_sample):
            #sample
            id_seq = random.choice(batch_pool)
            seq,target=get_traing_data(id_seq,self.L,self.K,self.B)# 若改成batch_pool內儲存這個  可以減少重複計算
        
            hist_ids=seq[:self.B+self.K-1]
            curr_ids=seq[self.K:self.K+self.B]

            # 轉成tensor 並加上batch維度
            hist_ids = torch.as_tensor(hist_ids, dtype=torch.int64,device=self.device).unsqueeze(0)
            curr_ids = torch.as_tensor(curr_ids, dtype=torch.int64,device=self.device).unsqueeze(0)
            target = torch.as_tensor(target, dtype=torch.float32,device=self.device).unsqueeze(0)

            self.optimizer.zero_grad()
            preds= self.etm(hist_ids,curr_ids)
            # loss_fn = torch.nn.PoissonNLLLoss(log_input=False)

            loss_fn = torch.nn.MSELoss()
            loss = loss_fn(preds, target)
            loss.backward()
            self.optimizer.step()
            print(f"Loss: {loss.item()}")
            





#輸入batch 回傳 訓練用seq, target
def get_traing_data(batch, L, K, B):  #len(batch)= B+K+L
    req_seq=batch[:B+K]
    target=[]
    counter = defaultdict(int)
    
    # 先處理好未來L筆的熱門度
    for i in range(L):
        o_id = batch[K+i]
        counter[o_id]+=1

    #紀錄熱門度(target)
    for i in range(B):
        tail_id = batch[K+L+i]
        head_id = batch[K+i]

        counter[tail_id]+=1
        counter[head_id]-=1
        target.append(counter[head_id])
        
        #用來防止記憶體洩漏
        if counter[head_id]<=0:
            del counter[head_id]
    target = np.asarray(target, dtype=np.int64)
    return req_seq , target