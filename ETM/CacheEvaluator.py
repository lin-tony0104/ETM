import pickle

class CacheEvaluator():
    def __init__(self,config, exp_name):
        self.exp_name=exp_name
        self.verbose=config["verbose"]#秀細節
        self.region=config["region"]
        self.requests=0
        self.hits=0
        self.cum_hits_rate=[] # 用來計算累計
        self.region_hits_rate=[]
        self.prev_hits =0#前個region的累積hits數


    def hit_rate(self,hit,req):
        return round(hit/req,4) if req else 0 #避免除0

    #
    def record(self,hit):
        self.requests+=1        
        if hit:
            self.hits+=1
        if not self.requests%self.region:
            region_hit=self.hits-self.prev_hits
            self.cum_hits_rate.append(round(self.hits / self.requests,4))
            self.region_hits_rate.append(round(region_hit / self.region,4))
            if self.verbose:
                print("exp: "+self.exp_name+" req: ",self.requests ," hit_rate: ",self.cum_hits_rate[-1] ," region_hit_rate: ",self.region_hits_rate[-1])
            
            self.prev_hits=self.hits

    
    def save_result(self):
        save_data={
            "region":self.region,
            "cum_hits_rate":self.cum_hits_rate,
            "region_hits_rate":self.region_hits_rate
        }

        with open("experiments/"+self.exp_name+"/result/result.pkl","wb") as f:
            pickle.dump(save_data,f)
