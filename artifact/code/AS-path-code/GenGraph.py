import json
import os
import numpy as np
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
import operator
from functools import reduce
from itertools import chain
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

net_grid = nx.MultiDiGraph()
# plt.figure(figsize=(100, 100))
# -------------------读取--------------------------
# 读取文件
Rtt_list = []
# 判断文件是否存在，如果存在 再做打开文件的操作
# 如果文件存在返回True 不存在 返回False
inv_list = []
rs = os.path.exists('20220101.as-rel2.txt')#https://publicdata.caida.org/datasets/as-relationships/serial-1/
if rs:
    # 1.打开文件
    file_handler = open('20220101.as-rel2.txt', mode='r')
    # 2.读取文件内容
    contents = file_handler.readlines()
    for msg in contents:
        msg = msg.strip('\n')  # 去除字符串中的\n
        # split() 通过某个字符分割字符串,返回的是分割完成后的列表
        # list_1 = msg.split(',')
        inv_list.append(msg)
    file_handler.close()
# print(inv_list)
file_handler = open('ix-asns_202110.json', mode='r')
# 2.读取文件内容
ixps = []
contents = file_handler.readlines()
for msg in contents:
    msg = msg.strip('\n')  # 去除字符串中的\n
    # split() 通过某个字符分割字符串,返回的是分割完成后的列表
    # list_1 = msg.split(',')
    ixps.append(json.loads(msg))
file_handler.close()
print('ixp-asn:', len(ixps))
edges = []
nodes = []
for item in inv_list:
    as1 = item.split("|")[0]
    as2 = item.split("|")[1]
    type = item.split("|")[2]
    if int(type) == 0:
        tup = (int(as1), int(as2), 4)
        edges.append(tup)
        tup1 = (int(as2), int(as1), 4)
        edges.append(tup1)
    if int(type) == -1:
        tup = (int(as1), int(as2), 1)
        edges.append(tup)
        tup1 = (int(as2), int(as1), 8)
        edges.append(tup1)

for ixp in ixps:
    edges.append((str(ixp['ix_id']) + 'ixp', ixp['asn'], 2))
    edges.append((ixp['asn'], str(ixp['ix_id']) + 'ixp', 2))

# 计算IXP中AS的个数
# as_in_ixp = []  # 每个ixp中的成员AS
ixp_num = []  # 所有IXP
# total_memberAS = []  # 所有AS

for ixp in ixps:
    if ixp['ix_id'] not in ixp_num:
        ixp_num.append(ixp['ix_id'])
# for ixp1 in ixp_num:
#     for ixp2 in ixps:
#         if int(ixp2['ix_id']) == ixp1:
#             as_in_ixp.append(ixp2['asn'])
#     # print(ixp1, as_in_ixp)
#     total_memberAS.append(as_in_ixp)
#     as_in_ixp = []
print('ixp',len(ixp_num))
# print(len(total_memberAS))

# 增强型拓扑-计算路径
# ArguedPaths = []
# i = 0
# while i < len(total_memberAS):
#     for as1 in total_memberAS[i]:
#         for as2 in total_memberAS[i]:
#             if int(as1) != int(as2):
#                 edges.append((as1, as2, 4))
#     i += 1
#     print(i)
# print('edge_num:', len(list(set(edges))))
# edges = list(set(edges))
ASs = []
file_handler = open('ASs.txt', mode='r')
# 2.读取文件内容
contents = file_handler.readlines()
for msg in contents:
    msg = msg.strip('\n')  # 去除字符串中的\n
    # split() 通过某个字符分割字符串,返回的是分割完成后的列表
    # list_1 = msg.split(',')
    ASs.append(int(msg))
file_handler.close()
# nodes
list_net_nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# edges
list_net_edges = [(1, 3), (3, 5), (5, 4), (4, 2), (2, 6),
                  (5, 7), (5, 8), (8, 6),
                  (7, 9), (8, 9), (6, 10),
                  (9, 11), (10, 12), (10, 13),
                  (11, 14), (12, 14), (12, 15),
                  (14, 16), (15, 16), (15, 17),
                  (16, 18), (17, 19), (12, 2), (12, 1),
                  (18, 20), (19, 7), (19, 2), (19, 1), (19, 5), (7, 19)]
