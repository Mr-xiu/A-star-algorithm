from AStarAlgorithm import AStarAlgorithm,judgeISValid
from BreadthAlgorithm import BreadthAlgorithm
from collections import defaultdict
from timeit import timeit
from random import sample as SORDER

def FindBestCost(TAG:bool)->None:
    PATH='result.txt'
    if TAG:
        TEST=GenerateTests(500)
        target=[1,2,3,4,5,6,7,8,0]
        for test in TEST:
            RES=[len(AStarAlgorithm(test,target,cost)) for cost in range(1,4)]
            with open(PATH,'a') as file:
                file.write(str(test)+' : '+str(RES)+'\n')
    
    STATIC=defaultdict(int)
    BIG=defaultdict(list)
    M={1:'曼哈顿距离结果',2:'欧氏距离结果',3:'切比雪夫距离'}
    with open(PATH,'r') as file:
        for lines in file.readlines():
            A=sorted([(l,c) for l,c in zip(eval(lines.split(':')[1]),range(1,4))])
            S=''
            if A[0][0]<A[1][0]:
                S+=M[A[0][1]]+' < '+M[A[1][1]]
                BIG[M[A[0][1]]+' < '+M[A[1][1]]].append(A[1][0]-A[0][0])
            elif A[0][0]==A[1][0]:
                S+=M[A[0][1]]+' = '+M[A[1][1]]
            if A[1][0]<A[2][0]:
                S+=' < '+M[A[2][1]]
                BIG[M[A[1][1]]+' < '+M[A[2][1]]].append(A[2][0]-A[1][0])
            elif A[1][0]==A[2][0]:
                S+=' = '+M[A[2][1]]
            STATIC[S]+=1
    for K,V in STATIC.items():
        print(K+' : '+str(V))
    for K,V in BIG.items():
        print(K+' 多了 '+str(max(V))+' 步 .')
    return 
    

def ContrastAstarTime()->None:
    PATH='result.txt'
    with open(PATH,'r') as file:
        for lines in file.readlines():
            Test.append(eval(lines.split(':')[0]))
    MT=timeit('[AStarAlgorithm(test,[1,2,3,4,5,6,7,8,0],1) for test in Test]','from AStartAlgorithm import AStarAlgorithm; from __main__ import Test',number=1)/len(Test)
    OT=timeit('[AStarAlgorithm(test,[1,2,3,4,5,6,7,8,0],2) for test in Test]','from AStartAlgorithm import AStarAlgorithm; from __main__ import Test',number=1)/len(Test)
    CT=timeit('[AStarAlgorithm(test,[1,2,3,4,5,6,7,8,0],3) for test in Test]','from AStartAlgorithm import AStarAlgorithm; from __main__ import Test',number=1)/len(Test)
    print('曼哈顿距离耗时:  ',MT)
    print('欧式距离耗时:    ',OT)
    print('切比雪夫距离耗时:',CT)
    return 

def TheFastINastarANDbfs()->None:
    AT=timeit('[AStarAlgorithm(test,[1,2,3,4,5,6,7,8,0],2) for test in Test]','from AStartAlgorithm import AStarAlgorithm; from __main__ import Test',number=1)
    BT=timeit('[BreadthAlgorithm(test,[1,2,3,4,5,6,7,8,0]) for test in Test]','from BreadthAlgorithm import BreadthAlgorithm; from __main__ import Test',number=1)
    print('广度优先搜索运行的时间是:  '+str(BT/10))
    print('      A*算法的运行时间是:  '+str(AT/10))
    return 

def GenerateTests(num:int,target:list=[1,2,3,4,5,6,7,8,0])->list:
    Order=[0,1,2,3,4,5,6,7,8]
    Haved=0
    NORDER=[]
    while Haved<num:
        Order=SORDER(Order,len(Order))
        if judgeISValid(Order,target):
            Haved+=1
            NORDER.append(tuple(Order))
    return NORDER

Test=GenerateTests(10)

if __name__=='__main__':
    # ContrastAstarTime()
    # FindBestCost(False)
    # print('\n\n')
    # TheFastINastarANDbfs()
    pass
