# -*- coding: gbk -*-
#import tensorflow as tf
import argh       #命令行模块 
import argparse   #命令行选项、参数和子命令解析器   
import tqdm
import os
import sys
from load_data_sets import DataSet, parse_data_sets  #把xxx库里 xxx类 import进来 也可以自己编写的模块

#TRAINING_CHUNK_RE = re.compile(r"train\d+\.chunk.gz")
def gtp():
    print("正在运行gtp模块")

def train():
    print("正在运行train模块")

def preprocess(*datasets,processed_dir="processed_data"):    #带一个星号（*）参数的函数传入的参数存储为一个元组（tuple）→(2,3,4)带两个（*）号则是表示字典（dict）→{a:2, b:3}
    print("正在运行preprocess模块")
    processed_dir=os.path.join(os.getcwd(),processed_dir) #输出路径
    if not os.path.isdir(processed_dir):    
        os.mkdir(processed_dir)
    #TensorFlow将存储块以及相应的块信息抽象为一种叫做Chunk(组块)的双向链表数据结构。
    test_chunk,training_chunks=parse_data_sets(*datasets)  
    print("分配 %s 位置作为测试块; 剩余的作训练块" % len(test_chunk), file=sys.stderr)


    test_dataset=DataSet.from_positions_w_context(test_chunk,is_test=True) #DataSet类
    test_filename=os.path.join(processed_dir,"test.chunk.gz")
    print("写入测试数据块")
    test_dataset.write(test_filename)

    training_datasets=map(DataSet.from_positions_w_context,training_chunks)
    for i,train_dataset in tqdm.tqdm(enumerate(training_datasets)):
        train_filename=os.path.join(processed_dir,"train%s.chunk.gz"% i)
        print("写入训练数据块")
        train_dataset.write(train_filename)
    print("已经写入训练数据%s"%(i+1))

parser=argparse.ArgumentParser()   #创建参数解析器
argh.add_commands(parser,[gtp,preprocess,train])   #增加命令

if __name__ == '__main__' :    #每个python模块（python文件，也就是此处的test.py和import_test.py）都包含内置的变量__name__,当运行模块被执行的时候，__name__等于文件名（包含了后缀.py）
    argh.dispatch(parser)      #根据参数转发到对应模块
