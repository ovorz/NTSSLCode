import json
import random
import time
import numpy as np
import requests
import binascii
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import os
RPC_USER = 'btc'
RPC_PASSWORD = '123456'
RPC_IP = '118.25.12.97'
# RPC_IP = '127.0.0.1'
RPC_PORT = 8332
txs_positive = []
pzy_ip = '10.0.8.6'
gyl_ip='10.0.8.11'
# --------------读取主动交易-----------------
file_handler = open('../Data_MultiNode_Testnet/pzy/Mid_result/Self_Txs_pzy_1016.txt', mode='r')#
# 2.读取文件内容
contents = file_handler.readlines()
for msg in contents:
    msg = msg.strip('\n')  # 去除字符串中的\n
    txs_positive.append(str(msg))
file_handler.close()
#----------------------------
# -----计算连接数的比例
# inv_dst_ips=[]
# rs = os.path.exists('inv_dst_ips0111_Pt3.txt')
# if rs:
#     # 1.打开文件
#     file_handler = open('inv_dst_ips0111_Pt3.txt', mode='r')
#     # 2.读取文件内容
#     contents = file_handler.readlines()
#     for msg in contents:
#         msg = msg.strip('\n')  # 去除字符串中的\n
#         # split() 通过某个字符分割字符串,返回的是分割完成后的列表
#         # list_1 = msg.split(',')
#         inv_dst_ips.append(msg)
#     file_handler.close()
# partation_link = random.sample(inv_dst_ips, 12)
# print('patation:',len(partation_link))

def isBlockHash(str):
    if "00000" in str:
        return True
    return False
def my_obj_pairs_hook(lst):
    result = {}
    count = {}
    for key, val in lst:
        if key in count:
            count[key] = 1 + count[key]
        else:
            count[key] = 1
        if key in result:
            if count[key] > 2:
                result[key].append(val)
            else:
                result[key] = [result[key], val]
        else:
            result[key] = val
    return result


getdata_json = "D:/硕士/硕士学位管理/中期/多节点实验/原数据/node_pzy/btc_testnet_1016_getdata_pzy.json"  # 换成自己的路径
inv_json = "D:/硕士/硕士学位管理/中期/多节点实验/原数据/node_pzy/btc_testnet_1016_inv_pzy.json"

rpc_connection = AuthServiceProxy('http://%s:%s@%s:%d' % (RPC_USER, RPC_PASSWORD, RPC_IP, RPC_PORT))


def big_small_end_convert(data):
    return bytes.decode(binascii.hexlify(binascii.unhexlify(data)[::-1]))


with open(getdata_json, 'r', encoding='utf-8') as load_f:
    blocks = json.load(load_f, object_pairs_hook=my_obj_pairs_hook)
load_f.close()
with open(inv_json, 'r', encoding='utf-8') as load_inv:
    invs = json.load(load_inv, object_pairs_hook=my_obj_pairs_hook)
load_inv.close()
re_getdata = []
re_inv = []

def getHash(txid):
    time.sleep(4)
    url = "https://api.blockchair.com/bitcoin/testnet/raw/transaction/" + str(txid)
    r = requests.get(url, timeout=120)
    re = json.loads(r.text)
    return re['data']

print("---------------------------getdata------------------------")
print(len(blocks))
for block in blocks:#每一个block表示一个包
    # if block['_source']['layers']['ip']['172.17.0.4ip.dst'] == '172.17.0.4' and block['_source']['layers']['ip']['ip.src'] in partation_link:
    if block['_source']['layers']['ip']['ip.dst'] == pzy_ip:
        if isinstance(block['_source']['layers']['bitcoin'], list):
            for b in block['_source']['layers']['bitcoin']:
                # print(b)
                if b['bitcoin.command'] == 'getdata':
                    re_getdata.append(b)
        else:
            # print(block['_source']['layers']['bitcoin'])
            re_getdata.append(block['_source']['layers']['bitcoin'])

# print(re_getdata)
print("hits getdata:", len(re_getdata))
getdata_hash = []
getdata_origin = []
for re in re_getdata:
    if isinstance(re['bitcoin.getdata']['Inventory vector'], list):
        for vec in re['bitcoin.getdata']['Inventory vector']:
            getdata_hash.append(big_small_end_convert(str(vec['bitcoin.getdata.hash']).replace(':', '')))
            getdata_origin.append(str(vec['bitcoin.getdata.hash']))
    else:
        getdata_hash.append(big_small_end_convert(
            str(re['bitcoin.getdata']['Inventory vector']['bitcoin.getdata.hash']).replace(':', '')))
        getdata_origin.append(str(re['bitcoin.getdata']['Inventory vector']['bitcoin.getdata.hash']))
