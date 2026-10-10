import sys
import heapq
class Node:
    def __init__(self,v,t,i):
        self.v,self.t,self.i=v,t,i
        self.p=self.n=None
        self.r=False
sys.setrecursionlimit(10000)
it=iter(sys.stdin.read().split())
uid=0
try:
    for _ in range(int(next(it))):
        N=int(next(it))
        S=next(it)
        if N==0:
            print(0)
            continue
        runs=[]
        c,cnt=S[0],1
        for k in range(1,N):
            if S[k]==c:cnt+=1
            else:runs.append({'c':c,'v':cnt});c=S[k];cnt=1
        runs.append({'c':c,'v':cnt})
        nodes=[Node(r['v'],r['c'],i)for i,r in enumerate(runs)]
        pq=[(r['v'],i,nodes[i])for i,r in enumerate(runs)]
        heapq.heapify(pq)
        for i in range(len(nodes)):
            if i>0:nodes[i].p=nodes[i-1]
            if i<len(nodes)-1:nodes[i].n=nodes[i+1]
        ops=lazy=0
        while pq:
            val,_,node=heapq.heappop(pq)
            # skip removed runs and stale entries left behind when a run grew by merging
            if node.r or val!=node.v:continue
            h=max(0,val-lazy)
            ops+=h
            lazy+=h
            node.r=True
            pn,nn=node.p,node.n
            if pn and nn:
                if pn.t==nn.t:
                    pn.v=pn.v+nn.v-lazy
                    pn.n=nn.n
                    if nn.n:nn.n.p=pn
                    nn.r=True
                    uid+=1
                    heapq.heappush(pq,(pn.v,uid,pn))
                else:pn.n=nn;nn.p=pn
            elif pn:pn.n=None
            elif nn:nn.p=None
        print(ops)
except StopIteration:pass  # end of input