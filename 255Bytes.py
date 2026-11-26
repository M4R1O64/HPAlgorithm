n,a,*o=open(0);a=[*map(int,a.split()),n:=int(n)+1,0]
while m:=[(len({x*~x for x in b}),j+1,k,*o,b)for k in range(n)for j in range(k)if 1in(a[j]+a[k],(b:=a[:j]+[-y for y in a[j:k][::-1]]+a[k:])[j]-b[j-1],a[j]+b[j]|min(a))]:_,*o,a=min(m)
print(len(o)//2,*o)
