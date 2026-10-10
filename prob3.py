import sys
sys.setrecursionlimit(2000)
class FenwickTree:
    def __init__(self,s):
        self.tree=[0]*(s+1)
        self.size=s
    def update(self,i,d):
        while i<=self.size:
            self.tree[i]+=d
            i+=i&(-i)
    def query(self,i):
        s=0
        while i>0:
            s+=self.tree[i]
            i-=i&(-i)
        return s
    def find_kth(self,k):
        idx,curr_sum=0,0
        # start from the highest power of two that fits (17 bits only covered sizes up to 262,143)
        for i in range(self.size.bit_length(),-1,-1):
            next_idx=idx+(1<<i)
            if next_idx<=self.size and curr_sum+self.tree[next_idx]<k:
                idx=next_idx
                curr_sum+=self.tree[idx]
        return idx+1
it=iter(sys.stdin.read().split())
try:
    for case_idx in range(1,int(next(it))+1):
        N,Q=int(next(it)),int(next(it))
        ids=[int(next(it))for _ in range(N)]
        ops=[(next(it),int(next(it)))for _ in range(Q)]
        print(f"Case {case_idx}:")
        MAX=N+Q+5
        bit=FenwickTree(MAX)
        data_map=[0]*(MAX+1)
        for i in range(N):
            bit.update(i+1,1)
            data_map[i+1]=ids[i]
        next_slot,cnt=N+1,N
        for op_type,val in ops:
            if op_type=='a':
                bit.update(next_slot,1)
                data_map[next_slot]=val
                next_slot+=1
                cnt+=1
            else:
                if val>cnt:
                    print("none")
                else:
                    idx=bit.find_kth(val)
                    print(data_map[idx])
                    bit.update(idx,-1)
                    cnt-=1
except StopIteration:pass  # end of input