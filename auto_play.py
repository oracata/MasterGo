# python 3.6.1
# coding: GBK

import copy
import random
import os
import msvcrt

# the board class, used to put everything
import time


class board:

    __points =[]
    block=[]     #吃子时判断块是否有气 记录的快


    def __init__(self):
        self.__points.clear()
        for i in range(22):
            line = []
            if i == 0 or i == 21:
                for j in range(22):
                    line.append('#')
            else:
                line.append('#')
                for j in range(20):
                    line.append(' ')
                line.append('#')
            self.__points.append(line)

    def getPoint(self, location):
        return self.__points[location[0]][location[1]]

    def clear(self):
        self.__points.clear()
        for i in range(21):
            line = []
            if i == 0 or i == 20:
                for j in range(21):
                    if j==0  :
                        line.append('# ')  #开头
                    elif j==20:
                        line.append('#')  #结尾
                    else:
                        #line.append('#  ')  # 横线框加2个空格
                        if j<10 :
                          line.append(str(j-1)+'  ')  # 横线框加2个空格
                        elif j == 19:
                              line.append('18 ')  #结尾
                        else:
                            line.append(str(j-1) + ' ')  # 横线框加2个空格

            else:
                line.append('#')
                for j in range(19):
                    if j==3 and i==4:
                        line.append(' 。')  # 盘中的角星位
                    elif j==3 and i==16:
                        line.append(' 。')  # 盘中的角星位
                    elif j==15 and i==4:
                        line.append(' 。')  # 盘中的角星位
                    elif j==15 and i==16:
                        line.append(' 。')  # 盘中的角星位

                    elif j == 9 and i == 4:
                        line.append(' 。')  # 盘中的边星位
                    elif j==3 and i==10:
                        line.append(' 。')  # 盘中的边星位
                    elif j==15 and i==10:
                        line.append(' 。')  # 盘中的边星位
                    elif j==9 and i==16:
                        line.append(' 。')  # 盘中的边星位

                    elif j==9 and i==10:
                        line.append(' 。')  # 盘中的天元星位
                    else:
                        line.append(' + ')  #盘中线加2个空格
                line.append(str(i-1))
            self.__points.append(line)
    '''
    def put_snake(self, snake_locations):
        # clear the board
        self.clear()

        # put the snake points
        for x in snake_locations:
            #self.__points[x[0]][x[1]] = 'o'  #尾巴
            self.__points[x[0]][x[1]] = ' + '  # 尾巴

        # the head
        x = snake_locations[len(snake_locations) - 1]
        self.__points[x[0]][x[1]] = ' O '
      '''
    def put_stone(self, stone):
        i=0
        for  stone_location in  stone:
           if  (i % 2) == 0 :
             self.__points[stone_location[0]+1][stone_location[1]+1] =  '\033[1;34m' + ' @ ' + '\033[0m'
           else :
             self.__points[stone_location[0]+1][stone_location[1]+1] ='\033[1;31m' + ' 0 ' + '\033[0m'
           i=i+1

    def show(self):
        os.system("cls")

        for i in range(21):
            for j in range(21):
                print(self.__points[i][j], end='')
            print()

        # 判断棋子（种类为yourChessman，位置为yourPosition）是否无气（死亡），有气则返回False，无气则返回无气棋子的列表
        # 本函数是游戏规则的关键，初始deadlist只包含了自己的位置，每次执行时，函数尝试寻找yourPosition周围有没有空的位置，有则结束，返回False代表有气；
        # 若找不到，则找自己四周的同类（不在deadlist中的）是否有气，即调用本函数，无气，则把该同类加入到deadlist，然后找下一个邻居，只要有一个有气，返回False代表有气；
        # 若四周没有一个有气的同类，返回deadlist,至此结束递归
        # def if_dead(self,deadlist,yourChessman,yourPosition):

    def if_dead(self, deadList, yourChessman, yourPosition):

        if yourChessman==1 :
            your='\033[1;31m' + ' 0 ' + '\033[0m'
        else:
            your='\033[1;34m' + ' @ ' + '\033[0m'


        for i in [-1, 1]:
            if [yourPosition[0] + i, yourPosition[1]] not in deadList:
                if self.__points[yourPosition[0] + i+1][yourPosition[1]+1] == ' + ':
                    return False
            if [yourPosition[0], yourPosition[1] + i] not in deadList:
                if self.__points[yourPosition[0]+1][yourPosition[1] + i+1]== ' + ':
                    return False
        if ([yourPosition[1],yourPosition[0] + 1] not in deadList) and (
                self.__points[yourPosition[0] + 1+1][yourPosition[1]+1] == your):
            midvar = self.if_dead(deadList + [[yourPosition[1],yourPosition[0] + 1]], your,
                                  [yourPosition[1],yourPosition[0] + 1 ])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        if ([yourPosition[1],yourPosition[0] - 1 ] not in deadList) and (
                self.__points[yourPosition[0] - 1+1][yourPosition[1]+1] == your):
            midvar = self.if_dead(deadList + [[ yourPosition[1],yourPosition[0] - 1]], your,
                                  [ yourPosition[1],yourPosition[0] - 1])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        if ([ yourPosition[1] + 1,yourPosition[0]] not in deadList) and (
                self.__points[yourPosition[0]+1][yourPosition[1] + 1+1] == your):
            midvar = self.if_dead(deadList + [[yourPosition[1] + 1,yourPosition[0]]], your,
                                  [yourPosition[1] + 1,yourPosition[0]])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        if ([yourPosition[1] - 1,yourPosition[0] ] not in deadList) and (
                self.__points[yourPosition[0]+1][yourPosition[1] - 1+1] == your):
            midvar = self.if_dead(deadList + [[yourPosition[1] - 1,yourPosition[0]]], your,
                                  [yourPosition[1] - 1,yourPosition[0]])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        return deadList


    def kill_stone(self,next_moves):
        #找到周围对方棋子坐标，
        for i in range(2):
            for j in range(2):

                 if next_moves[0]+i==next_moves[0] and  next_moves[1]+j==next_moves[1]:
                     y=next_moves[0]
                     x=next_moves[1]-1
                 if next_moves[0]+i==next_moves[0] and  next_moves[1]+j>next_moves[1] :
                     y = next_moves[0]
                     x = next_moves[1]+1


                 if next_moves[0]+i>next_moves[0] and  next_moves[1]+j==next_moves[1]:
                     y=next_moves[0]-1
                     x=next_moves[1]
                 if next_moves[0] + i > next_moves[0] and next_moves[1] + j > next_moves[1]:
                     y = next_moves[0]+1
                     x = next_moves[1]


                 if x>=0 and  x <=18 and   y >=0 and  y<=18   :  #如果坐标没有在盘外
                     if  (self.__points[y+1][x+1]=='\033[1;34m' + ' @ ' + '\033[0m'  and  self.__points[next_moves[0]+1][next_moves[1]+1]=='\033[1;31m' + ' 0 ' + '\033[0m') or  (self.__points[y+1][x+1]=='\033[1;31m' + ' 0 ' + '\033[0m'  and  self.__points[next_moves[0]+1][next_moves[1]+1]== '\033[1;34m' + ' @ ' + '\033[0m'):    #如果是对方的子
                         self.block=[]
                         killList = self.if_dead([[y, x]], (2 if self.__points[y+1][x+1]=='\033[1;34m' + ' @ ' + '\033[0m' else 1), [y, x])  #1是白棋 2是黑棋
                         if not killList == False:
                             self.block += copy.deepcopy(killList)

                         if len(self.block) > 0:
                                 for i in range(len(self.block)):
                                     self.__points[self.block[i][0]+1][self.block[i][1]+1] =' + '
                                 time.sleep(30)

        #遍历是否有气
        #如果没有气则置此片棋子为空+





