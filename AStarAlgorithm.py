from queue import PriorityQueue

# 判断输入状态是否有解
def judgeISValid(start:list,target:list)->bool:
    # 计算一个状态的逆序数的函数
    def countInversedNUM(state:list)->int:
        return sum([True for i in range(len(state)) if state[i]!=0 for j in range(i) if state[j]>state[i] and state[j]!=0])
    # 如果逆序数%2相等,则表示状态有解
    return (countInversedNUM(start)&1)==(countInversedNUM(target)&1)

def costMANHATUN(start:str,target:str)->float:
    # 使用曼哈顿距离计算代价函数值
    return sum([abs(start.index(str(i))//3-target.index(str(i))//3)+abs(start.index(str(i))%3-target.index(str(i))%3) for i in range(1,9)])

def costEUCLIDEAN(start:str,target:str)->float:
    return sum([(start.index(str(i))//3-target.index(str(i))//3)**2+(start.index(str(i))%3-target.index(str(i))%3)**2 for i in range(1,9)])

def costCHEBYSHEV(start:str,target:str)->float:
    return sum([max(abs(start.index(str(i))//3-target.index(str(i))//3),abs(start.index(str(i))%3-target.index(str(i))%3)) for i in range(1,9)])

# A*算法,用于使用A*算法搜索路径的函数
# 返回路径列表
def AStarAlgorithm(state:list,end:list,costFUNCTION:int=1)->list:
    # 如果输入状态无解,返回空列表,代表没有路径
    # 如果初始状态就是目标状态
    if not judgeISValid(state,end) or state==end:
        return []
    
    # 约定:
    # 使用字符串存储一个状态
    # 启发函数默认是曼哈顿距离

    CostFuntion=None
    if costFUNCTION==1:
        CostFuntion=costMANHATUN
    elif costFUNCTION==2:
        CostFuntion=costEUCLIDEAN
    elif costFUNCTION==3:
        CostFuntion=costCHEBYSHEV

    def judgePlaceValid(x:int,y:int)->bool:
        # 判断0的位置是否合法
        return 0<=x<3 and 0<=y<3

    def moveTOnextState(nowState:str,nowZeroP:int,zeroOFFSET:int)->str:
        # 根据0的移动方向,获得下一个状态
        if zeroOFFSET<0:
            nowZeroP+=zeroOFFSET
            zeroOFFSET=0-zeroOFFSET
        return nowState[:nowZeroP]+nowState[nowZeroP+zeroOFFSET]+nowState[nowZeroP+1:nowZeroP+zeroOFFSET]+nowState[nowZeroP]+nowState[nowZeroP+zeroOFFSET+1:]

    # 获取初始状态的信息
    # zeroP是初始状态的0位置
    # start,target表示起始和终止状态
    # cost表示起始状态的代价
    print(state)
    zeroS=state.index(0)
    start=''.join([str(i) for i in state])
    target=''.join([str(i) for i in end])
    cost=CostFuntion(start,target)+0
    
    # 一个存储状态的优先队列
    left=PriorityQueue()
    left.put((cost,start,zeroS,0))
    
    # 使用used来记录已经用过的状态
    # 使用direct表示0可以走的四个方向,表示0的坐标的变化量
    used={start:cost}
    direct=((0,1,1),(0,-1,-1),(1,0,3),(-1,0,-3))

    searchPath=dict()

    while not left.empty():
        Fcost,Fstate,Fzero,Fdeep=left.get()

        # 如果在向left中放入Fstate后,又找到了以更短的代价从Fstate到达target的路径
        if used[Fstate]<Fcost:
            continue
        
        x=Fzero/3
        y=Fzero%3

        for di in direct:
            if not judgePlaceValid(x+di[0],y+di[1]):
                continue

            newZeroPlace=Fzero+di[2]
            newState=moveTOnextState(Fstate,Fzero,di[2])
            newCost=CostFuntion(newState,target)+Fdeep

            isUsed=used.get(newState,-1)
            if isUsed==-1 or isUsed>newCost:
                used[newState]=newCost
                searchPath[newState]=Fstate
                left.put((newCost,newState,newZeroPlace,Fdeep+1))
    
            if newState==target:
                PATH=[target]
                StateBack=Fstate
                while StateBack!=start:
                    PATH.append(StateBack)
                    StateBack=searchPath[StateBack]
                return [[int(i) for i in j] for j in PATH[::-1]]

    return []


# 一个用于测试的函数,如果外部不可以import
def test()->None:
    # 测试样例,最短路径是15
    for i in range(1,4):
        a=AStarAlgorithm([2,7,3,6,4,5,8,0,1],[1,2,3,8,0,4,7,6,5],i)
        print(len(a))
    # t=timeit('AStarAlgorithm([2,7,3,6,4,5,8,0,1],[1,2,3,8,0,4,7,6,5])','from __main__ import AStarAlgorithm',number=10)
    # print(t/10)
    return 

if __name__=='__main__':
    test()