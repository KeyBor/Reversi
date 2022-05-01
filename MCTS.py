import datetime
import numpy as np
from copy import deepcopy
import math
import random
import UtilFunc
from Board import *


class Node:
    def __init__(self, state, parent=None, action=None, color=""):
        self.visits = 0  # 访问次数
        self.reward = 0.0  # 期望值
        self.state = state  # 棋盘状态，Broad类
        self.children = []  # 子节点
        self.parent = parent  # 父节点
        self.action = action  # 从父节点转移到本节点采取的动作
        self.color = color  # 该节点玩家颜色

    # 增加子节点
    def add_child(self, child_state, action, color):
        child_node = Node(child_state, parent=self, action=action, color=color)
        self.children.append(child_node)

    # 判断是否完全展开
    def full_expand(self):
        action = UtilFunc.check_legal_move_sim(self.state,1 if(self.color=='O') else -1)
        if len(self.children) == len(action):
            return True
        return False


class AIPlayer:
    """
    AI 玩家
    """
    step = 0

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        # 最大迭代次数
        self.max_times = 50
        # 玩家颜色
        self.chr_color = color
        self.num_color = -1 if(color == 'X') else 1
        # UCB超参数
        self.SCALAR = 1.2

    def select_expand_node(self, node):
        """
        选择扩展的节点
        :param node: 根节点
        :return: 拓展节点
        """
        while not self.game_overed(node.state):

            if len(node.children) == 0:
                new_node = self.expand(node)
                # print(new_node.action)
                return new_node
            elif random.uniform(0, 1) < .5:
                node = self.ucb(node, self.SCALAR)
            else:
                node = self.ucb(node, self.SCALAR)
                if not node.full_expand():
                    return self.expand(node)
                else:
                    node = self.ucb(node, self.SCALAR)
        return node

    def expand(self, node):
        """
        选择扩展的节点
        :param node: 根节点，Node 类
        :return: leave，Node 类
        """
        # 随机选择动作
        action_list = UtilFunc.check_legal_move_sim(node.state,1 if(node.color=='O') else -1)
        # 防止尾盘时出现卡死，没有动作可以选择
        if len(action_list) == 0:
            return node.parent

        action = random.choice(action_list)
        tried_action = [child.action for child in node.children]
        while action in tried_action:
            action = random.choice(action_list)

        # 复制状态并根据动作更新到新状态
        new_state = deepcopy(node.state)
        self.move(new_state,action, 1 if(node.color=='O') else -1)

        # 确定子节点颜色
        if node.color == 'X':
            new_color = 'O'
        else:
            new_color = 'X'

        # 新建节点
        node.add_child(new_state, action=action, color=new_color)
        return node.children[-1]

    def ucb(self, node, scalar):
        """
        选择最佳子节点
        :param node: 节点
        :param scalar: UCT公式超参数
        :return: best_child:最佳子节点
        """
        best_score = -float('inf')
        best_children = []
        for child in node.children:
            exploit = child.reward / child.visits
            if child.visits == 0:
                best_children = [child]
                break
            explore = math.sqrt(2.0 * math.log(node.visits) / float(child.visits))
            now_score = exploit + scalar * explore
            if now_score == best_score:
                best_children.append(child)
            if now_score > best_score:
                best_children = [child]
                best_score = now_score
        if len(best_children) == 0:
            return node.parent
        return random.choice(best_children)

    def uct(self, max_times, root):
        """
        根据当前棋盘状态获取最佳落子位置
        :param max_times: 最大搜索次数
        :param root: 根节点
        :return: action 最佳落子位置
        """
        for t in range(max_times):
            leave_node = self.select_expand_node(root)
            reward = self.random_stimulate_chess(leave_node)
            self.backup(leave_node, reward)
            best_child = self.ucb(root, 0)
        return best_child.action

    def random_stimulate_chess(self, node):
        """
        模拟随机对弈
        :param node: 节点
        :return: reward:期望值
        在定义期望值时同时考虑胜负关系和获胜的子数，board.get_winner()会返回胜负关系和获胜子数
        在这里定义获胜积10分，每多赢一个棋子多1分
        reward = 10 + difference
        """
        board = deepcopy(node.state)
        num_color = -1 if(node.color == 'X') else 1
        count = 0
        # -1 为'X' 1 为 'O'
        while not self.game_overed(board):
            action_list = UtilFunc.check_legal_move_sim(board,num_color)
            if not len(action_list) == 0:
                action = random.choice(action_list)
                self.move(board,action, num_color)
                if num_color == -1:
                    num_color = 1
                else:
                    num_color = -1
            else:
                if num_color == -1:
                    num_color = 1
                else:
                    num_color = -1
                action_list = UtilFunc.check_legal_move_sim(board,num_color)
                action = random.choice(action_list)
                self.move(board,action, num_color)
                if num_color == -1:
                    num_color = 1
                else:
                    num_color = -1
            count = count + 1
            if count >= 50:
                break

        # 价值函数
        _,_, winner, difference = UtilFunc.getWinner_sim(board)
        if winner == 2:
            reward = 0
        elif winner == 1:
            reward = 10 + difference
        else:
            reward = -(10 + difference)

        if self.chr_color == 'X':
            reward = - reward
        return reward

    def backup(self, node, reward):
        """
        反向传播函数
        """
        while node is not None:
            node.visits += 1
            if node.color == self.chr_color:
                node.reward += reward
            else:
                node.reward -= reward
            node = node.parent
        return 0

    def game_overed(self, board):
        """
        判断游戏是否结束
        """

        # 根据当前棋盘，判断棋局是否终止
        # 如果当前选手没有合法下棋的位子，则切换选手；如果另外一个选手也没有合法的下棋位置，则比赛停止。
        now_loc = UtilFunc.check_legal_move_sim(board,1)
        next_loc = UtilFunc.check_legal_move_sim(board,-1)

        over = len(now_loc) == 0 and len(next_loc) == 0  # 返回值 True/False

        return over

    def move(self,board,action,color):
        accessPos = UtilFunc.check_legal_move_sim(board,color)
        if (len(accessPos) == 0):
            return -1
        else:
            UtilFunc.flip_sim(board,action[0],action[1], color)
            return 1

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置
        """
        if self.chr_color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.chr_color))

        board_state = deepcopy(board)
        root = Node(state=board_state, color=self.chr_color)
        action = self.uct(300, root)  # 可设置最大搜索次数

        return action
