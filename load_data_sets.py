#-*- coding:gbk -*-
#from features import bulk_extract_features
import copy
import time

import numpy as np
import os
import sgf_wrapper
from sgf_wrapper import replay_sgf   #wrapper 封装
import sys
import itertools
#import tqdm
from tqdm import tqdm
import gzip
import go
import auto_play
import utils
import struct
from collections import namedtuple

from features import bulk_extract_features,make_onehot
CHUNK_SIZE = 4096
CHUNK_HEADER_FORMAT = "iii?"
CHUNK_HEADER_SIZE = struct.calcsize(CHUNK_HEADER_FORMAT)


np.set_printoptions(threshold=sys.maxsize)    #打印时显示完整矩阵





def take_n(n, iterable):
    return list(itertools.islice(iterable, n))




def iter_chunks(chunk_size, iterator):
    while True:
        next_chunk = take_n(chunk_size, iterator)
        # If len(iterable) % chunk_size == 0, don't return an empty chunk.
        if next_chunk:
            yield next_chunk
        else:
            break
'''
def display(n,move):                #显示棋盘变化
    for i in tqdm(range(100), desc='1st loop', ncols=75):
          time.sleep(0.01)
          '''

def make_onehot(coords):  #onehot则是顾名思义，一个长度为n的数组，蜂窝煤矩阵，只有一个元素是1，其他元素是0
    print("生成坐标棋谱图")
    num_positions = len(coords)                 #有多少步？

    output = np.zeros([num_positions, go.N ** 2], dtype=np.uint8) #返回给定形状和类型的矩阵，用0填充。uint8是专门用于存储各种图像的 现在是生成多少步，第步有361个点
    #print(output)
    for i, coord in enumerate(coords):                #遍历矩阵
        output[i, utils.flatten_coords(coord)] = 1    #放置坐标 将每一步落子转换成一位数组  flatten即降维 Flatten层用来将输入“压平”，即把多维的输入一维化，常用在从卷积层到全连接层的过渡
                                                      #将第i手,坐标置1
        #display(i,output[i].reshape(go.N,go.N))           #升维成棋盘显示
    return output

def find_sgf_files(*dataset_dirs): #python因为是脚本语言而不是编译语言，所以函数要先定义后才能调用 
    for dataset_dir in dataset_dirs:
        print("获取棋谱文件")
        full_dir=os.path.join(os.getcwd(),dataset_dir)
        dataset_files=[os.path.join(full_dir,name) for name in os.listdir(full_dir)] #取得所有文件的全路径名，os.listdir()得到目录下所有文件名或目录名
                                                                                     #os.listdir
                                                                                     # 小括号( )：代表tuple元组数据类型
                                                                                     # 中括号[ ]：代表list列表数据类型
                                                                                     # 大括号{ }花括号：代表dict字典数据类型 字典是由键对值组组成。冒号':'分开键和值，逗号','隔开组
                                                                                     #在 python 中，strings, tuples, 和 numbers 是不可更改的对象，而 list,dict 等则是可以修改的对象。
        for f in dataset_files:
            if os.path.isfile(f) and f.endswith(".sgf"):   #判断文件是否正确   ,判断字符串是否以指定后缀结尾
               yield f                                      #生成器让数据一步一步地处理，避免一次数据量过大而撑爆内存


def get_positions_from_sgf(file):     #取得行棋位置
    print("正在处理棋谱文件：%s"%file)
    #auto_play.game().__init__()
    with open(file) as t:                                   #打开一个文件到内存
         ft=replay_sgf(t.read())

         auto_play.game().run(ft,file)                      #自动显示棋谱


    with open(file) as f:                                   #打开一个文件到内存(上面已经打开过 要重新打开)

         for  i,position_w_context in enumerate(replay_sgf(f.read())):   #循环打开棋谱文件，得到棋谱数据 使用枚举得到坐标
             #print("正在处理第%s手"%(i+1))
             #print(position_w_context.next_move)    #sgf坐标 横坐标（从左到右） 从a到s   纵坐标：从上到下a到s    现在使用数字坐标先是纵坐票0到18   后是横从坐票0到18


             if position_w_context.is_usable():
                 yield position_w_context

