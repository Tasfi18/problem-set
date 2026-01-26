import sys
import math
c_no=1
inp_d=iter(sys.stdin.read().split())
try:
    while True:
        N,R=int(next(inp_d)),int(next(inp_d))
        if N==0 and R==0:break
        dist=[[0]*(N+1)for _ in range(N+1)]
        for _ in range(R):
            u,v,p=int(next(inp_d)),int(next(inp_d)),int(next(inp_d))
            dist[u][v]=max(dist[u][v],p)
            dist[v][u]=max(dist[v][u],p)
        S,D,T=int(next(inp_d)),int(next(inp_d)),int(next(inp_d))
        for k in range(1,N+1):
            for i in range(1,N+1):
                for j in range(1,N+1):
                    if dist[i][k]>0 and dist[k][j]>0:
                        dist[i][j]=max(dist[i][j],min(dist[i][k],dist[k][j]))
        print(f"Scenario #{c_no}")
        trips=math.ceil(T/(dist[S][D]-1))if dist[S][D]>0 else 0
        print(f"Minimum Number of Trips = {trips}")
        print()
        c_no+=1
except:
    pass