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
                    elif j==19:
                        line.append('# ')  #结尾
                    else:
                        line.append('#  ')  # 横线框加2个空格


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
                line.append('#')
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
             self.__points[stone_location[0]][stone_location[1]] =  '\033[1;34m' + ' @ ' + '\033[0m'
           else :
             self.__points[stone_location[0]][stone_location[1]] ='\033[1;31m' + ' 0 ' + '\033[0m'
           i=i+1

    def show(self):
        os.system("cls")

        for i in range(21):
            for j in range(21):
                print(self.__points[i][j], end='')
            print()


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



    def new_stone(self):
        while 1:
            line = random.randint(1, 20)
            column = random.randint(1, 20)
            if self.board.getPoint([column, line]) == ' ':
                self.stone = [column, line]
                return


    def show(self,next_moves):
        #print("坐标：")
        #print(next_moves)
        self.board.clear()
        #self.board.put_snake(self.snake.getPoints())
        self.board.put_stone(next_moves)
        self.board.show()



    def run(self,file):

        self.board.show()

        # the 'w a s d' are the directions
        #operation_dict = {b'w': 'up', b'W': 'up', b's': 'down', b'S': 'down', b'a': 'left', b'A': 'left', b'd': 'right', b'D': 'right'}
        op = msvcrt.getch()

        #while op != b'q':
        for i, self.position_w_context in enumerate(file):

                if self.position_w_context.next_move is not None:
                  self.stone.append(self.position_w_context.next_move)
                  self.show(self.stone)
                  time.sleep(2)
                  #op = msvcrt.getch()





