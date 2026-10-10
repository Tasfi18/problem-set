import sys
it=iter(sys.stdin.read().split())
try:
    for i in range(1,int(next(it))+1):
        W=next(it)
        n=len(W)
        dp=[[0]*n for _ in range(n)]
        for x in range(n):
            dp[x][x]=1
        for l in range(2,n+1):
            for s in range(n-l+1):
                e=s+l-1
                if W[s]==W[e]:
                    dp[s][e]=dp[s+1][e]+dp[s][e-1]+1
                else:
                    dp[s][e]=dp[s+1][e]+dp[s][e-1]-dp[s+1][e-1]
        print(f"Case {i}: {dp[0][n-1]}")
except StopIteration:pass  # end of input