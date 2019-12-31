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

r0 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock', db=0)
p0 = r0.pipeline()
p1 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock', db=1).pipeline()
p2 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock', db=2).pipeline()
p3 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock', db=3).pipeline()

r0.flushall()

t1=time.time()

sw_id = 1

# Set spine switch
spine_id = 1
for i in xrange(set_num):
    port_list = [k*spine_num+set_num*spine_num+1 for k in xrange(pod_num)]
    for j in xrange(spine_num):
        sw_name = "s%d" % (spine_id)
        p0.rpush(sw_id, sw_name)
        for n in xrange(pod_num):
            p0.rpush(sw_id, "port%d" %
                     (n+1), port_list[n], 0)
        sw_id += 1
        spine_id += 1

# Set leaf switch
leaf_id = 1
for i in xrange(pod_num):
    port_list_down = [k+set_num*spine_num+leaf_num*pod_num+i*tor_num+1 for k in xrange(tor_num)]
    for j in xrange(leaf_num):
        port_list_up=[n+j*spine_num+1 for n in xrange(spine_num)]
        sw_name="l%d" % (leaf_id)
        
        p1.rpush(sw_id, sw_name)
        for n in xrange(spine_num):
            p1.rpush(sw_id, "port%d" %
                     (n+1), port_list_up[n], 0)

        p2.rpush(sw_id, sw_name)
        for n in xrange(tor_num):
            p2.rpush(sw_id, "port%d" %
                     (spine_num+n+1), port_list_down[n], 0)
        
        sw_id += 1
        spine_id += 1

# Set tor switch
tor_id=1
for i in xrange(pod_num):
    port_list=[spine_num*set_num+i*leaf_num+k+1 for k in xrange(leaf_num)]
    for j in xrange(tor_num):
        sw_name="t%d" % (tor_id)
        p3.rpush(sw_id,sw_name)
        for n in xrange(leaf_num):
            p3.rpush(sw_id,"port%d"%(n+1),port_list[n],0)

        sw_id += 1
        spine_id += 1

p0.execute()
p1.execute()
p2.execute()
p3.execute()


t2=time.time()

print(t2-t1)