# the game
class game:

    board = board()
    #snake = snake()
    stone = []
    count = 0


    def __init__(self):

        #self.new_stone()
        self.board.clear()
        #self.board.put_snake(self.snake.getPoints())
        #self.board.put_stone(next_move)


    '''
    def new_stone(self):
        while 1:
            line = random.randint(1, 20)
            column = random.randint(1, 20)
            if self.board.getPoint([column, line]) == ' ':
                self.stone = [column, line]
                return
    '''


    def show(self,next_moves):
        #print("坐标：")
        #print(next_moves)
        self.board.clear()
        #self.board.put_snake(self.snake.getPoints())
        self.board.put_stone(next_moves)
        self.board.show()

    def kill(self,next_moves):
        self.board.kill_stone(next_moves)




    def run(self,file,file_name):

        self.board.show()

        ## the 'w a s d' are the directions
        ##operation_dict = {b'w': 'up', b'W': 'up', b's': 'down', b'S': 'down', b'a': 'left', b'A': 'left', b'd': 'right', b'D': 'right'}
        #op = msvcrt.getch()     #等待键盘输入

        ##while op != b'q':


        for i, position_w_context in enumerate(file):

                if  position_w_context.next_move is not None :
                  move= position_w_context.next_move
                  self.stone.append( move)

                  self.show(self.stone)
                  print("正在处理棋谱文件：%s:%s"%(file_name,move))
                  self.kill(move)

                else:
                  self.stone.clear()


                time.sleep(1)
                #op = msvcrt.getch()





