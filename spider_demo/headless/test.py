# 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
# import redis
#
# pool = redis.ConnectionPool(host='140.143.22.203', port=6379, decode_responses=True, password="redis_foobared", db=0)
# r = redis.Redis(connection_pool=pool)
# # r = redis.Redis(host='140.143.22.203', port=6379, db=0, password="redis_foobared")
# print(r.lrange("ownedcore_home", 1, 1))  # gender 取出键male对应的值
#
# v=r.lrange("ownedcore_home", 1, 1)
# for item in v[0].split("\u0001"):
#     print(item)
import uuid
print(str(uuid.uuid3(uuid.NAMESPACE_DNS,"test")))