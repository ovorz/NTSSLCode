import random
import numpy as np
if __name__ == '__main__':
#输入：
    OCSVM_Outlier_Index = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TrainSet/pseudo_label/OCSVM_oulier_Trainset_tcy_0206+11_100%.txt', delimiter=',')  # 加载OCSVM的异常值下标
    IF_Outlier_Index=np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TrainSet/pseudo_label/IF_oulier_Trainset_tcy_0206+11_100%.txt', delimiter=',')# 加载IF的异常值下标
    AE_Outlier_Index=np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TrainSet/pseudo_label/AE_oulier_Trainset_tcy_0206+11_100%.txt', delimiter=',')# 加载AE的异常值下标
    Trainyload = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TrainSet/train_y_inv&recv_get_tcy_0206+11_100%.txt', delimiter=',')#加载真实标签值
    train_x = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TrainSet/datafinal_tcy_0206+11_100%.txt', delimiter=',')#
#-----------------------------------------------------------------------------------------------------------------
    Inters = np.intersect1d(np.intersect1d(OCSVM_Outlier_Index,IF_Outlier_Index),AE_Outlier_Index)#求交集
    print(len(Inters))
    score_OC_IF_AE=[]#对应的score_IF值
    inv = []
    recv=[]
    for i in Inters:
        score_OC_IF_AE.append(train_x[int(i)][4])
        inv.append(train_x[int(i)][0])
        recv.append(train_x[int(i)][1])
    print(Inters)
    print(score_OC_IF_AE)
    j = 0
    target = []
    while j < train_x.shape[0]:
        if train_x[j][4] >= min(score_OC_IF_AE) and train_x[j][0] >= min(inv) and train_x[j][1]>=min(recv):
            target.append(1)
            print(train_x[j])
        else:
            target.append(0)
        j += 1
    train_y_new = np.array(target)
np.savetxt("../Data_MultiNode_Mainnet/tcy/100%/TrainSet/pseudo_label/Pseudo_train_y_inv&recv_get_tcy_0206+11_100%.txt", train_y_new, fmt='%f', delimiter=',')#保存伪标签

#混合标签------------------------
# j = 0
# PosiIndex = []
# while j < Trainyload.shape[0]:
#     if int(Trainyload[j]) == 1:
#         PosiIndex.append(j)
#     j += 1
# i = 0
# Posi_nums=len(PosiIndex)
# print('Posi_nums:', Posi_nums)#真实正样本的数量
#
# #随机选取50%的标签作为已知的真实正样本标签，与伪标签进行混合
# RealPositiveLabel=random.sample(PosiIndex,int(0.5*Posi_nums))
# print(RealPositiveLabel)
#
# MixLabel=[]
# k=0
# while k < train_y_new.shape[0]:
#     if k in RealPositiveLabel:
#         MixLabel.append(1)
#     else:
#         MixLabel.append(train_y_new[k])
#     k += 1
# train_y_mix_label = np.array(MixLabel)
# np.savetxt("../pzy/TrainY_Mix-Label_0821_1_jiaoji2.txt", train_y_mix_label, fmt='%f', delimiter=',')#保存混合标签




