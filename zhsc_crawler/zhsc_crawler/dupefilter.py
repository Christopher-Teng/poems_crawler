import hashlib
import logging

from redis import Redis
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from .hashmap import HashMap


class RedisBloomDupeFilter(BaseDupeFilter):
    """
    基于Redis的布隆过滤器
    """

    def __init__(self, host='localhost', port=6379, db=0, bitSize=32, seeds=[5, 7, 11], blockNum=1, key='bloomfilter'):
        self.redis = Redis(host=host, port=port, db=db)  # 连接Redis
        self.bitSize = 1 << bitSize  # 在Redis中申请一个BitSet，Redis中BitSet实际上使用String进行存储，因此最大容量为512M，即2^32
        self.seeds = seeds  # 生成多个hash函数的种子
        self.key = key  # Redis中使用的键名
        self.blockNum = blockNum  # Redis中总共申请多少个BitSet
        self.hashFunc = []  # hash函数
        for seed in self.seeds:
            # 根据提供的种子生成多个hash函数
            self.hashFunc.append(HashMap(self.bitSize, seed))
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        _host = settings.get('REDIS_HOST', 'localhost')
        _port = settings.getint('REDIS_PORT', 6379)
        _db = settings.getint('REDIS_DUPE_DB', 0)
        _bitSize = settings.getint('BLOOMFILTER_BIT_SIZE', 32)
        _seeds = settings.getlist('BLOOMFILTER_HASH_SEEDS', [])
        _blockNum = settings.getint('BLOOMFILTER_BLOCK_NUMBER', 1)
        _key = settings.get('BLOOMFILTER_REDIS_KEY', 'bloomfilter')
        return cls(_host, _port, _db, _bitSize, _seeds, _blockNum, _key)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        if self.exists(fp):
            # 如果请求指纹已经存在
            return True
        self.insert(fp)  # 如果请求指纹不存在
        return False

    def insert(self, str_input):
        """
        加入请求指纹
        """
        md5 = hashlib.md5()
        md5.update(str(str_input).encode('utf-8'))
        _input = md5.hexdigest()
        _name = self.key+str(int(_input[0:2], 16) % self.blockNum)
        for func in self.hashFunc:
            """
            将hash映射后的bit为置位为1
            """
            _offset = func.hash(_input)
            self.redis.setbit(_name, _offset, 1)

    def exists(self, str_input):
        """
        判断请求指纹是否已存在
        """
        if not str_input:
            return False
        md5 = hashlib.md5()
        md5.update(str(str_input).encode('utf-8'))
        _input = md5.hexdigest()
        _name = self.key+str(int(_input[0:2], 16) % self.blockNum)
        ret = True
        for func in self.hashFunc:
            """
            如果经过hash映射之后对应的bit位上有任意一个0，则一定不存在
            """
            _offset = func.hash(_input)
            ret = ret & self.redis.getbit(_name, _offset)
        return ret

    def log(self, request, spider):
        self.logger.debug(u'已过滤的重复请求：%(request)s', {'request': request})
        spider.crawler.stats.inc_value('redisbloomfilter/filtered', spider=spider)
