import xgboost as xgb
from sklearn import metrics
import numpy as np
# 导入鸢尾花的数据
from sklearn.preprocessing import MinMaxScaler
# 加载数据
import pandas as pd
import pymysql

#输入：-----------------------------------------------------
test_y = np.loadtxt('../Data_MultiNode_Mainnet/gyl/100%/TestSet/train_y_inv&recv_get_gyl_1210.txt', delimiter=',')
y_pred = np.loadtxt('Cluster_train_y_inv&recv_get_gyl_1210.txt', delimiter=',')
#------------------------------------------------------------
recall=[]
precision=[]
f1=[]

#混淆后的data_HASH文件，便于输出交易hash
# df = pd.read_csv('../Data_MultiNode_Testnet/gyl/TestSet/btc_testnet_gyl_shuffle.txt', names=['tx_id', 't1', 't2', 't3', 't4'])
dic={}
confusion_metrix = metrics.confusion_matrix(test_y, y_pred)
dic["TN"] = confusion_metrix[0][0]
dic["TP"] = confusion_metrix[1][1]
dic["FP"] = confusion_metrix[0][1]
dic["FN"] = confusion_metrix[1][0]
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

# sql = "insert into tx_ip_map(txhash,nodeaddr) values(%s,%s)"
# i=0
# while i<y_pred.shape[0]:
#     if y_pred[i] == 1:
#         try:
#             cursor.execute(sql, (TestResult[i][0],'118.25.12.97:8333'))
#             db.commit()
#             print(1)
#         except Exception as e:
#             db.rollback()
#     i+=1
