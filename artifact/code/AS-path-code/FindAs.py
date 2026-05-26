import json
import random
import binascii
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import os

# from bitnodes import getAS

pzy_ip='10.0.8.6'
tcy_ip='10.0.4.16'
gyl_ip='10.0.8.11'
RPC_USER = 'btc'
RPC_PASSWORD = '123456'
RPC_IP = '101.43.124.195'
RPC_PORT = 8332

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


getdata_json = "E:/多节点实验/jsons/btc_mainnet_pzy_0221_Pt2_getdata.json"  # 换成自己的路径
inv_json = "E:/多节点实验/jsons/btc_mainnet_pzy_0221_Pt2_inv.json"

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
getdata_src_ip=[]
inv_dst_ip=[]
print("---------------------------getdata------------------------")
print(len(blocks))
for block in blocks:
    if block['_source']['layers']['ip']['ip.dst'] == pzy_ip and  'bitcoin' in block['_source']['layers'].keys():
        if isinstance(block['_source']['layers']['bitcoin'], list):
            for b in block['_source']['layers']['bitcoin']:
                if b['bitcoin.command'] == 'getdata':
                    getdata_src_ip.append(block['_source']['layers']['ip']['ip.src'])
        else:
            getdata_src_ip.append(block['_source']['layers']['ip']['ip.src'])
print("getdata_src_ip：", len(list(set(getdata_src_ip))))
print("---------------------------inv------------------------")
inv_hash = []
print(len(invs))
for inv in invs:
    if inv['_source']['layers']['ip']['ip.src'] == pzy_ip and  'bitcoin' in inv['_source']['layers'].keys():
        if isinstance(inv['_source']['layers']['bitcoin'], list):
            for i in inv['_source']['layers']['bitcoin']:
                if i['bitcoin.command'] == 'inv':
                    inv_dst_ip.append(inv['_source']['layers']['ip']['ip.dst'])
        else:
            inv_dst_ip.append(inv['_source']['layers']['ip']['ip.dst'])
print("inv_dst_ips:",list(set(inv_dst_ip)),len(list(set(inv_dst_ip))))

fileObject = open('../../Data_MultiNode_Mainnet/pzy/100%/inv_dst_ips/mainnet_pzy_inv_dst_ips0221_Pt2.txt', 'w')
for ip in list(set(inv_dst_ip)):
    r = ''.join(str(ip))
    fileObject.write(r)
    fileObject.write('\n')
fileObject.close()
