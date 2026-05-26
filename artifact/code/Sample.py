# 实现IsolationForest高维数据的异常值检测算法
import random
import matplotlib.pyplot as plt
import numpy as np
import math
from collections import Counter
import sys
import pandas as pd
from sklearn.ensemble._hist_gradient_boosting.common import POS

from sklearn.metrics import precision_recall_curve
from sklearn.preprocessing import MinMaxScaler
#source code:https://blog.csdn.net/slx_share/article/details/87872420


sys.setrecursionlimit(1000000)

class Node:
    def __init__(self, val=None, right=None, left=None):
        self.val = val  # 存储样本索引,仅叶节点
        self.right = right
        self.left = left
class RandomTree:
    def __init__(self):
        self.tree = None
        self.n_feas = None

    def get_split(self, data, inds):
        # 随机构建切分点
        f = np.random.choice(self.n_feas)  # 随机选择一个特征
        up = max(data[inds, f])
        down = min(data[inds, f])
        v = (up - down) * np.random.sample() + down  # 在该特征的最大与最小值间随机选择一个数
        return f, v
    def split(self, data, inds):
        # 切分数据集
        f, v = self.get_split(data, inds)
        left_ind = []
        right_ind = []
        for i in inds:
            if data[i, f] <= v:
                left_ind.append(i)
            else:
                right_ind.append(i)
        return left_ind, right_ind

    def buildTree(self, data, inds):
        if len(inds) < 3:  # 叶节点
            return Node(val=inds)
        left_ind, right_ind = self.split(data, inds)
        left = self.buildTree(data, left_ind)
        right = self.buildTree(data, right_ind)
        return Node(left=left, right=right)

    def fit(self, data):
        self.n_feas = data.shape[1]
        inds = np.arange(data.shape[0])
        self.tree = self.buildTree(data, inds)
        return

    def traverse(self):
        # 遍历树，统计每个样本的路径长
        path_len = Counter()
        i = -1
        def helper(currentNode):
            nonlocal i
            i += 1
            if currentNode.val is not None:
                for ind in currentNode.val:
                    path_len[ind] = i
                return
            for child in [currentNode.left, currentNode.right]:
                helper(child)
                i -= 1
            return
        helper(self.tree)
        return path_len

class IsolationForest:
    def __init__(self, n_tree, epsilon):
        self.n_tree = n_tree
        self.epsilon = epsilon  # 异常点比例
        self.scores = Counter()
    def fit_predict(self, data):
        for _ in range(self.n_tree):
            RT = RandomTree()
            RT.fit(data)
            path_len = RT.traverse()
            self.scores = self.scores + path_len
        n_sample = data.shape[0]
        phi = 2 * math.log(n_sample - 1) - 2 * (n_sample - 1) / n_sample
        for key, val in self.scores.items():
            self.scores[key] = 2 ** -(val / self.n_tree / phi)  # 归一化
        q = np.quantile(list(self.scores.values()), 1 - self.epsilon)
        outliers = [key for key, val in self.scores.items() if val > q]
        # print(self.scores)
        score = []
        i = 0
        while i < data.shape[0]:
            score.append(self.scores[i])
            i += 1
        s = np.array(score)
        new = np.insert(data, 4, values=s, axis=1)
        np.savetxt("../Data_MultiNode_Mainnet/tcy/100%/TestSet/datafinal_tcy_0215_100%.txt", new,fmt='%f',delimiter=',')
        for o in outliers:
            print(self.scores[o], o)
        return outliers,score
def data_pro(data):
    A = 0
    B = 0.0001  # 小数的范围A ~ B
    a = random.uniform(A, B)
    C = 10  # 随机数的精度round(数值，精度)
    return data + round(a, C) #保留小数点后十位

if __name__ == '__main__':
    # # ----------------------------------------------------------------------------
    Trainyload=np.loadtxt('../Data_MultiNode_Mainnet/pzy/100%/TestSet/train_y_inv&recv_get_pzy_0215_100%.txt', delimiter=',')
    tx = np.loadtxt('../Data_MultiNode_Mainnet/pzy/100%/TestSet/main_tx_inv&recv_get_pzy_0215_100%.txt', delimiter=',',dtype='str')
    invAndrecv_get = np.loadtxt('../Data_MultiNode_Mainnet/pzy/100%/TestSet/main_inv&recv_get_pzy_0215_100%.txt', delimiter=',')
    i=0
    PosIndex=[]

    while i<Trainyload.shape[0]:
        if Trainyload[i]==1:
            PosIndex.append(i)
        i+=1
    print(PosIndex)
    tx_pos = tx[PosIndex]
    Trainyload_pos = Trainyload[PosIndex]
    invAndrecv_get_pos = invAndrecv_get[PosIndex]
    Trainyload_neg=np.delete(Trainyload,PosIndex)
    tx_neg=np.delete(tx,PosIndex,axis=0)
    invAndrecv_get_neg=np.delete(invAndrecv_get,PosIndex,axis=0)

    indices = np.random.choice(Trainyload_neg.shape[0], 5000, replace=False)
    Trainyload_new=np.concatenate((Trainyload_neg[indices], Trainyload_pos))
    invAndrecv_get_new=np.concatenate((invAndrecv_get_neg[indices],invAndrecv_get_pos))
    tx_new=np.concatenate((tx_neg[indices], tx_pos))
    print(Trainyload_new.shape[0])
    np.savetxt("../Data_MultiNode_Mainnet/pzy/100%/TestSet/train_y_inv&recv_get_pzy_0215_100%_sampled.txt", Trainyload_new, fmt='%f', delimiter=',')
    np.savetxt("../Data_MultiNode_Mainnet/pzy/100%/TestSet/main_inv&recv_get_pzy_0215_100%_sampled.txt", invAndrecv_get_new, fmt='%f',
               delimiter=',')
    np.savetxt("../Data_MultiNode_Mainnet/pzy/100%/TestSet/main_tx_inv&recv_get_pzy_0215_100%_sampled.txt", tx_new, fmt='%s',
               delimiter=',')


