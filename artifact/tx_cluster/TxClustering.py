import json
import time
from datetime import datetime
from datetime import timedelta
from elasticsearch import Elasticsearch
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
# -*- coding = utf-8 -*-
import requests
import binascii
import pymysql
import numpy as np

db = pymysql.connect(host="101.43.124.195", user="root", password="bupt2021", database="btc",
                     charset='utf8')
cursor = db.cursor()


def big_small_end_convert(data):
    return bytes.decode(binascii.hexlify(binascii.unhexlify(data)[::-1]))


def ts2t(ts):  # 时间戳转为时间
    timeArray = time.localtime(ts)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


RPC_USER = 'btc'
RPC_PASSWORD = '123456'
RPC_IP = '10.112.60.13'
# RPC_IP = '127.0.0.1'
RPC_PORT = 8332


def ts2t(ts):  # 时间戳转为时间
    timeArray = time.localtime(ts)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


rpc_connection = AuthServiceProxy('http://%s:%s@%s:%d' % (RPC_USER, RPC_PASSWORD, RPC_IP, RPC_PORT))

list_trans = []


def getAS(strSql):
    getASsql = "select ASN from bitnodes_list0113 where IpAddr='" + str(strSql) + ":8333'"
    try:
        cursor.execute(getASsql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        return -1


def GetTxcluster(txid):
    url = 'http://www.walletexplorer.com/api/1/tx?txid=' + txid + '&caller=songyuc@bupt.edu.cn'
    re = requests.get(url)
    re_json = json.loads(re.text)
    # print(re_json)
    return re_json['wallet_id']


def GetTestLabel(result, txid):
    print(txid)
    for re in result:
        if re[0] == txid:
            # print(re[1])
            return re[1]


def GetTxCulsterFromDB(txid):
    sql = "select cluster_id from tx_cluster_1210 where tx_id = '{0}'".format(str(txid))
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        if result!=():
            return result[0][0]
        else:
            return -1
    except Exception as e:
        print(e)

if __name__ == '__main__':
    ASs = []
    nodesPerAs = {}
    datetime.today()
    GetNodeInfo = 'https://bitnodes.io/api/v1/snapshots/latest/'
    # TestSettxs = np.loadtxt('../MainnetExperiment/100%/TestSet/main_tx_inv&recv_get_tcy_1121_Pt2_100%.txt',
    #                         delimiter=',', dtype='str')
    TestResult = np.loadtxt('../Data_MultiNode_Mainnet/gyl/100%/TestSet/TestResult_gyl_1210.txt', delimiter=',', dtype='str')
    sql = "select count(*),cluster_id from tx_cluster_1210 group by cluster_id order by count(*) desc "
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    dic = {}
    for re_cluster in result:
        arr = []
        sql = "select tx_id from tx_cluster_1210 where cluster_id = '{0}'".format(str(re_cluster[1]))
        try:
            cursor.execute(sql)
            result_tx = cursor.fetchall()
            # print(result)
            for re in result_tx:
                label = GetTestLabel(TestResult, re[0])
                arr.append(label)
        except Exception as e:
            print(e)
        print(arr)
        dic[str(re_cluster[1])] = arr
    sql_get_cluster_group = ""
    tx_lost = []
    print(dic)
    filename = "cluster_label_100%_gyl_1210.json"
    with open(filename, 'w') as file_obj:
        json.dump(dic, file_obj)

    New_label = []
    for tx in TestResult:
        cluster_id = GetTxCulsterFromDB(tx[0])
        if cluster_id != -1 and str(cluster_id) in dic.keys():
            label_array = dic[str(cluster_id)]
            if(str(label_array).count("0")>str(label_array).count("1")):
                New_label.append(0)
            elif(str(label_array).count("0")<str(label_array).count("1")):
                New_label.append(1)
            else:
                New_label.append(int(tx[1]))
            # print(label_array,str(label_array).count("1"),str(label_array).count("0"))
        else:
            New_label.append(int(tx[1]))

    print(New_label,len(New_label))
    np.savetxt("Cluster_train_y_inv&recv_get_gyl_1210.txt", np.array(New_label),
               fmt='%f',
               delimiter=',')