print("getdata_hash_num:", len(getdata_hash))
end_getdata = []
for hash in getdata_hash:
    i = 0
    for hash2 in getdata_hash:
        if hash == hash2:
            i += 1
    if [hash, i] not in end_getdata:
        end_getdata.append([hash, i])
print(end_getdata)
print(len(end_getdata))
differ_hash_data = []
differ_data = []
for single in end_getdata:
    # print(single[0])
    try:
        # the_tx = rpc_connection.getrawtransaction(single[0], True)
        the_tx = getHash(single[0])
        # print(the_tx[str(single[0])]['decoded_raw_transaction'])
        if len(the_tx)!=0:
            the_tx = the_tx[str(single[0])]['decoded_raw_transaction']['hash']
            if the_tx != single[0]:
                print("yes")
                differ_hash_data.append(the_tx)
                differ_data.append([single[0], the_tx])
            else:
                print("same")
        else:
            print("0,error", the_tx)
    except Exception as e:
        print("error:blockchair api 错误", single[0], e)
print('differ_data', differ_data)
print("---------------------------inv------------------------")
inv_hash = []
print(len(invs))
for inv in invs:
    # if inv['_source']['layers']['ip']['ip.src'] == '172.17.0.4' and 'bitcoin' in inv['_source']['layers'].keys() and inv['_source']['layers']['ip']['ip.dst'] in partation_link:
    if inv['_source']['layers']['ip']['ip.src'] == pzy_ip and 'bitcoin' in inv['_source']['layers'].keys():
        if isinstance(inv['_source']['layers']['bitcoin'], list):
            for i in inv['_source']['layers']['bitcoin']:
                if i['bitcoin.command'] == 'inv':
                    re_inv.append(i)
        else:
            re_inv.append(inv['_source']['layers']['bitcoin'])
print("hits inv:", len(re_inv))
for re in re_inv:
    if isinstance(re['bitcoin.inv']['Inventory vector'], list):
        for vec in re['bitcoin.inv']['Inventory vector']:
            inv_hash.append(big_small_end_convert(str(vec['bitcoin.inv.hash']).replace(':', '')))
    else:
        inv_hash.append(big_small_end_convert(
            str(re['bitcoin.inv']['Inventory vector']['bitcoin.inv.hash']).replace(':', '')))
print("inv_hash_num:", len(inv_hash))
end_inv = []
for hash in inv_hash:
    i = 0
    for hash2 in inv_hash:
        if hash == hash2:
            i += 1
    if [hash, i] not in end_inv:
        end_inv.append([hash, i])
print(end_inv)
print("origin:", len(end_inv))
differ = []
differ_hash = []
same = []
for single in end_inv:
    # print(single[0])
    try:
        # the_tx = rpc_connection.getrawtransaction(single[0], True)
        the_tx = getHash(single[0])
        if len(the_tx) != 0:
            the_tx = the_tx[str(single[0])]['decoded_raw_transaction']['hash']
            if the_tx != single[0]:
                print("yes")
                differ_hash.append(the_tx)
                differ.append([single[0], the_tx])
            else:
                print("same")
        else:
            # same.append([single[0], the_tx])
            print("0,error")
        # if re_tx['hash']!=single[0] and re_tx['hash'] in end_inv:
        #     print("txid：",single[0],"hash：",re_tx['hash'])
    except Exception as e:
        print("error1", single[0], e)
print("隔离见证交易：", differ)


def get_num(hash):
    num = 0
    for i in end_inv:
        if i[0] == hash:
            num = i[1]
    return num


def isDiffer(hash):
    for d in differ:
        if hash == d[0]:
            return True
    return False


def getHash(hash):
    for d in differ:
        if hash == d[0]:
            return d[1]
    return -1


def get_numData(hash):
    num = 0
    for i in end_getdata:
        if i[0] == hash:
            num = i[1]
    return num


def isDifferData(hash):
    for d in differ_data:
        if hash == d[0]:
            return True
    return False


def getHashData(hash):
    for d in differ_data:
        if hash == d[0]:
            return d[1]
    return -1


