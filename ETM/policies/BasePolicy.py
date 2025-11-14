"""
因為 run.py要呼叫request()
所以 限制policy一定都要實現 request(self,o_id,o_size)
"""
from abc import ABC,abstractmethod
class BasePolicy(ABC):
    @abstractmethod
    def request(self,o_id,o_size)->bool: #回傳bool 是回傳是否hit 
        pass
