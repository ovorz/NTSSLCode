import json
import time
import numpy as np
from datetime import datetime, date
from datetime import timedelta
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import plistlib
import os
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
# -*- coding = utf-8 -*-
import requests
import binascii





def big_small_end_convert(data):
    return bytes.decode(binascii.hexlify(binascii.unhexlify(data)[::-1]))


PRICE = 'D:/硕士/USD_CNY.xlsx'


def ts2t(ts):  # 时间戳转为时间
    timeArray = time.localtime(ts)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def getHash(txid):
    url = "https://api.blockchair.com/bitcoin/testnet/raw/transaction/" + str(txid)
    r = requests.get(url, timeout=60)
    re = json.loads(r.text)
    return re['data'][str(txid)]['decoded_raw_transaction']['hash']

bgp_dump = "D:/硕士/项目/FC21_wireshark/updates.20210526.0125.gz"  # 换成自己的路径
if __name__ == '__main__':
    # url='https://api.blockchair.com/bitcoin/testnet/raw/transaction/19c654b48ff7b09b09b92684187b1d5d13c81f46b2f0912190e703faf5c311a4'
    # r = requests.get(url)
    # re = json.loads(r.text)
    # print(re['data'])
    # try:
    #     print(getHash("14e137d3e5444a8161b1bdf4a18e475c168f8b51aa5a0dac7a1945c6b4c42fea"))
    #     # hash = getHash("19c654b48ff7b09b09b92684187b1d5d13c81f46b2f0912190e703faf5c311a4")
    #     # if hash == "e36f877040c0f15ebbc8e2cdeb5569bad0388bd068c05f13227882e7e42576c7":
    #     #     print("yes")
    # except:
    #     print("error")
    pcap_hash='fc:cb:ed:d0:55:13:46:12:ba:be:4e:b0:a0:c9:94:ad:7f:e8:6e:9f:e8:4c:a5:e0:82:ee:54:45:64:6e:54:ca'
    di = '1d1e201a5841479d30438e41b6e5e8c6780f28ecb5ead8d3b9eb37ae73b11e3c'
    hash = big_small_end_convert("1d1e201a5841479d30438e41b6e5e8c6780f28ecb5ead8d3b9eb37ae73b11e3c")
    print(di)
    print(hash)
    # txs = np.loadtxt('../Data_MultiNode_Testnet/pzy/TrainSet/testnet_tx_inv&recv_get_pzy.txt', delimiter=',',dtype='str')
    # label = np.loadtxt('../Data_MultiNode_Testnet/pzy/TrainSet/train_y_btc_testnet_pzy.txt', delimiter=',')
    # data = np.loadtxt('../Data_MultiNode_Testnet/pzy/TrainSet/testnet_inv&recv_get_pzy.txt', delimiter=',')
    # i=0
    # arrToDel=[]
    # while i< txs.shape[0]:
    #     if '000000' in txs[i][0]:
    #         print(i)
    #         arrToDel.append(i)
    #     i+=1
    # new_txs = np.delete(txs,arrToDel,axis=0)
    # new_label=np.delete(label,arrToDel,axis=0)
    # new_data=np.delete(data,arrToDel,axis=0)
    # np.savetxt("../Data_MultiNode_Testnet/pzy/TrainSet/New_testnet_tx_inv&recv_get_pzy.txt", new_txs, fmt='%s', delimiter=',')
    # np.savetxt("../Data_MultiNode_Testnet/pzy/TrainSet/New_train_y_btc_testnet_pzy.txt", new_label, fmt='%f', delimiter=',')
    # np.savetxt("../Data_MultiNode_Testnet/pzy/TrainSet/New_testnet_inv&recv_get_pzy.txt", new_data, fmt='%f', delimiter=',')
