import sys
it=iter(sys.stdin.read().split())
try:
    for _ in range(int(next(it))):
        N,M=int(next(it)),int(next(it))
        req=[int(next(it))for _ in range(M)]
        # nxt[i]: the next position after i where req[i] is needed again.
        # (Copying a dictionary for every position used O(M x distinct) time and memory.)
        INF=float('inf')
        nxt,last=[INF]*M,{}
        for i in range(M-1,-1,-1):
            nxt[i]=last.get(req[i],INF)
            last[req[i]]=i
        desk,prep={},0  # item on the desk -> when it is needed next
        for i in range(M):
            v=req[i]
            if v in desk:
                desk[v]=nxt[i]
                continue
            prep+=1
            if N<=0:continue
            if len(desk)>=N:
                # evict the item needed furthest in the future (Belady's rule)
                del desk[max(desk,key=desk.get)]
            desk[v]=nxt[i]
        print(prep)
except StopIteration:pass  # end of input