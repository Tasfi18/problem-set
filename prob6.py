import sys
m={}
S=""
def gv(d):return d if d%2 else 2*d
def dp(i,t,r):
    s=(i,t,r)
    if s in m:return m[s]
    if i==len(S):return 1,r
    l=int(S[i])if t else 9
    tc,ts=0,0
    for d in range(l+1):
        nt=t and d==l
        v=gv(d)
        nr=(r+v)%10
        c,s_=dp(i+1,nt,nr)
        tc+=c
        ts+=s_
    m[s]=(tc,ts)
    return tc,ts
def calc(N):
    if N<=0:return 0
    global S,m
    S=str(N)
    m={}
    return dp(0,True,0)[1]
it=iter(sys.stdin.read().split())
try:
    for _ in range(int(next(it))):
        A,B=int(next(it)),int(next(it))
        print(calc(B)-calc(A-1))
except:pass