class DataSet(object):   #类名的单词首字母大写 ，类继承了object类的属性 为什么要继承object类呢？目的是便于统一操作。继承object类是为了让自己定义的类拥有更多的属性。比如__init__()
    def __init__(self,pos_features,next_moves,results,is_test=False):      #self代表当前对象的地址，self能避免非限定调用的全局变量。
        #初始化属性
        print("开始初始化数据集对象")
        self.pos_features = pos_features
        self.next_moves = next_moves
        self.results = results
        self.is_test = is_test
        assert pos_features.shape[0]==next_moves.shape[0],"在下一步中出现相同的数不要丢掉"  # 用于判断一个表达式，在表达式条件为 false 的时候触发异常 避免运行后出现崩溃的情况。
        self.data_size = pos_features.shape[0]
        self.board_size = pos_features.shape[1]
        self.input_planes = pos_features.shape[-1]
        self._index_within_epoch = 0
        self.shuffle()

    def shuffle(self):
        print("开始打乱顺序，洗牌")
        perm = np.arange(self.data_size)
        np.random.shuffle(perm)
        self.pos_features = self.pos_features[perm]
        self.next_moves = self.next_moves[perm]
        self._index_within_epoch = 0

    def write(self, filename):
        print("写入中......")
        header_bytes = struct.pack(CHUNK_HEADER_FORMAT, self.data_size, self.board_size, self.input_planes, self.is_test)
        position_bytes = np.packbits(self.pos_features).tostring()
        next_move_bytes = np.packbits(self.next_moves).tostring()
        with gzip.open(filename, "wb", compresslevel=6) as f:   #wb 是以二进制写入   使用with 可以避免因忘记写close而造成数据丢失的问题。
             f.write(header_bytes)        #写入属性头
             f.write(position_bytes)      #写入全部手数
             f.write(next_move_bytes)     #写入每一步


    @staticmethod    #这个注解表示  不用实例化类 可直接使用这个方法
    def from_positions_w_context(positions_w_context, is_test=False):

        positions, next_moves, results = zip(*positions_w_context)    #将元组列表解压成矩阵
        extracted_features = bulk_extract_features(positions)
        encoded_moves = make_onehot(next_moves)
        print("生成数据集对象")
        #print(encoded_moves)
        return DataSet(extracted_features, encoded_moves, results, is_test=is_test)



def split_test_training(positions_w_context,est_num_positions):
    desired_test_size=10**5
    if est_num_positions<2*desired_test_size:                        #1000张棋谱才能充分训练
       print("！！！没有足够的数据生成测试数据集. Splitting 67:33")
       positions_w_context = list(tqdm(positions_w_context))
       test_size = len(positions_w_context) // 3
       return positions_w_context[:test_size], [positions_w_context[test_size:]]
    else:
       print("Estimated number of chunks: %s" % (
             (est_num_positions - desired_test_size) // CHUNK_SIZE), file=sys.stderr)
       test_chunk = take_n(desired_test_size, positions_w_context)
       training_chunks = iter_chunks(CHUNK_SIZE, positions_w_context)
       return test_chunk, training_chunks
    pass

def parse_data_sets(*datasets):  #解析数据
    print("在下面列文件路径{}中查找sfg文件".format('\n'.join(datasets)))          #format:替换{}的内容，join:每个文件中间插入一个换行符 换行符是单引号
    sgf_files=list(find_sgf_files(*datasets))   #得到全路径文件名列表，list() 方法用于将元组转换为列表 
    print("共有%s 个sgf文件"%len(sgf_files),file=sys.stderr)   #错误输出到
    est_num_positions=len(sgf_files)*200 #估计每局手数 estimate：估计
    positions_w_context=itertools.chain(*map(get_positions_from_sgf,sgf_files))#把所有文件组合起来。生成迭代内容，chain()可以把一组迭代对象串联起来，形成一个更大的迭代器
    test_chunk,training_chunks=split_test_training(positions_w_context,est_num_positions)#分割文件
    return test_chunk,training_chunks
