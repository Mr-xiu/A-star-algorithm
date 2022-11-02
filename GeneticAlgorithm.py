from bisect import bisect_left
from random import randint, random

# 判断输入状态是否有解


def judgeISValid(start: list, target: list) -> bool:
    # 计算一个状态的逆序数的函数
    def countInversedNUM(state: list) -> int:
        return sum([True for i in range(len(state)) if state[i] != 0 for j in range(i) if state[j] > state[i] and state[j] != 0])
    # 如果逆序数%2相等,则表示状态有解
    return (countInversedNUM(start) & 1) == (countInversedNUM(target) & 1)


class Creatures:

    def __init__(self, start: list, target: list, Genelength: int = 140, GeneSize: int = 40, loop: int = 1000) -> None:
        self.start, self.target = ''.join([str(i) for i in start]), ''.join(
            [str(i) for i in target])  # 设置初始状态和终止状态
        self.GeneCnt = GeneSize  # 设置种群的大小,种群中个体的个数
        self.GeneLength = Genelength  # 设置基因的长度
        self.EvolutionLoop = loop  # 设置种群进化的次数
        self.EnvironmentalFitness = lambda state: int(sum(
            [100-10*int(state[i]) for i in range(len(state)) if self.target[i] == state[i]]))  # 定义计算个体环境适应度的函数
        self.EndTag = self.EnvironmentalFitness(
            self.target)   # 当一个个体的环境适应度达到EndTag时,说明找到了好的个体
        self.MutationProbility = 0.15  # 定义个体变异的概率
        self.CrossProbility = 0.8  # 定义两个个体基因交叉变异的概率
        self.JudgePlaceValid = lambda x, y: 0 <= x < 3 and 0 <= y < 3    # 定义判断位置是否合法的函数
        self.Dirct = ((-1, 0), (1, 0), (0, -1), (0, 1))               # 上下左右移动
        self.Genes = [''.join([str(randint(0, 3)) for gene in range(
            self.GeneLength)]) for individual in range(self.GeneCnt)]  # 初始化每个个体的基因
        self.Fitness = [0 for i in range(self.GeneCnt)]        # 记录每一个个体的环境适应度
        self.PreFitness = [0 for i in range(self.GeneCnt)]     # 对环境适应度求前缀和
        self.Move = lambda state, TowPlace: state[:TowPlace[0]]+state[TowPlace[1]] + \
            state[TowPlace[0]+1:TowPlace[1]]+state[TowPlace[0]] + \
            state[TowPlace[1]+1:]  # 获得一次移动后的状态的函数
        self.RandSeed = (2147456, 9857498)
        return

    def inherit(self, FitSum: int) -> None:
        # 模拟种群的更新换代,将环境适应度高的个体更大程度的遗传下去
        LastPopulation = self.Genes[:]
        for GenePlace in range(self.GeneCnt):
            RandomNUM = randint(1, FitSum)
            InheritFrom = bisect_left(self.PreFitness, RandomNUM)
            self.Genes[GenePlace] = LastPopulation[InheritFrom]
        return

    def mutations(self) -> None:
        # 模拟种群中个体的变异
        for GenePlace in range(self.GeneCnt):
            RandomProbility = random()
            if RandomProbility < self.MutationProbility:
                # 如果随机结果是发生变异
                # 随机出要发生多少基因位的变异
                GrainNUM = randint(1, self.GeneLength)
                gene = self.Genes[GenePlace]
                for i in range(GrainNUM):
                    # 随机出哪一位基因发生变异
                    GrainPlace = randint(0, self.GeneLength-1)
                    gene = gene[:GrainPlace]+str(
                        int((randint(self.RandSeed[0], self.RandSeed[1])) % 4))+gene[GrainPlace+1:]
                self.Genes[GenePlace] = gene
        return

    def crossMutaion(self) -> None:
        # 模拟种群中基因的交叉变异
        for i in range(self.GeneCnt):
            RandomProbility1 = random()
            RandomProbility2 = random()
            if RandomProbility1 < self.CrossProbility and RandomProbility2 < self.CrossProbility:
                Gene1 = randint(0, self.GeneCnt-1)
                Gene2 = randint(0, self.GeneCnt-1)
                gene1 = self.Genes[Gene1]
                gene2 = self.Genes[Gene2]
                GrainNUM = randint(1, self.GeneLength)
                for i in range(GrainNUM):
                    GrainPlace = randint(0, self.GeneLength-1)
                    a = gene1[:GrainPlace] + \
                        gene2[GrainPlace]+gene1[GrainPlace+1:]
                    b = gene2[:GrainPlace] + \
                        gene1[GrainPlace]+gene2[GrainPlace+1:]
                    gene1 = a
                    gene2 = b
                self.Genes[Gene1] = gene1
                self.Genes[Gene2] = gene2
        return

    def SumEnvironmentalFitness(self) -> int:
        SUM = 0  # 返回的SUM便于进行种群的优胜劣汰的遗传
        for GenePlace in range(self.GeneCnt):
            gene = self.Genes[GenePlace]
            start = self.start
            ZeroPlace = start.index('0')
            ZeroX, ZeroY = int(ZeroPlace//3), int(ZeroPlace % 3)
            for GrainPlace in range(self.GeneLength):
                dirct = self.Dirct[int(gene[GrainPlace])]
                NewX, NewY = int(ZeroX+dirct[0]), int(ZeroY+dirct[1])
                if self.JudgePlaceValid(NewX, NewY):
                    NewZeroPlace = int(NewX*3+NewY)
                    start = self.Move(start, sorted([NewZeroPlace, ZeroPlace]))
                    ZeroPlace, ZeroX, ZeroY = NewZeroPlace, NewX, NewY
                self.Fitness[GenePlace] = self.EnvironmentalFitness(start)
                if self.Fitness[GenePlace] == self.EndTag:
                    self.HaveFindPath = True  # 获得Path
                    self.BestGene = gene[:GrainPlace+1]  # 获得Path
                    return SUM
            if self.Fitness[GenePlace] == 0:
                self.Fitness[GenePlace] = 1
            # 求出前缀和
            self.PreFitness[GenePlace] = self.Fitness[GenePlace] + \
                (self.PreFitness[GenePlace-1] if GenePlace > 0 else 0)
            SUM += self.Fitness[GenePlace]
        return SUM

    def searchPath(self) -> list:
        self.HaveFindPath = False
        for loop in range(self.EvolutionLoop):
            FitSum = self.SumEnvironmentalFitness()
            if self.HaveFindPath:
                # 如果找到路径
                Dir = self.BestGene
                start = self.start
                Path = [[int(i) for i in start]]
                ZeroPlace = Path[-1].index(0)
                ZeroX = int(ZeroPlace//3)
                ZeroY = int(ZeroPlace % 3)
                for di in Dir:
                    d = self.Dirct[int(di)]
                    if self.JudgePlaceValid(ZeroX+d[0], ZeroY+d[1]):
                        NewZeroPlace = int((ZeroX+d[0])*3+ZeroY+d[1])
                        start = self.Move(start, sorted(
                            [NewZeroPlace, ZeroPlace]))
                        Path.append([int(i) for i in start])
                        ZeroPlace = NewZeroPlace
                        ZeroX += d[0]
                        ZeroY += d[1]
                    if start == self.target:
                        return Path
            self.inherit(FitSum)
            self.crossMutaion()
            self.mutations()
        # 如果进化完毕,仍未找到路径,则无解
        return []


def GeneticAlgorithm(start: list, target: list) -> list:
    # 如果无解或者其实状态和终止状态相同,则返回空列表
    if not judgeISValid(start, target) or start == target:
        return []

    solution = Creatures(start, target)
    return solution.searchPath()


def main() -> None:
    Path = GeneticAlgorithm([2, 7, 3, 6, 4, 5, 8, 0, 1], [
                            1, 2, 3, 8, 0, 4, 7, 6, 5])
    print(Path)
    a = input()


if __name__ == '__main__':
    main()
