# -*- coding:utf-8 -*-
# configuration
import os 
# import generator
# resp = generate()
# print resp.text
#def gee():
	# os.system('sh /Users/xuejun/Downloads/flask-for-data-science-master/load.sh')
#l= gee()



# RANGE_ARGS = 200
# RADIUS_ARGS = 10
# os.system('sh /Users/xuejun/Downloads/flask-for-data-science-master/load.sh %d %d' %(RANGE_ARGS,RADIUS_ARGS))

# SPARK_METHOD = os.system('sh /Users/xuejun/Downloads/flask-for-data-science-master/load.sh %d %d' %(RANGE_ARGS,RADIUS_ARGS))
# print SPARK_METHOD 
import urllib
import shelve
import datetime
from datetime import timedelta
# RFM_PATH="/Users/xuejun/Downloads/predPaths_test.txt"
# link_close = []
# id_list = {}
# for line in urllib.urlopen(RFM_PATH):
#     res = line.strip().split(',')  
#     tem = []
#     tem.append(res[1])
#     if res[0] in id_list:
#         id_list[res[0]] += 1
#     else:
#         id_list[res[0]] = 1
#     tem.append(id_list[res[0]])
#     tem.append(res[2])
#     tem.append(res[3])
#     tem.append(res[4])
#     tem.append(datetime.datetime.strptime(res[5],'%Y/%m/%d %H:%M:%S').strftime('%Y/%m/%d %H:%M:%S'))
#     link_close.append(tem)

# FIRST_FILE = '/Users/xuejun/Downloads/flask-for-data-science-master/guestbook.dat'
# base = shelve.open(FIRST_FILE)
# if 'first_list' not in base:
#     first_list = []
# else:
#     # 从数据库获取数据
#     first_list = base['first_list']
# # 将提交的数据添加到表头
# for each in link_close[:1000]:
#     first_list.insert(0, {
#         'id': each[0],
#         'taxi_id': each[1],
#         'lng': each[2],
#         'lat': each[3],
#         'user':each[4],
#         'create_at':each[5],
#     })
# # 更新数据库
# base['first_list'] = first_list

# first_list = base.get('first_list', [])[:10]
# print first_list
# greeting_list = base.get('greeting_list',[])
# print greeting_list

# if 'first_table' not in base:
#         first_table = []
# else:
#     # 从数据库获取数据
#     first_table = base['first_table']
#     # 将提交的数据添加到表头
# first_table.insert(0, {
#     'table_range': 15,
# })
#     # 更新数据库
# base['first_table'] = first_table
# first_list = base.get('first_table', [])
# base.close()

# print first_list[0]['']


#second_list
RFM_PATH="/Users/xuejun/Downloads/predPaths_test.txt"
second_close = []
id_list = {}
for line in urllib.urlopen(RFM_PATH):
    res = line.strip().split(',')  
    tem = []
    tem.append(res[1])
    if res[0] in id_list:
        id_list[res[0]] += 1
    else:
        id_list[res[0]] = 1
    tem.append(id_list[res[0]])
    tem.append(res[2])
    tem.append(res[3])
    tem.append(res[4])
    tem.append((datetime.datetime.strptime(res[5],'%Y/%m/%d %H:%M:%S')+timedelta(days=400)).strftime('%Y/%m/%d %H:%M:%S'))
    second_close.append(tem)

FIRST_FILE = '/Users/xuejun/Downloads/flask-for-data-science-master/guestbook.dat'
base = shelve.open(FIRST_FILE)
if 'second_list' not in base:
    second_list = []
else:
    # 从数据库获取数据
    second_list = base['first_list']
# 将提交的数据添加到表头
for each in second_close[1000:2000]:
    second_list.insert(0, {
        'id': each[0],
        'taxi_id': each[1],
        'lng': each[2],
        'lat': each[3],
        'user':each[4],
        'create_at':each[5],
    })
# 更新数据库
base['second_list'] = second_list

sec_list = base.get('second_list', [])[:10]
print sec_list