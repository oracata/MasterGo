#-*- coding:gbk -*-
'''
#块注释用3个单引号
代码功能：从sgf文件中提取手数和它们的下一手
2个主要功能：
'''

import sgf
import go
from go  import  Position
from collections import namedtuple
from utils import parse_sgf_coords as pc

import numpy as np


class GameMetadata(namedtuple("GameMetadata", "result handicap board_size")):   #构造类 namedtuple类位于collections模块,有了namedtuple后通过属性访问数据能够让我们的代码更加的直观更好维护
        pass

class PositionWithContext(namedtuple("SgfPosition", "position next_move metadata")):
    '''
    Wrapper around go.Position.
    Stores a position, the move that came next, and the eventual result.
    '''
    def is_usable(self):
        return all([
            self.position is not None,
            self.next_move is not None,
            self.metadata.result != "Void",
            self.metadata.handicap <= 4,
        ])

    def __str__(self):
        return str(self.position) + '\nNext move: {} Result: {}'.format(self.next_move, self.result)


def sgf_prop(value_list):
    '''取sgf属性元素值，把sgf文件转换为合理的值'''
    if value_list is None:
        return None
    if len(value_list) == 1:
        return value_list[0]
    else:
        return value_list
def handle_node(pos, node):
    'A node can either add B+W stones, play as B, or play as W.'
    props = node.properties
    black_stones_added = [pc(coords) for coords in props.get('AB', [])]
    white_stones_added = [pc(coords) for coords in props.get('AW', [])]
    if black_stones_added or white_stones_added:
        return add_stones(pos, black_stones_added, white_stones_added)
    # If B/W props are not present, then there is no move. But if it is present and equal to the empty string, then the move was a pass.
    elif 'B' in props:
        black_move = pc(props.get('B', [''])[0])
        return pos.play_move(black_move, color=go.BLACK)
    elif 'W' in props:
        white_move = pc(props.get('W', [''])[0])
        return pos.play_move(white_move, color=go.WHITE)
    else:
        return pos


def add_stones(pos, black_stones_added, white_stones_added):
    working_board = np.copy(pos.board)
    go.place_stones(working_board, go.BLACK, black_stones_added)
    go.place_stones(working_board, go.WHITE, white_stones_added)
    new_position = Position(board=working_board, n=pos.n, komi=pos.komi, caps=pos.caps, ko=pos.ko, recent=pos.recent, to_play=pos.to_play)
    return new_position


def get_next_move(node):
    if not node.next:
        return None
    props = node.next.properties
    if 'W' in props:
        return pc(props['W'][0])
    else:
        return pc(props['B'][0])

def maybe_correct_next(pos, next_node):
    if next_node is None:
        return
    if (('B' in next_node.properties and not pos.to_play == go.BLACK) or
        ('W' in next_node.properties and not pos.to_play == go.WHITE)):
        pos.flip_playerturn(mutate=True)

def replay_sgf(sgf_contents):
    '''
    '''
    collection=sgf.parse(sgf_contents) #collection能把数据对象化 便于操作
    game=collection.children[0]
    prop=game.root.properties
    assert int(sgf_prop(prop.get('GM',['1'])))==1,"这不是围棋棋谱！"   #prop.get  取到一个元素  字符转数字
    komi=0                                                             #初始化贴子规则
    if prop.get('KM') != None:
        komi=float(sgf_prop(prop.get('KM')))
    metadata=GameMetadata(
            result=sgf_prop(prop.get('RE')),                            #比赛结果
            handicap=int(sgf_prop(prop.get('HA', [0]))),               #让子
            board_size=int(sgf_prop(prop.get('SZ')))                    #棋盘大小
            )
    go.set_board_size(metadata.board_size)
    pos=Position(komi=komi)
    current_node=game.root
    while pos is not None and current_node is not None :                               #开始遍历棋谱节点   sgf字母结点  转为纯数字结点
          pos = handle_node(pos, current_node)
          maybe_correct_next(pos, current_node.next)
          next_move = get_next_move(current_node)
          yield PositionWithContext(pos, next_move, metadata)
          current_node = current_node.next
    pass
