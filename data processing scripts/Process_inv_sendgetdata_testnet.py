import json
import random
import time
import numpy as np
import requests
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import plistlib
import sys
import binascii
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import os

RPC_USER = 'btc'
RPC_PASSWORD = '123456'
RPC_IP = '118.25.12.97'
# RPC_IP = '127.0.0.1'
RPC_PORT = 8332
txs_positive = []
file_handler = open('Txs_Positive_0113.txt', mode='r')
# 2.读取文件内容
contents = file_handler.readlines()
for msg in contents:
    msg = msg.strip('\n')  # 去除字符串中的\n
    # split() 通过某个字符分割字符串,返回的是分割完成后的列表
    # list_1 = msg.split(',')
    txs_positive.append(str(msg))
file_handler.close()
txs0630_test = ['31b3a79bc207aaf434348137512c9e632415e6066c298c952f7bc4c9301ec48c',
                '07e6303871452d52e065ec4f244665fe41840ea85b486e422a903772efd3078b',
                '6b443509d4d488d62215431cf6f242e6a3093549755761c39047c891d8c17ae3',
                '90f68958d63b5a45f1b01178f5e0adca28caac7f42f1de18d544307261299b77',
                'e80def0b0acf61a0f49dd00c3e35c4acf9bf2eafd627f6916ce29dab1bc039e1',
                '8c23902cd23ffd65e58fd82e2ad254f363bd856ce2295227cf28892c4e1b01da',
                'e284a771f9494eb3a497d35db2527cf25f00e45def1586c7c34b7d647ccc6846',
                'f044caa0d6670c0d938a94fc97dc21befa1684a21c0789c8eb4d2b2f97c04bc0',
                'cd08159b359a638ab976f1fa791b75c64ef8e38b7f29c4a3c3e6214ce1669928',
                '71d948dfb35e7486212bb509196b404472806fbd09588a9177be56393e49f30d',
                '9c59017997bbb399fcfe4d4961f7d807c3872ab0c54e9006d48640c1ca473b13',
                'b90bb786ab297f3696f564901891592bc68e6a30f0c42223bacee667e0b15e88',
                '8dc8bbbb05fd2914d95f8ab579e11b9e4f0eeb289e477efc9b41ef9517ddfbe8',
                'c77e28767d7a571c15b2057299704c0c757145b8614d677042910b2f998eba95',
                '7a994e08a7714a0502eaf12fe79058455c15802d4327ea433750e8ed550808f6',
                'b66cd125f7d61fbdea4197f9eac9b627a59787b206d2cf3902d9c468cd4f446b',
                'c91fd5d568ef494c6bef6d6a7f0c86ad7105c74090e95165dfebfdf3a450ce55',
                'c632e1fc5840297bfb77203316f9f740bf053203410d90b9ca5a7e572473b49f',
                '75e93b3fc0e5f6602f0d46713e76cd3460f797e3dbb78d4e60f7df7ba43aba7d',
                'a832cdda901624bb47321e567a550d7c67242b5fa10b53cdfcba941dc59c2e60',
                '91ba317b07134bdad5180430304d3d38a4b2609e5d45b451504ff94dcd654b2f',
                '55f22e85d5b5d2e7aab4924852db5eab54bd9a5c47074eefc3a24adde8495be2',
                '7b3d1ad5ef2c488b89334673b4a577456b0ab1a8483664879ff3ebdb03719fb7',
                'b009cc8123da0376c68d8ae1d1e96c1717927d04713c3b93413ae1a32b272ff2']
txs0424 = ['c271e489879a737083e00b5d3975cb1574bd9abc01db317166ba1d45f5bf1c9f',
           '49efb2b66bb0d7e94d7d2ca9f72379878410150d2ee4f3c809bcd59235f4e436',
           '866e6a76054d28cc0c970be735f85dba9a88db91c65e1403f3338ded7cffb66a',
           'dcac84a112abd7daa4076a96bfd7bc9f2efb562660a6330ab03de72f15153189',
           '22919d4b75955d652af4ff4db5ca76a1beb75b9fd888da68f5fa7da85b8fb771',
           '7b93a7a8963360ce890fac6b8464cf837f5f109d9ea985887f50e96b6bb07ea6',
           '8be833a2ba0e676722d1e73ef12cc98533cc804ddd97c18d5c65f75cf34bfa84',
           '04d9dbabf205e355c743ffd8d1ce2e3ee06142b1c98e102e88adb70efb1f2c31',
           '916bd8a8c72b0a15d1f04e1d977020605e57aaabd89de8f4b69c99651f1e9a07',
           '1c1430e080ac62955fb566a1099cc57889df536575b15d5ff72888c5c7802161',
           '14e137d3e5444a8161b1bdf4a18e475c168f8b51aa5a0dac7a1945c6b4c42fea',
           'ca422753ebddbeaa7fe02e76186859d7ec587dd8d7655b801419861df9d87b07',
           '8b0f386b53317cec5fb806b8fb0195a92d61b689f5a10ae616c7870dd90a0456']
