import xgboost as xgb
from sklearn import metrics
import numpy as np
# 导入鸢尾花的数据
from sklearn.preprocessing import MinMaxScaler
# 加载数据
import pandas as pd

# 输入：-------------------------------------------------------------------------
TrainXload = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TrainSet/datafinal_tcy_1208.txt', delimiter=',')
Trainyload = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TrainSet/pseudo_label/Pseudo_train_y_inv&recv_get_tcy_1208.txt',
                        delimiter=',')  # 伪标签样本集
TestXload = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TestSet/datafinal_tcy_1210.txt', delimiter=',')
Testyload = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TestSet/train_y_inv&recv_get_tcy_1210.txt', delimiter=',')
TestTxs = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TestSet/main_tx_inv&recv_get_tcy_1210.txt', delimiter=',',
                     dtype='str')
# ------------------------------------------------------------
# 实现归一化
scalar = MinMaxScaler()  # 实例化
# 参数设置
params = {'booster': 'gbtree',
          'objective': 'binary:logistic',
          'eval_metric': 'auc',
          'max_depth': 5,  # 深度
          'lambda': 10,
          'subsample': 0.55,
          'colsample_bytree': 0.55,
          'min_child_weight': 2,
          'eta': 0.025,
          'seed': 2020,  # 随机种子
          'nthread': 8,
          'silent': 0,
          'scale_pos_weight': 5,
          'zero_division': 1}
recall = []
precision = []
f1 = []

train_X, train_y = scalar.fit_transform(TrainXload), Trainyload
test_X, test_y = scalar.fit_transform(TestXload), Testyload

dtrain = xgb.DMatrix(train_X, label=train_y)
watchlist = [(dtrain, 'train')]
bst = xgb.train(params, dtrain, num_boost_round=100, evals=watchlist)  # to save model训练函数
dtest = xgb.DMatrix(test_X)
ypred = bst.predict(dtest)
thredhold = 0.16
inp = []
print(ypred)
# 混淆后的data_HASH文件，便于输出交易hash
# df = pd.read_csv('../Data_MultiNode_Testnet/gyl/TestSet/btc_testnet_gyl_shuffle.txt', names=['tx_id', 't1', 't2', 't3', 't4'])
while thredhold < 1:
    dic = {}
    thredhold = round(thredhold + 0.02, 3)
    dic["thredhold"] = thredhold
    score = ypred
    y_pred = (ypred >= thredhold) * 1
    TestResult = []
    print(len(y_pred))
    i = 0
    while i < len(y_pred):
        if (y_pred[i] == 1):
            TestResult.append([TestTxs[i][0], 1, score[i]])
        else:
            TestResult.append([TestTxs[i][0], 0, score[i]])
        i += 1
    TestResult = np.array(TestResult)
    np.savetxt("../Data_MultiNode_Mainnet/tcy/100%/TestSet/TestResult_tcy_1210.txt", TestResult, fmt='%s',delimiter=',')  # 保存测试集中的交易以及检测结果
    confusion_metrix = metrics.confusion_matrix(test_y, y_pred)
    dic["TN"] = confusion_metrix[0][0]
    dic["TP"] = confusion_metrix[1][1]
    dic["FP"] = confusion_metrix[0][1]
    dic["FN"] = confusion_metrix[1][0]
    print("thredhold", thredhold, "_______________________zz___________")
    print('ACC: %.4f' % metrics.accuracy_score(test_y, y_pred))
    print('Recall: %.4f' % metrics.recall_score(test_y, y_pred))
    fpr, tpr, thresholds = metrics.roc_curve(test_y, y_pred, pos_label=1)
    print('Fpr:', dic["FP"] / (dic["FP"] + dic["TN"]))
    print('F1-score: %.4f' % metrics.f1_score(test_y, y_pred))
    print('Precesion: %.4f' % metrics.precision_score(test_y, y_pred))
    dic["Recall"] = metrics.recall_score(test_y, y_pred)
    dic["Precision"] = metrics.precision_score(test_y, y_pred)
    dic["F1"] = metrics.f1_score(test_y, y_pred)
    dic["Fpr"] = dic["FP"] / (dic["FP"] + dic["TN"])
    inp.append(dic)
    break
df = pd.DataFrame(inp)
# df.to_csv("../Data_MultiNode_Mainnet/tcy/100%/TestSet/xgb_pseudo_label.csv")

