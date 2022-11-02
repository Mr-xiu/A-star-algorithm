# 判断输入状态是否有解
def judgeISValid(start: list, target: list) -> bool:
    # 计算一个状态的逆序数的函数
    def countInversedNUM(state: list) -> int:
        return sum([True for i in range(len(state)) if state[i] != 0 for j in range(i) if state[j] > state[i] and state[j] != 0])
    # 如果逆序数%2相等,则表示状态有解
    return (countInversedNUM(start) & 1) == (countInversedNUM(target) & 1)


def BreadthAlgorithm(st: list, ta: list) -> list:
    # 如果无解或者其实状态和终止状态相同,则返回空列表
    if not judgeISValid(st, ta) or st == ta:
        return []

    dirct = ((-1, 0), (1, 0), (0, -1), (0, 1))
    used = set()
    start = ''.join([str(i) for i in st])
    target = ''.join([str(i) for i in ta])
    left = [start]

    def moveToNEWzero(state, TowPlace): return state[:TowPlace[0]]+state[TowPlace[1]] + \
        state[TowPlace[0]+1:TowPlace[1]] + \
        state[TowPlace[0]]+state[TowPlace[1]+1:]
    searchPath = dict()
    def judgePlace(x, y): return 0 <= x < 3 and 0 <= y < 3
    while len(left) > 0:
        left2 = []
        for state in left:
            zeroPlace = state.index('0')
            zeroX = int(zeroPlace//3)
            zeroY = int(zeroPlace % 3)
            for d in dirct:
                newzerox = int(zeroX+d[0])
                newzeroy = int(zeroY+d[1])
                newzero = int(newzerox*3+newzeroy)
                if judgePlace(newzerox, newzeroy):
                    newState = moveToNEWzero(
                        state, sorted([newzero, zeroPlace]))
                    if newState not in used:
                        used.add(newState)
                        left2.append(newState)
                        searchPath[newState] = state
                    if newState == target:
                        Path = []
                        while newState != start:
                            Path.append(newState)
                            newState = searchPath[newState]
                        return [[int(j) for j in i] for i in Path[::-1]]
        left = left2
    return []


def main() -> None:
    Path = BreadthAlgorithm([2, 7, 3, 6, 4, 5, 8, 0, 1], [1, 2, 3, 8, 0, 4, 7, 6, 5])
    print(Path)


if __name__ == '__main__':
    main()