txs = ['d8da1920d1cbb2a5f3f255ae56a46ea39a38d28abb7d2faa60933faf2789db7e',
       '6967bdf6c14181be4b494fb9d9465a92714694798ed3a50b6b39ba9ac4608126',
       '136d865c671a2a7fc6dd26b426f1eb51932be977b3862067a53ef5dea75ffcb8',
       '2ea379a946b45f44cb3300845f2087c5ff84ce04f643bac87ee73cb8406dc75f',
       'cd152c20484a217b7042ef9a72d068af12e21101649f162bd2c93a432c6c58d7',
       '5807cad7cf59751012a455436ae977b3e66f58742887b3b8b3e3a65a9b89dd05',
       '2be8ec2d4942f3f474db3917ab5a1a9b20b7e8db3ba15efbe849cdea676fa136',
       '2b8c6fe4b8230578cbcdd5e3258f799d78bde615f123b8b35d3729a52293ab71',
       'b55ba590d370741d1caef545b7676f06696aac5bee6106c06143905017af83a9',
       '19c654b48ff7b09b09b92684187b1d5d13c81f46b2f0912190e703faf5c311a4']
tx0517 = ['f6e9eb324b8a3736b70301290e927080495379043b24043a28dcb462910211e5',
          '1eb701cb25d3ef8ecf32c869ea4ee9be5810cec938c532ff0908d061b19ccbf2',
          '1e6aab1e56d5d587f79d1356ac7891b5ff21a8c4e474eca42fb1a4d66f8a6fcb',
          '460e03d5b57c77035af0a141b831334cdb84855ed1f9ac3a0da2925cf4e48055',
          '713642674dd32cd38ceef3dae6966d1cfe84890d6b231c42863878b0636e7734',
          '1c549730d0d1f0aaf80789ec89866d8733dc172d4ed30ee68f99dce33126ec59',
          'aba3b6d1273904dfa6ec69d4494e4290f80eb3dffd7642e9d741935f5e8b7b53',
          'e8c52429ca7d331ae5f81a037bb74291f5b4369a90b7398c6cc55687200b6fa4',
          '51f5ae7cb4f87b0f23a7cc982c48c1314d1d179cb2d25085d31abd61e7b5ce3d',
          '3e0bfefec63bd00cd1e7aeec79e293ed74f1b34719597aff23674d84fa49aacd',
          'cc2d3ecb545815243545937808f51f2dde89dff0c6fc26b0fac031dc5cea5f26',
          '230a634d799d6b9f7ab4fcbc2173bfc137a91bac1f5e55a87ffc4ca2892f1939',
          '137df41bd9ef30a35ebf1ca3ac99f13e187a4ee6fa71d9b42b5ae6826a83efd3',
          'a5a5d3f50bfd94f2d66b31c9266025e3a601de949fa9c0856410a2f1e9a134a1',
          '643aeafeafb08b6c8ded64d15b30a886a067ac410a62ba76301a3463794f1a38',
          '30cbb9fd377c15f0801df93fff3370dabf7116f4b2c4d76549fcd79e2fd0ffa9',
          '28ff44c3b4d7e3673758b93144157469bdc7d2f02a87577ad1a2790ee918afee',
          'f94e96d3e6fcccbd0114311fe9a25c403e8b409aa8368fdfc61b4eb17c7d0cad',
          '70f9045ede50211bcf67495c391188519d3f51bc51aec9ca59d59583bdec61df',
          '69b2d888a28dce996953c62988b0e21eac62d14cb44af5097ede31c70b10d874',
          'd4ed902c7c9d3e77f73554f66c928697d2af7d847e9d81f60afa890e6f31b18a',
          '74930ca4e9ae94ebb50e73d05ad6357e8cf89d718bd8296b684108f8f4e1c776',
          'be6878601d885712a8a0349eb52b960f5095cda6a4768775b5d1c65fe27bb7b8',
          'dce55054756717bd35cadfe355ad3052c77850bb089db20f28eaf342a26746f3',
          '6d3b6f20d11245a9ea9cdcceccab84aab358acd5cca9cb6e440708d08641a38e',
          'c32e1dffb521a402c62d905158a90ac605f72baf933c0a4774dfbff187982710',
          '1860e8c8a951932330b461aa29be0dd807df5083a309c74048ed4d122220c605',
          '7a6ad300fe39e2a24aefd2fb28cbb1a59493dd151445d46cb38adfce714bd1a',
          '88ad48513b828bd63ebff91f8bf92dc278049de6edcea9289b3384d965b58247',
          'f3239f340617b84cd5144addb9dbe129e44fde432e93fbe8b215a4b4db236504',
          '55b0fe420bc61e09c621da2fca949b96650f25f02c8703a532382423807e4ef3',
          '41fdcde7bfd8f5ffaba2d57d6d086f0b23aaec9064aeabda310c4fbbe5d65648',
          'e5416f8019d20f6d086ba4fe72ec75a554d884259066b3937a44d32531030e4d',
          '7dcd7775283e33a1f543e730834ff4558a903c37cd8f7a0b317562e212462468',
          '3bfe605b9af3164b1191be48944de5e3502ceecb9bd3e796196e9b0bf11d9fed',
          'b0c467c5bb87bfd1b12c2ce4de138f6298fccd5ce75ce19d23dfae1eb7e14da4',
          '40a63a1464ec947a9b0fedf37584239a5b47ba04bcd43400de313a64170511f1',
          '0c90345e1193a968ca8511501ceeb6c4b4b4a75b2fe9a79b795435baec7f307d',
          'a4901ebaf237bb6b3b3bb37b6e159b6bfd93c9aaeb2cca632bdb873376accc95',
          '3cbc45599b62dda41dbc1a53ec7f46fced9fb646db17ea19184458d989a30ccf',
          '749f5ee157847d240ddb636205c43e9ea7bf37ba862dc0032cd4b74684cd6bd3',
          'c662d983122dbc8a205beccd3ff267ed16b7e4bf47fa56e470bf2b8bb2d7ceaa']
