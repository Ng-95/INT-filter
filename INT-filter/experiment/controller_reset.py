import redis
import random
import time 
from device import switch

# LINDEX id
# LRANGE
node_list = [30, 30, 30, 30, 60]
spine_num = node_list[0]
leaf_num = node_list[1]
tor_num = node_list[2]
set_num = node_list[3]
pod_num = node_list[4]

p0 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock', db=0).pipeline()
p1 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock', db=1).pipeline()
p2 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock', db=2).pipeline()
p3 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock', db=3).pipeline()

t1=time.time()

sw_id = 1

# Reset spine switch
for i in xrange(set_num*spine_num):
    for j in xrange(pod_num):
        p0.lset(sw_id,(j+1)*3,random.randint(0,99))
    sw_id+=1    

# Reset leaf switch
for i in xrange(pod_num*leaf_num):
    for j in xrange(spine_num):
        p1.lset(sw_id,(j+1)*3,random.randint(0,99))
    for k in xrange(tor_num):
        p2.lset(sw_id,(k+1)*3,random.randint(0,99))
    sw_id+=1

# Set tor switch
for i in xrange(pod_num*tor_num):
    for j in xrange(leaf_num):
        p3.lset(sw_id,(j+1)*3,random.randint(0,99))
    sw_id+=1


p0.execute()
p1.execute()
p2.execute()
p3.execute()

t2=time.time()

print(t2-t1)



