#-*- coding:gbk -*-
#from features import bulk_extract_features
import numpy as np
import os
from sgf_wrapper import replay_sgf   #wrapper ��װ
import sys
import itertools
import tqdm
import gzip
import go
import utils
import struct

from features import bulk_extract_features,make_onehot

CHUNK_HEADER_FORMAT = "iii?"


def make_onehot(coords):
    num_positions = len(coords)
    output = np.zeros([num_positions, go.N ** 2], dtype=np.uint8)
    for i, coord in enumerate(coords):
        output[i, utils.flatten_coords(coord)] = 1
    return output

def find_sgf_files(*dataset_dirs): #python��Ϊ�ǽű����Զ����Ǳ������ԣ����Ժ���Ҫ�ȶ������ܵ��� 
    for dataset_dir in dataset_dirs:
        full_dir=os.path.join(os.getcwd(),dataset_dir)
        dataset_files=[os.path.join(full_dir,name) for name in os.listdir(full_dir)] #ȡ�������ļ���ȫ·������os.listdir()�õ�Ŀ¼�������ļ�����Ŀ¼��
                                                                                     #os.listdir
                                                                                     # С����( )������tupleԪ����������
                                                                                     # ������[ ]������list�б���������
                                                                                     # ������{ }�����ţ�����dict�ֵ��������� �ֵ����ɼ���ֵ����ɡ�ð��':'�ֿ�����ֵ������','������
                                                                                     #�� python �У�strings, tuples, �� numbers �ǲ��ɸ��ĵĶ��󣬶� list,dict �����ǿ����޸ĵĶ���
        for f in dataset_files:
            if os.path.isfile(f) and f.endswith(".sgf"):   #�ж��ļ��Ƿ���ȷ   ,�ж��ַ����Ƿ���ָ����׺��β
               yield f                                      #������������һ��һ���ش���������һ��������������ű��ڴ�


def get_positions_from_sgf(file):     #ȡ������λ��
    with open(file) as f:                                   #��һ���ļ����ڴ�
         for position_w_context in replay_sgf(f.read()):   #�õ�����λ��
             if position_w_context.is_usable():
                 yield position_w_context

class DataSet(object):   #�����ĵ�������ĸ��д ����̳���object������� ΪʲôҪ�̳�object���أ�Ŀ���Ǳ���ͳһ�������̳�object����Ϊ�����Լ��������ӵ�и�������ԡ�����__init__()
    def __init__(self,pos_features,next_moves,results,is_test=False):      #self������ǰ����ĵ�ַ��self�ܱ�����޶����õ�ȫ�ֱ�����
        #��ʼ������
        self.pos_features = pos_features
        self.next_moves = next_moves
        self.results = results
        self.is_test = is_test
        assert pos_features.shape[0]==next_moves.shape[0],"����һ���г�����ͬ������Ҫ����"  # �����ж�һ������ʽ���ڱ���ʽ����Ϊ false ��ʱ�򴥷��쳣 �������к���ֱ����������
        self.data_size = pos_features.shape[0]
        self.board_size = pos_features.shape[1]
        self.input_planes = pos_features.shape[-1]
        self._index_within_epoch = 0
        self.shuffle()

    def shuffle(self):
        perm = np.arange(self.data_size)
        np.random.shuffle(perm)
        self.pos_features = self.pos_features[perm]
        self.next_moves = self.next_moves[perm]
        self._index_within_epoch = 0

    def write(self, filename):
        header_bytes = struct.pack(CHUNK_HEADER_FORMAT, self.data_size, self.board_size, self.input_planes, self.is_test)
        position_bytes = np.packbits(self.pos_features).tostring()
        next_move_bytes = np.packbits(self.next_moves).tostring()
        with gzip.open(filename, "wb", compresslevel=6) as f:
             f.write(header_bytes)
             f.write(position_bytes)
             f.write(next_move_bytes)

       #���
    @staticmethod    #���ע���ʾ  ����ʵ������ ��ֱ��ʹ���������
    def from_positions_w_context(positions_w_context, is_test=False):
        positions, next_moves, results = zip(*positions_w_context)    #��Ԫ���б���ѹ�ɾ���
        extracted_features = bulk_extract_features(positions)
        encoded_moves = make_onehot(next_moves)
        return DataSet(extracted_features, encoded_moves, results, is_test=is_test)

def split_test_training(positions_w_context,est_num_positions):
    desired_test_size=10**5
    if est_num_positions<2*desired_test_size:                        #1000�����ײ��ܳ��ѵ��
       print("������û���㹻���������ɲ������ݼ�. Splitting 67:33")
       positions_w_context = list(tqdm.tqdm(positions_w_context))
       test_size = len(positions_w_context) // 3
       return positions_w_context[:test_size], [positions_w_context[test_size:]]
    else:
       print("Estimated number of chunks: %s" % (
             (est_num_positions - desired_test_size) // CHUNK_SIZE), file=sys.stderr)
       test_chunk = take_n(desired_test_size, positions_w_context)
       training_chunks = iter_chunks(CHUNK_SIZE, positions_w_context)
       return test_chunk, training_chunks
    pass

def parse_data_sets(*datasets):  #��������
    print("���������ļ�·��{}�в���sfg�ļ�".format('\n'.join(datasets)))          #format:�滻{}�����ݣ�join:ÿ���ļ��м����һ�����з� ���з��ǵ�����
    sgf_files=list(find_sgf_files(*datasets))   #�õ�ȫ·���ļ����б���list() �������ڽ�Ԫ��ת��Ϊ�б� 
    print("����%s ��sgf�ļ�"%len(sgf_files),file=sys.stderr)   #���������
    est_num_positions=len(sgf_files)*200 #����ÿ������ estimate������
    positions_w_context=itertools.chain(*map(get_positions_from_sgf,sgf_files))#�������ļ�������������ɵ������ݣ�chain()���԰�һ������������������γ�һ������ĵ�����
    test_chunk,training_chunks=split_test_training(positions_w_context,est_num_positions)#�ָ��ļ�
    return test_chunk,training_chunks