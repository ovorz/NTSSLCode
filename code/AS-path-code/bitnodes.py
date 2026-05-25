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


db = pymysql.connect(host="118.25.12.97", user="gyl", password="150203", database="btc",
                     charset='utf8')
cursor = db.cursor()


def big_small_end_convert(data):
    return bytes.decode(binascii.hexlify(binascii.unhexlify(data)[::-1]))


def ts2t(ts):  # 时间戳转为时间
    timeArray = time.localtime(ts)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


Z_RPC_USER = 'zcashuser'
Z_RPC_PASSWORD = '123456'
Z_RPC_IP = '10.112.60.13'
Z_RPC_PORT = 8232
RPC_USER = 'btc'
RPC_PASSWORD = '123456'
RPC_IP = '10.112.60.13'
# RPC_IP = '127.0.0.1'
RPC_PORT = 8332
ES_IP = '10.108.23.179'
ES_PORT = 9200
TIMEOUT = 60
TX_INDEX = 'btc_tx_new'
DOC_TYPE = 'raw'


def ts2t(ts):  # 时间戳转为时间
    timeArray = time.localtime(ts)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


rpc_connection = AuthServiceProxy('http://%s:%s@%s:%d' % (RPC_USER, RPC_PASSWORD, RPC_IP, RPC_PORT))
z_rpc_connection = AuthServiceProxy('http://%s:%s@%s:%i' % (Z_RPC_USER, Z_RPC_PASSWORD, Z_RPC_IP, Z_RPC_PORT))

list_trans = []
es = Elasticsearch("%s:%d" % (ES_IP, ES_PORT))


def getAS(strSql):
    getASsql = "select ASN from bitnodes_list0113 where IpAddr='" + str(strSql) + ":8333'"
    try:
        cursor.execute(getASsql)
        result=cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        return -1

if __name__ == '__main__':
    ASs=[]
    nodesPerAs={}
    datetime.today()
    GetNodeInfo='https://bitnodes.io/api/v1/snapshots/latest/'
    # Traintxs = np.loadtxt('NTSSL_Txs_25%.txt', delimiter=',', dtype='str')
    re = requests.get(GetNodeInfo)
    re_nodelist = json.loads(re.text)
    # print(re_nodelist)
    totalnodes=re_nodelist['total_nodes']
    nodelist=re_nodelist['nodes']
    print(nodelist)
    sql = "insert into bitnodes_info_darkbee(IpAddr,ProtocolVersion,UserAgent,ConnectedSince,Services,Height,Hostname,City,CountryCode,Latitude,Longitude,Timezone,ASN,OrganizationName) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    count = "select ASN ,count(*) from bitnodes_list0113 group by ASN order by count(*) "
    getASsql="select * from bitnodes_list0113 where IpAddr="+''+":8333"

    # for tx in Traintxs:
    #     sql_cluster="select distinct txhash,cluster from tx_cluster_0112 where txhash = '{0}' ".format(str(tx))
    #     # print(sql_cluster)
    #     try:
    #         cursor.execute(sql_cluster)
    #         result = cursor.fetchall()
    #         print(result[0])
    #         sql_ = "select distinct txhash,cluster from tx_cluster_0112 where cluster = '{0}' ".format(str(result[0][1]))
    #         # print(sql_)
    #         cursor.execute(sql_)
    #         result = cursor.fetchall()
    #         print(len(result))
    #     except Exception as e:
    #         print(e)


#     try:
#         cursor.execute(count)
#         result=cursor.fetchall()
#         # print(cursor.fetchall())
#         for re in result:
#             ASN=str(re[0]).strip('AS')
#             nodesPerAs[ASN]=re[1]
#             if ASN:
#                 ASs.append(ASN)
#     except Exception as e:
#         print(e)
#     print(len(ASs))
# json_str = json.dumps(nodesPerAs)
# with open('NodesPerAs20220113.json', 'w') as json_file:
#     json_file.write(json_str)

    for node in nodelist:
        print(node)
        # print(nodelist[str(node)][0],nodelist[str(node)][1],nodelist[str(node)][2],nodelist[str(node)][3],nodelist[str(node)][4],nodelist[str(node)][5],nodelist[str(node)][6],nodelist[str(node)][7],nodelist[str(node)][8],nodelist[str(node)][9],nodelist[str(node)][10],nodelist[str(node)][11],nodelist[str(node)][12])
        # if nodelist[str(node)][11]!='TOR' and nodelist[str(node)][11] not in ASs and nodelist[str(node)][11]:
        #     try:
        #         ASs.append(nodelist[str(node)][11])
        #     except Exception as e:
        #         print(e)
        #         print(nodelist[str(node)][11])
            # print(node,nodelist[str(node)][5],nodelist[str(node)][7],nodelist[str(node)][11],nodelist[str(node)][12])
        try:
            cursor.execute(sql, (node,nodelist[str(node)][0],nodelist[str(node)][1],nodelist[str(node)][2],nodelist[str(node)][3],nodelist[str(node)][4],nodelist[str(node)][5],nodelist[str(node)][6],nodelist[str(node)][7],nodelist[str(node)][8],nodelist[str(node)][9],nodelist[str(node)][10],nodelist[str(node)][11],nodelist[str(node)][12]))
            db.commit()
        except Exception as e:
            db.rollback()
            print(e)
    # print(ASs,len(ASs))
    # fileObject = open('ASes20220113.txt', 'w')
    # for AS in ASs:
    #     r = ''.join(str(AS).strip('AS'))
    #     fileObject.write(r)
    #     fileObject.write('\n')
    # fileObject.close()

