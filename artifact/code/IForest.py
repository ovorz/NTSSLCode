# 实现IsolationForest高维数据的异常值检测算法
import random
import matplotlib.pyplot as plt
import numpy as np
import math
from collections import Counter
import sys
import pandas as pd

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
        np.savetxt("../Data_MultiNode_Mainnet/pzy/100%/TestSet/datafinal_pzy_0221_100%_Pt2.txt", new,fmt='%f',delimiter=',')
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
    Trainyload=np.loadtxt('../Data_MultiNode_Mainnet/pzy/100%/TestSet/train_y_inv&recv_get_pzy_0221_100%_Pt2.txt', delimiter=',')
    # invAndsend_get = np.loadtxt('../MainnetExperiment/100%/MidResult/main_inv&send_get_tcy_1121_Pt2_100%.txt', delimiter=',')
    invAndrecv_get = np.loadtxt('../Data_MultiNode_Mainnet/pzy/100%/TestSet/main_inv&recv_get_pzy_0221_100%_Pt2.txt', delimiter=',')
    i = 0
    data_final = []
    data_final_3 = []
    while i < invAndrecv_get.shape[0]:
        # if invAndrecv_get[i][0] == invAndsend_get[i][0]:
        if 1:
            inv_send = data_pro(invAndrecv_get[i][0])
            # getdata_send = data_pro(invAndsend_get[i][1])
            getdata_recv = data_pro(invAndrecv_get[i][1])
            sum = data_pro(invAndrecv_get[i][1] + invAndrecv_get[i][0]) * 10
            ratio = 10000 * (round(data_pro(invAndrecv_get[i][1]) / data_pro(invAndrecv_get[i][0]), 10))
            data_final.append([inv_send, getdata_recv,ratio, sum])
            # data_final_3.append([getdata_recv, getdata_send, ratio])#fc21论文中的特征向量
        else:
            print(i+1)
        i += 1
    # data_final_txs=np.loadtxt('data_final_txs_self.txt',delimiter=',')
    #     # data_final=np.loadtxt('main_data_final_new_0112_full.txt',delimiter=',')
    PosiIndex = []
    testy=[]
    j = 0
    while j < Trainyload.shape[0]:
        if int(Trainyload[j]) == 1:
            PosiIndex.append(j)
        # testy.append(Trainyload[j]*1)
        j += 1
    # test_y=np.array(testy)
    print('Posi_nums:', len(PosiIndex))
    # data_final_3 =np.loadtxt('Dataset_75%_Connections/main_data_final_xgb_0112_75%_fullWithScore.txt',delimiter=',')
    # temp_4 = np.array(data_final)
    temp_3 = np.array(data_final)
    # --------------------------------------------------
    i=0.01
    inp=[]
    while i < 0.02:
        dic={}
        IF = IsolationForest(100, i)  # 设置异常数据比例
        out_ind, ypred = IF.fit_predict(temp_3)
        out_ind_len = len(out_ind)
        print(out_ind, out_ind_len)
        # np.savetxt("../Data_MultiNode_Mainnet/tcy/100%/TrainSet/pseudo_label/IF_oulier_Trainset_tcy_0206+11_100%.txt", out_ind, fmt='%f', delimiter=',')  # 保存检测出来的异常值的下标
        inters = np.intersect1d(np.array(PosiIndex), out_ind)
        hit = len(inters)
        print(inters, hit)
        recall = hit / len(PosiIndex)
        print("i=",i)
        print('recall:', recall)
        fpr = (out_ind_len - hit) / (len(data_final) - len(PosiIndex))
        print('fpr:', fpr)
        precision = hit / out_ind_len
        print('precision:', precision)
        f1=2 * recall * precision / (recall + precision)
        print('f1:', f1)
        dic["threshold"] = i
        dic["recall"] = recall
        dic["precision"] = precision
        dic["fpr"] = fpr
        dic["F1"] = f1
        i += 0.02
        inp.append(dic)
df = pd.DataFrame(inp)
# df.to_csv("../Data_MultiNode_Mainnet/tcy/TrainSet/IF_mainnet_recall_pre_f1_tcy_1208.csv")#保存不同阈值下的检测效果