final = []
for hash in end_inv:
    n = 0
    if isDiffer(hash[0]):
        hash_ = getHash(hash[0])
        if hash_ != -1:
            n = hash[1] + get_num(hash_)
            final.append([hash[0], hash_, n])
    elif hash[0] not in differ_hash:
        final.append([hash[0], "none", hash[1]])
print("finalInv:", len(final))
final_getdata = []
for hash in end_getdata:
    n = 0
    if isDifferData(hash[0]):
        hash_ = getHashData(hash[0])
        if hash_ != -1:
            n = hash[1] + get_numData(hash_)
            final_getdata.append([hash[0], hash_, n])
    elif hash[0] not in differ_hash_data:
        final_getdata.append([hash[0], "none", hash[1]])
print("final_getdata:", len(final_getdata))
num_array = []
for e in final:
    i = 0
    for e1 in final:
        if e[2] == e1[2]:
            i += 1
    if [e[2], i] not in num_array:
        num_array.append([e[2], i])
print(num_array)
# -------------------写入--------------------------
# fileObject = open('getdata_1130.txt', 'w')
# for re in end_getdata:
#     r = ''.join(str(re))
#     fileObject.write(r)
#     fileObject.write('\n')
# fileObject.close()
# fileObject = open('inv_1130.txt', 'w')
# for re in end_inv:
#     r = ''.join(str(re))
#     fileObject.write(r)
#     fileObject.write('\n')
# fileObject.close()
# fileObject = open('finalinv_1130.txt', 'w')
# for re in final:
#     r = ''.join(str(re))
#     fileObject.write(r)
#     fileObject.write('\n')
# fileObject.close()
# fileObject = open('finalgetdata_1130.txt', 'w')
# for re in final_getdata:
#     r = ''.join(str(re))
#     fileObject.write(r)
#     fileObject.write('\n')
# fileObject.close()
# # -------------------读取--------------------------
# # 读取文件
# # Rtt_list = []
# # 判断文件是否存在，如果存在 再做打开文件的操作
# # 如果文件存在返回True 不存在 返回False
# # inv_list = []
# # rs = os.path.exists('end_inv.txt')
# # if rs:
# #     # 1.打开文件
# #     file_handler = open('end_inv.txt', mode='r')
# #     # 2.读取文件内容
# #     contents = file_handler.readlines()
# #     for msg in contents:
# #         msg = msg.strip('\n')  # 去除字符串中的\n
# #         # split() 通过某个字符分割字符串,返回的是分割完成后的列表
# #         list_1 = msg.split(',')
# #         inv_list.append(list_1)
# #     file_handler.close()
# # print(inv_list)
list = []
DaIn = []

def data_pro(data):
    A = -0.0001
    B = 0.0001  # 小数的范围A ~ B
    a = random.uniform(A, B)
    C = 10  # 随机数的精度round(数值，精度)
    return data + round(a, C)


info = []

target = []


def getdata():
    for f in final:
        for single in final_getdata:
            # print(single[0],inv)
            if f[0] == single[0] or f[1] == single[0]:
                print("train re:", single, f)
                try:
                    DaIn.append(f)
                    info.append(f)
                    if f[0] in txs_positive:
                        target.append(1)
                        # list.append(
                        #     [data_pro(f[2]), data_pro(single[2])])
                        list.append([f[2], single[2]])
                    else:
                        target.append(0)
                        list.append(
                            [f[2], single[2]])
                except:
                    print("error")
        if f not in DaIn:
            if f[0] in txs_positive:
                target.append(1)
                list.append(
                    [f[2], 0])
            else:
                list.append(
                    [f[2], 0])
                target.append(0)
            info.append(f)
    # print("DaIn:", DaIn)
    return list, info, target
# for i in getdata_origin:
#     print([big_small_end_convert(str(i).replace(':', '')),i])
if __name__ == '__main__':
    data1, info, target = getdata()
    lable = np.array(target)
    data = np.array(data1)
    np.savetxt("../Data_MultiNode_Testnet/pzy/train_y_btc_testnet_1016_pzy.txt", lable, fmt='%f', delimiter=',')
    np.savetxt("../Data_MultiNode_Testnet/pzy/testnet_inv&recv_get_1016_pzy.txt", data, fmt='%f', delimiter=',')
    print("list:", len(data1))
    info1 = np.array(info)
    np.savetxt("../Data_MultiNode_Testnet/pzy/testnet_tx_inv&recv_get_1016_pzy.txt", info1, fmt='%s', delimiter=',')