tx0517part = ['f6e9eb324b8a3736b70301290e927080495379043b24043a28dcb462910211e5',
              '1eb701cb25d3ef8ecf32c869ea4ee9be5810cec938c532ff0908d061b19ccbf2',
              '1e6aab1e56d5d587f79d1356ac7891b5ff21a8c4e474eca42fb1a4d66f8a6fcb',
              '460e03d5b57c77035af0a141b831334cdb84855ed1f9ac3a0da2925cf4e48055',
              '713642674dd32cd38ceef3dae6966d1cfe84890d6b231c42863878b0636e7734',
              '1c549730d0d1f0aaf80789ec89866d8733dc172d4ed30ee68f99dce33126ec59',
              'aba3b6d1273904dfa6ec69d4494e4290f80eb3dffd7642e9d741935f5e8b7b53',
              'e8c52429ca7d331ae5f81a037bb74291f5b4369a90b7398c6cc55687200b6fa4',
              '51f5ae7cb4f87b0f23a7cc982c48c1314d1d179cb2d25085d31abd61e7b5ce3d',
              '3e0bfefec63bd00cd1e7aeec79e293ed74f1b34719597aff23674d84fa49aacd',
              'cc2d3ecb545815243545937808f51f2dde89dff0c6fc26b0fac031dc5cea5f26',
              '230a634d799d6b9f7ab4fcbc2173bfc137a91bac1f5e55a87ffc4ca2892f1939',
              '137df41bd9ef30a35ebf1ca3ac99f13e187a4ee6fa71d9b42b5ae6826a83efd3',
              'a5a5d3f50bfd94f2d66b31c9266025e3a601de949fa9c0856410a2f1e9a134a1',
              '643aeafeafb08b6c8ded64d15b30a886a067ac410a62ba76301a3463794f1a38',
              '30cbb9fd377c15f0801df93fff3370dabf7116f4b2c4d76549fcd79e2fd0ffa9',
              '28ff44c3b4d7e3673758b93144157469bdc7d2f02a87577ad1a2790ee918afee',
              'f94e96d3e6fcccbd0114311fe9a25c403e8b409aa8368fdfc61b4eb17c7d0cad',
              '70f9045ede50211bcf67495c391188519d3f51bc51aec9ca59d59583bdec61df',
              '69b2d888a28dce996953c62988b0e21eac62d14cb44af5097ede31c70b10d874',
              'd4ed902c7c9d3e77f73554f66c928697d2af7d847e9d81f60afa890e6f31b18a', ]


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


getdata_json = "/home/disk1/tcy/mainnet_0113_tencent/btc_main_0113_getdata_send.json"  # 换成自己的路径
inv_json = "/home/disk1/tcy/mainnet_0113_tencent/btc_main_0113_inv_send.json"

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
for block in blocks:
    if block['_source']['layers']['ip']['ip.src'] == '172.17.0.4':
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
        the_tx = rpc_connection.getrawtransaction(single[0], True)
        # the_tx = getHash(single[0])
        if the_tx:
            the_tx = the_tx['hash']
            if the_tx != single[0]:
                print("yes")
                differ_hash_data.append(the_tx)
                differ_data.append([single[0], the_tx])
            else:
                print("same")
        else:
            print("0,error", the_tx)
    except Exception as e:
        print("error2", single[0], e)
print('differ_data', differ_data)
print("---------------------------inv------------------------")
inv_hash = []
print(len(invs))
for inv in invs:
    if inv['_source']['layers']['ip']['ip.src'] == '172.17.0.4'  and 'bitcoin' in inv['_source']['layers'].keys():
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
        the_tx = rpc_connection.getrawtransaction(single[0], True)
        # the_tx = getHash(single[0])
        if the_tx:
            the_tx = the_tx['hash']
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
    np.savetxt("train_y_inv&send_get0113.txt", lable, fmt='%f', delimiter=',')
    np.savetxt("testnet_inv&send_get0113.txt", data, fmt='%f', delimiter=',')
    print("list:", len(data1))
    info1 = np.array(info)
    np.savetxt("testnet_tx_inv&send_get0113.txt", info1, fmt='%s', delimiter=',')
