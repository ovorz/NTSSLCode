import math
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')
from sklearn.model_selection import train_test_split
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint
from keras import regularizers
from sklearn.preprocessing import StandardScaler, MinMaxScaler

data_ae = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/AE_background/datafinal_tcy_0212_100%.txt', delimiter=',')#加载背景集，作为自训练过程中的训练集与验证集
scalar = MinMaxScaler()  # 实例化
data_ae = scalar.fit_transform(data_ae[:,:3])#选择前三列数据，即不使用score作为特征值
#按照8:2切成训练集和测试集
X_train, X_test = train_test_split(data_ae, test_size=0.2, random_state=520)
test = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TrainSet/datafinal_tcy_0206+11_100%.txt', delimiter=',')#加载测试样本集合
Trainyload = np.loadtxt('../Data_MultiNode_Mainnet/tcy/100%/TrainSet/train_y_inv&recv_get_tcy_0206+11_100%.txt', delimiter=',')#加载真实标签
j = 0
PosiIndex = []
while j < Trainyload.shape[0]:
    if int(Trainyload[j]) == 1:
        PosiIndex.append(j)
    j += 1
i = 0
print('Posi_nums:', len(PosiIndex))#保存真实正样本下标集合
test = scalar.fit_transform(test[:,:3])
input_dim = X_train.shape[1]
encoding_dim = 16
num_epoch = 50
batch_size = 32
input_layer = Input(shape=(input_dim,))
encoder = Dense(encoding_dim, activation="tanh",
                activity_regularizer=regularizers.l1(10e-5))(input_layer)
encoder = Dense(int(encoding_dim / 2), activation="relu")(encoder)
decoder = Dense(int(encoding_dim / 2), activation='tanh')(encoder)
decoder = Dense(input_dim, activation='relu')(decoder)
autoencoder = Model(inputs=input_layer, outputs=decoder)
autoencoder.compile(optimizer='adam',
                    loss='mean_squared_error',
                    metrics=['mae'])

# 模型保存为SofaSofa_model.h5，并开始训练模型
checkpointer = ModelCheckpoint(filepath="SofaSofa_model.h5",
                               verbose=0,
                               save_best_only=True)
history = autoencoder.fit(X_train, X_train,
                          epochs=num_epoch,
                          batch_size=batch_size,
                          shuffle=True,
                          validation_data=(X_test, X_test),
                          verbose=1,
                          callbacks=[checkpointer]).history
# 读取模型
autoencoder = load_model('SofaSofa_model.h5')

# 利用训练好的autoencoder重建测试集
pred_test = autoencoder.predict(X_test)
# pred_fraud = autoencoder.predict(X_fraud)
pred_detect = autoencoder.predict(test)

# 计算还原误差MSE和MAE
mse_test = np.mean(np.power(X_test - pred_test, 2), axis=1)
# mse_fraud = np.mean(np.power(X_fraud - pred_fraud, 2), axis=1)
mse_detect = np.mean(np.power(test - pred_detect, 2), axis=1)
# print(mse_detect)
n = math.ceil(mse_detect.shape[0] * 0.005)  # 设置阈值
outlier_index = mse_detect.argsort()[-n:][::-1]
print(outlier_index, len(outlier_index))
np.savetxt("../Data_MultiNode_Mainnet/tcy/100%/TrainSet/pseudo_label/AE_oulier_Trainset_tcy_0206+11_100%.txt", outlier_index,fmt='%f',delimiter=',')#保存到文件中
#------------------------------------------------------------------
inters = np.intersect1d(np.array(PosiIndex), outlier_index)
print(inters, len(inters))#查看有多少命中真实标签
