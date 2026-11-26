n=int(input())
a=0,*map(int,input().split()),n+1
o=[];w={a}
while[*a]!=sorted(a)and(m:=max(((sum((~x in b)+(x>1)*(1-x in b)for x in b),-k,(l,r),b)for k,(l,r)in enumerate({(i+(d>0),j-(d<0))for v in range(n+2)for d in(-1,1)if v+d>0 and v in a and-v-d in a for i,j in[sorted((a.index(v),a.index(-v-d)))]}or{(l,r)for l in range(1,n+1)for r in range(l,n+1)})for b in[a[:l]+tuple(-y for y in a[r:l-1:-1])+a[r+1:]]if b not in w),default=0)):a=m[3];w|={a};o=['%d %d'%m[2]]+o
print(len(o),*o,sep='\n')
#######
