import random
from time import sleep
from tkinter import *
import tkinter.messagebox
from tkinter.simpledialog import *
import time
from AStarAlgorithm import AStarAlgorithm
from GeneticAlgorithm import GeneticAlgorithm
from BreadthAlgorithm import BreadthAlgorithm

class show:
    # 页面的初始化算法
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title('A*算法解决8数码问题')
        self.root.iconbitmap('.\\images\\favicon.ico')
        self.root.geometry('800x600')  # 这里的乘号不是 * ，而是小写英文字母 x
        self.lableList = []  # 储存九个方格的lable的列表
        self.textList = []  # 储存数字的信息
        self.cangoback = False
        self.step = 1  # 当前所在的步数
        self.stepLable = Label(self.root, text='第' + str(self.step) +
                               '步', bg='pink', width=20, height=8, font=('宋体', 15),)
        self.btn_goback = Button(
            self.root, text='上一步', command=self.goback, bg='gray')
        self.btn_gonext = Button(
            self.root, text='下一步', command=self.gonext, bg='gray')
        self.updateCangoback()
        self.btn_changeAlgorithm = Button(self.root, text='A*算法',
                                          command=self.changeAlgorithm, bg='skyblue')
        self.btn_changeAlgorithm.place(x=20, y=20, height=30, width=100)
        self.algorithmType = 0  # 算法类型：0：A*算法；1：广度优先算法；2：遗传算法

        self.btn_changeCostFunction = Button(self.root, text='曼哈顿距离',
                                             command=self.changeCostFunction, bg='skyblue')
        self.btn_changeCostFunction.place(x=20, y=60, height=30, width=100)
        self.costFunctionType = 1  # 启发函数类型：1：曼哈顿距离；2：欧式距离；3：切比雪夫距离

        self.btn_setTarget = Button(self.root, text='设置最终状态',
                                    command=self.setTarget, bg='skyblue')
        self.btn_setTarget.place(x=660, y=20, height=30, width=100)
        self.target = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # 目标状态

        # 循环生成九个方格
        for i in range(9):
            yHeight = 20
            if i >= 6:
                yHeight = 260
            elif i >= 3:
                yHeight = 140
            self.lableList.append(' ')
            self.lableList[i] = Label(
                self.root, text=' ', bg='green', width=20, height=8, relief=RAISED, font=('宋体', 18),)
            self.lableList[i].place(
                x=200+(i % 3)*150, y=yHeight, height=100, width=100)
            self.lableList[i].bind('<Button-1>', self.changeText)
            self.textList.append(0)

        btn_random = Button(self.root, text='随机生成',
                            command=self.randomCreat, bg='gray')
        btn_random.place(x=200, y=400, height=30, width=100)
        btn_run = Button(self.root, text='运行', command=self.run, bg='gray')
        btn_run.place(x=500, y=400, height=30, width=100)

        self.root.mainloop()

    # 切换算法的方法
    def changeAlgorithm(self):
        self.algorithmType = self.algorithmType + 1
        if self.algorithmType == 3:
            self.algorithmType = 0
        # 如果为遗传算法，点击切换为A*算法
        if self.algorithmType == 0:
            self.btn_changeAlgorithm.config(text='A*算法', bg='skyblue')
        elif self.algorithmType == 1:
            self.btn_changeAlgorithm.config(text='广度优先算法', bg='yellow')
        else:
            self.btn_changeAlgorithm.config(text='遗传算法', bg='pink')

    # 切换启发函数的方法
    def changeCostFunction(self):
        self.costFunctionType = self.costFunctionType + 1
        if self.costFunctionType == 4:
            self.costFunctionType = 1

        if self.costFunctionType == 1:
            self.btn_changeCostFunction.config(text='曼哈顿距离', bg='skyblue')
        elif self.costFunctionType == 2:
            self.btn_changeCostFunction.config(text='欧式距离', bg='yellow')
        else:
            self.btn_changeCostFunction.config(text='切比雪夫距离', bg='pink')

    # 设置目标状态的方法
    def setTarget(self):
        inputStr = askstring(
            '请依次输入九个方格的数字', '0代表为空，数字间用空格隔开')
        if inputStr == None:
            return
        inputList = inputStr.split()
        haveVisit = {}
        if len(inputList) != 9:
            tkinter.messagebox.showwarning('错误', '输入数量错误')
            return
        for i in range(len(inputList)):
            inputList[i] = int(inputList[i])
            if inputList[i] < 0 or inputList[i] > 8:
                tkinter.messagebox.showwarning('错误', '请输入0-8的数字')
                return
            elif inputList[i] in haveVisit.keys():
                tkinter.messagebox.showwarning('错误', '输入重复')
                return
            else:
                haveVisit[inputList[i]] = True
        self.cangoback = False
        self.updateCangoback()
        self.target = inputList
        tkinter.messagebox.showinfo('成功', '已更改目标状态')

    # 在新窗口中为方格选择数字的方法
    def changeText(self, event):
        index = -1
        for i in range(9):
            if event.widget == self.lableList[i]:
                index = i
                break
        inputNum = askinteger(
            '请输入', '请输入0-8的整数,注意:不能重复,输入0置空', minvalue=0, maxvalue=8)
        if inputNum is None:
            return

        # 若重复，则忽略输入
        for i in range(9):
            if self.textList[i] == inputNum and inputNum != 0:
                return
        # 不重复，设置值
        self.cangoback = False
        self.updateCangoback()
        if inputNum == 0:
            self.textList[index] = inputNum
            self.lableList[index].config(text=' ', bg='green')
        else:
            self.textList[index] = inputNum
            self.lableList[index].config(text=inputNum, bg='pink')

    # 随机初始化方法
    def randomCreat(self):
        self.textList = random.sample(range(0, 9), 9)
        self.cangoback = False
        self.updateCangoback()
        for i in range(9):
            if self.textList[i] == 0:
                self.lableList[i].config(text=' ', bg='green')
            else:
                self.lableList[i].config(text=self.textList[i], bg='pink')

    # 运行算法的方法
    def run(self):
        num0 = 0
        for i in range(9):
            if self.textList[i] == 0:
                num0 += 1
        if num0 > 1:
            tkinter.messagebox.showwarning('错误', '输入格式有误')
            return
        sleepTime = askfloat('请输入', '请输入变换的间隔(单位:s),最大为5s',
                             minvalue=0, maxvalue=5)
        if sleepTime is None:
            return
        # 在这里调用接口返回变换的信息
        # 若为A*
        self.showTextList = []

        if self.algorithmType == 0:
            self.showTextList = AStarAlgorithm(
                self.textList, self.target, self.costFunctionType)
        elif self.algorithmType == 1:
            self.showTextList = BreadthAlgorithm(
                self.textList, self.target)

        else:
            self.showTextList = GeneticAlgorithm(
                self.textList, self.target)
        # print(self.showTextList)
        i = 0
        # 若为空列表，说明无解
        if len(self.showTextList) == 0:
            flag = True
            for i in range(9):
                if self.target[i] != self.textList[i]:
                    flag = False
                    break
            if flag:
                tkinter.messagebox.showwarning('提示', '已是目标状态')
            else:
                tkinter.messagebox.showwarning('错误', '无解')
            self.cangoback = False
            self.updateCangoback()
            self.root.update()  # 刷新页面
            return
        while i < len(self.showTextList):
            # 延迟
            time.sleep(sleepTime)
            self.textList = self.showTextList[i]
            for k in range(9):
                if self.textList[k] == 0 or self.textList[k] == '0':
                    self.lableList[k].config(text=' ', bg='green')
                else:
                    self.lableList[k].config(text=self.textList[k], bg='pink')
            self.root.update()  # 刷新页面
            i += 1
        self.cangoback = True
        self.step = len(self.showTextList)  # 当前所在的步数
        self.updateCangoback()
        self.root.update()  # 刷新页面
        tkinter.messagebox.showinfo('成功', '运行结束')

    # 更新能否进行下一步，上一步以及步数
    def updateCangoback(self):
        if self.cangoback:
            s = '第' + str(self.step) + '步/共' + \
                str(len(self.showTextList)) + '步'
            self.stepLable.config(text=s)
            self.stepLable.place(x=320, y=400, height=30, width=160)
            self.btn_goback.place(x=100, y=500, height=30, width=100)
            self.btn_gonext.place(x=600, y=500, height=30, width=100)
        else:
            self.stepLable.place_forget()
            self.btn_goback.place_forget()
            self.btn_gonext.place_forget()

    # 返回上一步的方法
    def goback(self):
        if self.step == 1:
            tkinter.messagebox.showwarning('不能上一步', '已是第一步')
        else:
            self.step -= 1
            self.textList = self.showTextList[self.step-1]
            for k in range(9):
                if self.textList[k] == 0 or self.textList[k] == '0':
                    self.lableList[k].config(text=' ', bg='green')
                else:
                    self.lableList[k].config(text=self.textList[k], bg='pink')
            self.root.update()  # 刷新页面
            self.updateCangoback()

    # 去下一步的方法
    def gonext(self):
        if self.step == len(self.showTextList):
            tkinter.messagebox.showwarning('不能下一步', '已是最后一步')
        else:
            self.step += 1
            self.textList = self.showTextList[self.step-1]
            for k in range(9):
                if self.textList[k] == 0 or self.textList[k] == '0':
                    self.lableList[k].config(text=' ', bg='green')
                else:
                    self.lableList[k].config(text=self.textList[k], bg='pink')
            self.root.update()  # 刷新页面
            self.updateCangoback()


show()
