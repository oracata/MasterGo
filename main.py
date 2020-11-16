# -*- coding: gbk -*-
#import tensorflow as tf
import argh       #������ģ�� 
import argparse   #������ѡ������������������   
import tqdm
import os
import sys
from load_data_sets import DataSet, parse_data_sets  #��xxx���� xxx�� import���� Ҳ�����Լ���д��ģ��

#TRAINING_CHUNK_RE = re.compile(r"train\d+\.chunk.gz")
def gtp():
    print("��������gtpģ��")

def train():
    print("��������trainģ��")

def preprocess(*datasets,processed_dir="processed_data"):    #��һ���Ǻţ�*�������ĺ�������Ĳ����洢Ϊһ��Ԫ�飨tuple����(2,3,4)��������*�������Ǳ�ʾ�ֵ䣨dict����{a:2, b:3}
    print("��������preprocessģ��")
    processed_dir=os.path.join(os.getcwd(),processed_dir) #���·��
    if not os.path.isdir(processed_dir):    
        os.mkdir(processed_dir)
    #TensorFlow���洢���Լ���Ӧ�Ŀ���Ϣ����Ϊһ�ֽ���Chunk(���)��˫���������ݽṹ��
    test_chunk,training_chunks=parse_data_sets(*datasets)  
    print("���� %s λ����Ϊ���Կ�; ʣ�����ѵ����" % len(test_chunk), file=sys.stderr)


    test_dataset=DataSet.from_positions_w_context(test_chunk,is_test=True) #DataSet��
    test_filename=os.path.join(processed_dir,"test.chunk.gz")
    print("д��������ݿ�")
    test_dataset.write(test_filename)

    training_datasets=map(DataSet.from_positions_w_context,training_chunks)
    for i,train_dataset in tqdm.tqdm(enumerate(training_datasets)):
        train_filename=os.path.join(processed_dir,"train%s.chunk.gz"% i)
        print("д��ѵ�����ݿ�")
        train_dataset.write(train_filename)
    print("�Ѿ�д��ѵ������%s"%(i+1))

parser=argparse.ArgumentParser()   #��������������
argh.add_commands(parser,[gtp,preprocess,train])   #��������

if __name__ == '__main__' :    #ÿ��pythonģ�飨python�ļ���Ҳ���Ǵ˴���test.py��import_test.py�����������õı���__name__,������ģ�鱻ִ�е�ʱ��__name__�����ļ����������˺�׺.py��
    argh.dispatch(parser)      #���ݲ���ת������Ӧģ��
