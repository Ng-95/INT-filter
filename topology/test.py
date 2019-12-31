import redis

def database_init(r,r2,nodes_list=[2,2,2,2,2],time_out=5000):
    r2.flushall()
    
    spine_num = nodes_list[0]
    set_num = nodes_list[1]
    leaf_num = nodes_list[1]
    tor_num = nodes_list[2]
    h_num = nodes_list[3]
    pod_num = nodes_list[4]
    
    d={}
    t=0
    keys=[]
    for i in range(set_num*spine_num):
        d[str(t)]=set_num
        t+=1
    
    for i in range(set_num*leaf_num):
        d[str(t)]=set_num+tor_num
        t+=1
    
    for i in range(set_num*leaf_num):
        d[str(t)]=leaf_num+pod_num
        t+=1

    for k,v in d.items():
        for i in range(v):
            keys.append(k+'-'+str(i+1))
    
    for key in keys:
        r2.lpush(key,0,0)
        r.lpush(key,0,0)
        r.pexpire(key,time_out)
    
    
        
if __name__=='__main__':
    r = redis.Redis(unix_socket_path='/var/run/redis/redis.sock')
    r2 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock',db=1)
    database_init(r,r2)