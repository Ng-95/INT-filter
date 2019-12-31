import random
import time
import redis

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

list1=[] # Leaf to spine
list2=[] # Spine to leaf
list3=[] # Tor to leaf
list4=[] # Leaf to tor

t1=time.time()

leaf_id=set_num*spine_num+1
for i in xrange(leaf_num):
    for j in xrange(spine_num):
        p1.lindex(leaf_id,(j+1)*3)
    leaf_id+=1
list1=map(int,p1.execute())


for i in xrange(set_num*spine_num):
    p0.lindex(i+1,6)
list2=map(int,p0.execute())

list_1_2=[x+y for (x,y) in zip(list1,list2)]

t2=time.time()

tor_id=spine_num*set_num+leaf_num*pod_num+1
for i in xrange(leaf_num):
    p3.lindex(tor_id,(i+1)*3)
list3=map(int,p3.execute())


leaf_id=spine_num*set_num+1*leaf_num+1
for i in xrange(leaf_num):
    p2.lindex(leaf_id,3)
    leaf_id+=1
list4=map(int,p2.execute())
    
list_3_4=[x+y for (x,y) in zip(list3,list4)]

t3=time.time()

print(t2-t1,t3-t2)






# Tor to tor in same pod

list5=[]
list6=[]

t4=time.time()

tor_id=spine_num*set_num+leaf_num*pod_num+1
for i in xrange(leaf_num):
    p3.lindex(tor_id,(i+1)*3)
list5=map(int,p3.execute())


leaf_id=spine_num*set_num+1
for i in xrange(leaf_num):
    p2.lindex(leaf_id,6)
    leaf_id+=1
list6=map(int,p2.execute())

list_5_6=[x+y for (x,y) in zip(list5,list6)]

t5=time.time()

print(t5-t4)


