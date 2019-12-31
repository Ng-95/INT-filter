import redis
import random
import time 
from device import switch

# LINDEX id
# LRANGE

r = redis.Redis(unix_socket_path='/var/run/redis/redis.sock')

a=[1,2,3]
b=[2,3,4]

c=[x+y for (x,y) in zip(a,b)]
print(c)

