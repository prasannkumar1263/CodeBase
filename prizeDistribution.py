from math import log10,floor,ceil
def prettyPrint(List1,List2):
    rankStart,rankEnd=0,0
    for i in range(len(List1)):
        rankStart,rankEnd=rankEnd+1,rankEnd+List1[i]
        if rankStart==rankEnd:
            print("{}".format(rankStart),List2[i],sep="    ")
        else:
            print("{}-{}".format(rankStart,rankEnd),List2[i],sep="    ")

def roundToNice(number):
    expCount=0
    while((number>1000 or number%10==0) and number!=0):
        number//=10
        expCount+=1
    if number>=10 and number<100:
        number=(number//5)*5
    elif number>=100 and number<250:
        number=(number//25)*25
    elif number>=250 and number<1000:
        number=(number//125)*125
    number=number*(10**expCount)
    return number

def powSum(N,m,entryFee,excess,bucketSizeList):
    Sum=0
    index=0
    count=bucketSizeList[0]
    bucketedPrizeList=[entryFee*i for i in bucketSizeList]

    for i in range(1,N+1):
        value=i**(-1*m)
        Sum+=value
        bucketedPrizeList[index]+=excess*value
        count-=1
        if count==0:
            bucketedPrizeList[index]/=bucketSizeList[index]
            index+=1
            try:
                count=bucketSizeList[index]
            except:
                break
    return Sum,bucketedPrizeList

def calculatePrizes(potSize,entryFee,N,P1,bucketSizeList):
    low,high=0,8
    excess=P1-entryFee
    distributionRatio=(potSize-N*entryFee)/excess
    while(low<=high):
        mid=(high+low)/2
        value,List=powSum(N,mid,entryFee,excess,bucketSizeList)
        if value<0.9999*distributionRatio:
            high=mid
        elif value>1.0001*distributionRatio:
            low=mid
        else:
            break
    return List


def calculateBucketSizes(N,r_max):
    single_buckets=min(ceil(log10(N))+1,3)
    bucketSizes=[1 for i in range(single_buckets)]
    bucketSizes.extend([0 for i in range(r_max-single_buckets)])
    low,high=1,100
    r_max-=single_buckets
    N-=single_buckets
    if r_max!=0:
        while(low<=high):
            mid=(high+low)/2
            value=mid*(mid**r_max-1)/(mid-1)
            if value<0.99*N:
                low=mid
            elif value>1.01*N:
                high=mid
            else:
                break
        r_max+=single_buckets
        N+=single_buckets
        for i in range(single_buckets,r_max):
            elementSum=sum(bucketSizes)
            if ceil(mid*bucketSizes[i-1])+elementSum<=N:
                if ceil((mid**2)*bucketSizes[i-1])+ceil(mid*bucketSizes[i-1])+elementSum>N:
                    bucketSizes[i]=floor((N-elementSum)/2)
                    bucketSizes[i+1]=ceil((N-elementSum)/2)
                    break
            bucketSizes[i]=ceil(mid*bucketSizes[i-1])
        while(bucketSizes[-1]==0):
            bucketSizes.pop(-1)
        bucketSizes[-1]=0
        for i in range(len(bucketSizes)-1):
            bucketSizes[i]=roundToNice(bucketSizes[i])
        bucketSizes[-1]=N-sum(bucketSizes)
        return bucketSizes

def nicefy(potSize,bucketSizeList,bucketPrizeList):
    excess=0
    for i in range(len(bucketSizeList)):
        niceNo=roundToNice(int(bucketPrizeList[i]))
        bucketPrizeList[i]=niceNo
        excess+=bucketPrizeList[i]*bucketSizeList[i]
    excess=potSize-excess
    return excess,bucketPrizeList

def allocateExcessFunds(potSize,excess,bucketSizeList,bucketPrizeList):
    n=len(bucketSizeList)
    print(excess)
    for i in range(n-1):
        if bucketPrizeList[i]==bucketPrizeList[i+1]:
            incrementer=((bucketPrizeList[i+1]+bucketPrizeList[i-1])/2-bucketPrizeList[i])*bucketSizeList[i]
            if incrementer<=excess:
                bucketPrizeList[i]=(bucketPrizeList[i+1]+bucketPrizeList[i-1])/2
                excess-=incrementer
    if excess>=0:
        index=0
        for i in range(n):
            if bucketSizeList[i]!=1:
                index=i
                break
        print(excess)
        bucketPrizeList[index-1]+=excess
        if bucketPrizeList[index-1]%10==0:
            bucketPrizeList[index-1]=int(bucketPrizeList[index-1])
        for i in range(index-1,0,-1):
            if bucketPrizeList[i]>bucketPrizeList[i-1]:
                bucketPrizeList[i],bucketPrizeList[i-1]=bucketPrizeList[i-1],bucketPrizeList[i]
            print(bucketPrizeList)
    return bucketPrizeList

def heuristicSolution(potSize,entryFee,P1,N,r_max):
    bucketSizeList=calculateBucketSizes(N,r_max)
    bucketPrizeList=calculatePrizes(potSize,entryFee,N,P1,bucketSizeList)
    excess,bucketPrizeList=nicefy(potSize,bucketSizeList,bucketPrizeList)
    bucketPrizeList=allocateExcessFunds(potSize,excess,bucketSizeList,bucketPrizeList)
    prettyPrint(bucketSizeList,bucketPrizeList)
