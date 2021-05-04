"""
生成用于RedisBloomDupeFilter的哈希函数
"""
class HashMap():
    def __init__(self, m, seed):
        self.m = m
        self.seed = seed

    def hash(self, value):
        """
        计算输入字符串的哈希值
        """
        ret = 0
        for i in range(len(value)):
            ret += self.seed*ret+ord(value[i])
        return (self.m-1) & ret
