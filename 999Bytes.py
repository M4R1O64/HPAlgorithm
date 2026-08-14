import sys
def rev(a,l,r):
 b=a[:];b[l:r+1]=[-x for x in b[l:r+1][::-1]];return b
def sc(a,n):
 p={v:i for i,v in enumerate(a)};s=0
 for v in p:
  i=p[v]
  if v<=n and -(v+1) in p:
   j=p[-(v+1)]
   if i>j:i,j=j,i
   s+=i+1<=j
  if v>=2 and -(v-1) in p:
   j=p[-(v-1)]
   if i>j:i,j=j,i
   s+=i<=j-1
 return s
n=int(input())
a=[0]+list(map(int,input().split()))+[n+1]
t=list(range(n+2))
ans=[];vis={tuple(a)}
while a!=t:
 p={v:i for i,v in enumerate(a)};cand=set()
 for v in range(n+2):
  for d in-1,1:
   if d==1 and v>n or d<0 and v<2:continue
   if v in p and -(v+d) in p:
    i,j=p[v],p[-(v+d)]
    if i>j:i,j=j,i
    if i+(d==1)<=j-(d==-1):
     cand.add((i+(d==1),j-(d==-1)))
 if not cand:
  for l in range(1,n+1):
   for r in range(l,n+1):cand.add((l,r))
 best=None;bs=-1
 for l,r in cand:
  b=rev(a,l,r);tb=tuple(b)
  if tb in vis:continue
  v=sc(b,n)
  if v>bs:bs=v;best=l,r
 if not best:break
 a=rev(a,*best);vis.add(tuple(a));ans.append(best)
print(len(ans))
for x in ans[::-1]:print(*x)
