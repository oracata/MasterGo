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
    block=[]     #����ʱ�жϿ��Ƿ����� ��¼�Ŀ�


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
                        line.append('# ')  #��ͷ
                    elif j==20:
                        line.append('#')  #��β
                    else:
                        #line.append('#  ')  # ���߿��2���ո�
                        if j<10 :
                          line.append(str(j-1)+'  ')  # ���߿��2���ո�
                        elif j == 19:
                              line.append('18 ')  #��β
                        else:
                            line.append(str(j-1) + ' ')  # ���߿��2���ո�

            else:
                line.append('#')
                for j in range(19):
                    if j==3 and i==4:
                        line.append(' ��')  # ���еĽ���λ
                    elif j==3 and i==16:
                        line.append(' ��')  # ���еĽ���λ
                    elif j==15 and i==4:
                        line.append(' ��')  # ���еĽ���λ
                    elif j==15 and i==16:
                        line.append(' ��')  # ���еĽ���λ

                    elif j == 9 and i == 4:
                        line.append(' ��')  # ���еı���λ
                    elif j==3 and i==10:
                        line.append(' ��')  # ���еı���λ
                    elif j==15 and i==10:
                        line.append(' ��')  # ���еı���λ
                    elif j==9 and i==16:
                        line.append(' ��')  # ���еı���λ

                    elif j==9 and i==10:
                        line.append(' ��')  # ���е���Ԫ��λ
                    else:
                        line.append(' + ')  #�����߼�2���ո�
                line.append(str(i-1))
            self.__points.append(line)
    '''
    def put_snake(self, snake_locations):
        # clear the board
        self.clear()

        # put the snake points
        for x in snake_locations:
            #self.__points[x[0]][x[1]] = 'o'  #β��
            self.__points[x[0]][x[1]] = ' + '  # β��

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

        # �ж����ӣ�����ΪyourChessman��λ��ΪyourPosition���Ƿ��������������������򷵻�False�������򷵻��������ӵ��б�
        # ����������Ϸ����Ĺؼ�����ʼdeadlistֻ�������Լ���λ�ã�ÿ��ִ��ʱ����������Ѱ��yourPosition��Χ��û�пյ�λ�ã��������������False����������
        # ���Ҳ����������Լ����ܵ�ͬ�ࣨ����deadlist�еģ��Ƿ������������ñ���������������Ѹ�ͬ����뵽deadlist��Ȼ������һ���ھӣ�ֻҪ��һ������������False����������
        # ������û��һ��������ͬ�࣬����deadlist,���˽����ݹ�
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
        #�ҵ���Χ�Է��������꣬
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


                 if x>=0 and  x <=18 and   y >=0 and  y<=18   :  #�������û��������
                     if  (self.__points[y+1][x+1]=='\033[1;34m' + ' @ ' + '\033[0m'  and  self.__points[next_moves[0]+1][next_moves[1]+1]=='\033[1;31m' + ' 0 ' + '\033[0m') or  (self.__points[y+1][x+1]=='\033[1;31m' + ' 0 ' + '\033[0m'  and  self.__points[next_moves[0]+1][next_moves[1]+1]== '\033[1;34m' + ' @ ' + '\033[0m'):    #����ǶԷ�����
                         self.block=[]
                         killList = self.if_dead([[y, x]], (2 if self.__points[y+1][x+1]=='\033[1;34m' + ' @ ' + '\033[0m' else 1), [y, x])  #1�ǰ��� 2�Ǻ���
                         if not killList == False:
                             self.block += copy.deepcopy(killList)

                         if len(self.block) > 0:
                                 for i in range(len(self.block)):
                                     self.__points[self.block[i][0]+1][self.block[i][1]+1] =' + '
                                 time.sleep(30)

        #�����Ƿ�����
        #���û�������ô�Ƭ����Ϊ��+





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
        #print("���꣺")
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
        #op = msvcrt.getch()     #�ȴ���������

        ##while op != b'q':


        for i, position_w_context in enumerate(file):

                if  position_w_context.next_move is not None :
                  move= position_w_context.next_move
                  self.stone.append( move)

                  self.show(self.stone)
                  print("���ڴ��������ļ���%s:%s"%(file_name,move))
                  self.kill(move)

                else:
                  self.stone.clear()


                time.sleep(1)
                #op = msvcrt.getch()





