import sys
it=iter(sys.stdin.read().split())
try:
    for _ in range(int(next(it))):
        N,M=int(next(it)),int(next(it))
        req=[int(next(it))for _ in range(M)]
        next_use=[{}for _ in range(M+1)]
        for i in range(M-1,-1,-1):
            next_use[i]=next_use[i+1].copy()
            next_use[i][req[i]]=i
        desk,prep=set(),0
        for i in range(M):
            v=req[i]
            if v in desk:continue
            prep+=1
            if len(desk)<N:
                desk.add(v)
            else:
                to_evict=max(desk,key=lambda x:next_use[i+1].get(x,float('inf')))
                desk.remove(to_evict)
                desk.add(v)
        print(prep)
except:pass