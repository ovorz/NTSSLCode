import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np

plt.style.use('fivethirtyeight')
from sklearn import svm

# 输入文件
Trainyload = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TrainSet/train_y_inv&recv_get_tcy_0206+11_100%.txt', delimiter=',')#标签集
Trainxload = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TrainSet/datafinal_tcy_0206+11_100%.txt', delimiter=',')#训练集
j = 0
PosiIndex = []
while j < Trainyload.shape[0]:
    if int(Trainyload[j]) == 1:
        PosiIndex.append(j)
    j += 1
i = 0
print('Posi_nums:', len(PosiIndex))#真实正样本的数量

# use the same dataset
scalar = MinMaxScaler()  # 实例化
tr_data = scalar.fit_transform(Trainxload[:,:3])
clf = svm.OneClassSVM(nu=0.005, kernel='rbf', gamma=0.1)#nu表示阈值
'''
OneClassSVM(cache_size=200, coef0=0.0, degree=3, gamma=0.1, kernel='rbf',
      max_iter=-1, nu=0.05, random_state=None, shrinking=True, tol=0.001,
      verbose=False)
'''
clf.fit(tr_data)
pred = clf.predict(tr_data)
index = []
print(pred.shape[0])
i = 0
while i < pred.shape[0]:
    if pred[i] == -1:
        index.append(i)
    i += 1
print(index)
outlier_index = np.array(index)#保存检测为异常值的下标
# inliers are labeled 1（转发交易） , outlier are labeled -1（始发交易）
np.savetxt("../Data_MultiNode_Mainnet/tcy/100%/TrainSet/pseudo_label/OCSVM_oulier_Trainset_tcy_0206+11_100%.txt", outlier_index,fmt='%f',delimiter=',')#保存到文件中

# 伪标签，就要去拿outlier_index 和隔离森林的结果去求交集，得到的那个集合就是第一步的正样本集合，score_IF，求集合中最小的score_IF值，再去判断（大于这个最小值score_IF的标为正样本）并重新打标
inters = np.intersect1d(np.array(PosiIndex), outlier_index)
print(inters, len(inters))#查看有多少命中真实标签