# net_grid.add_nodes_from(list_net_nodes)
net_grid.add_weighted_edges_from(edges)
# pos = nx.circular_layout(net_grid)  # 随机分布
# nx.draw_networkx_nodes(net_grid, pos=pos, node_color='#ff0000', node_size=150, alpha=0.6)  # 点的样式
# nx.draw_networkx_edges(net_grid, pos=pos, width=0.5, alpha=0.4)  # 边的样式
# nx.draw(net_grid, with_labels=True, node_size=400, node_color='#ff0000', pos=pos)
# plt.savefig("plot.pdf")
# plt.show()
# 计算AS之间路径
AllPaths = {}
BitNodesPath = {}
SingleSrc = []
for AS in ASs:
    try:
        # print(nx.shortest_path(net_grid, source=AS,weight='weight'))
        # print(nx.shortest_path_length(net_grid, source=AS,weight='weight'))
        AllPaths[AS] = nx.shortest_path(net_grid, source=AS, weight='weight')
        for AS1 in AllPaths[AS].keys():
            try:
                SingleSrc.append(AllPaths[AS][AS1])
                # print(AllPaths[AS][AS1])
            except Exception as e:
                print('e2', e)
    except Exception as e:
        print('e1', e)
    BitNodesPath[AS] = SingleSrc
    print('yes', AS)
    SingleSrc = []
#
json_str = json.dumps(BitNodesPath)
with open('BitNodesPath_withIXP2021_all.json', 'w') as json_file:
    json_file.write(json_str)
print('Finished')


# #根据比例筛选中间人AS
with open('BitNodesPath_withIXP2021.json', 'r', encoding='utf-8') as load_path:
    Paths = json.load(load_path, object_pairs_hook=my_obj_pairs_hook)
load_path.close()

with open('NodesPerAs.json', 'r', encoding='utf-8') as load_path:
    NodesPerAs = json.load(load_path, object_pairs_hook=my_obj_pairs_hook)
load_path.close()
temp = {}
re = {}
AS_temp = []
MiTM = []
idx=[]
for AS in ASs:
    # arc=np.array(Paths[str(AS)])
    total = list(chain(*Paths[str(AS)]))#图一：首先遍历每一个自治域A_from，计算该自治域与其他自治域之间的路径(allpaths，
    # ，计算路径中出现的自治域A_mid的次数进行统计并降序排序，越靠前说明经过该自治域的路径越多，计算这些路径中有多少路径(paths)同时经过一个自治域A_mid，计算比例path/allpaths;如果path/allpaths>=25%,那么计算A_from中包含的节点数量nodes,即存在自治域A，对于
    #node个节点，A_mid可以劫持其25%的连接,统计所有符合这种条件的A_from_sum,并计算所包含的节点数量总和node_sum
    #图二：计算所有自治域之间的路径all_path，并计算所有路径中出现的中间人自治域A_mid的次数进行统计并降序排序，越靠前说明经过该自治域的路径越多，那么该自治域能够劫持的域间连接越多，计算经过自治域A_mid的数量num_A_mid,比上所有域间连接的数量num_all_path,即为该自治域A_mid能够劫持的网络中连接的比例。
    # print(Counter(total))
    try:
        idx1 = list(Counter(total))[0]
        idx2 = list(Counter(total))[2]
        # if 0.1 <= float(Counter(total)[idx2] / Counter(total)[idx1]):
        #     print(Counter(total)[idx2], Counter(total)[idx1], idx2)
        AS_temp.append(AS)
        # AS_temp.append(idx2)
        MiTM.append(idx2)
    except Exception as e:
        print('error', e)

total_count=[]
i = 0
intercept_nodes = 0
count1=[]
count2=[]
count3=[]
count4=[]
while i < len(AS_temp):
    for As_path in Paths[str(AS_temp[i])]:
        try:
                if MiTM[i] in As_path:
                    intercept_nodes += NodesPerAs[str(As_path[-1])]
        except Exception as e:
            print(e)
    total_count.append(intercept_nodes)
    print(max(total_count))
    # if intercept_nodes >= 2220:#按照25%，50%，75%，100%的比例，计算节点的数量
    #     count1.append(AS_temp[i])
    #     count1.append(MiTM[i])
    #
    # if intercept_nodes >=3700:
    #     count2.append(AS_temp[i])
    #     count2.append(MiTM[i])
    #
    # if intercept_nodes >=5180:
    #     count3.append(AS_temp[i])
    #     count3.append(MiTM[i])
    #
    # if intercept_nodes >=6660:
    #     count4.append(AS_temp[i])
    #     count4.append(MiTM[i])
    i += 1
    intercept_nodes = 0
# print('AS_num',len(list(set(count))))
# num_node = 0
# i=0
# for count in [count1,count2,count3,count4]:
#     for asn in list(set(count)):
#         try:
#             num_node += NodesPerAs[str(asn)]
#         except:
#             continue
#     print('node_num:',float(num_node/7400))
#     i+=1
#     num_node=0
