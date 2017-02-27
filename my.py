# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
import time
import torndb
import requests
def database(fun, sql):
	try:
		db = torndb.Connection(host = "localhost", 
			database = "data",
			user = "root",
			password = "bm83147439",
			time_zone = "+8:00")
		if fun == 0:
			return db.query(sql)
		else:
			db.execute(sql)
			return 0
	except Exception as e:
		print sql + ' ERROR MSG0'
		print str(e) + ' ERROR MSG0'
		time.sleep(5)
		return database(fun, sql)
avid_list = []
av_not_change_count = {}
for each in database(0, 'select * from av'):
	avid_list.append(each['av_id'])
	av_not_change_count[each['av_id']] = {}
	av_not_change_count[each['av_id']]['last'] = 0
	av_not_change_count[each['av_id']]['count'] = 0
'''
detail+
t_id av_id view danmaku favorite coin share now_rank his_rank
av
av_id
'''
def insert_av(av):
	database(1, 'insert into av (av_id, time, mid, duration) values({0}, \'{1}\', {2}, {3})'.format(
		av['aid'] if str(av['aid']).isdigit() else 0,
		av['create'],
		av['mid'] if str(av['mid']).isdigit() else 0,
		av['duration'] if str(av['duration']).isdigit() else 0))
def insert_detail(av_id, detail):
	database(1, 'insert into detail (av_id, view, danmaku, favorite, coin, share, now_rank, his_rank) values({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7})'.format(
		av_id if str(av_id).isdigit() else 0, 
		detail['view'] if str(detail['view']).isdigit() else 0,
		detail['danmaku'] if str(detail['danmaku']).isdigit() else 0,
		detail['favorite'] if str(detail['favorite']).isdigit() else 0,
		detail['coin'] if str(detail['coin']).isdigit() else 0,
		detail['share'] if str(detail['share']).isdigit() else 0,
		detail['now_rank'] if str(detail['now_rank']).isdigit(),
		detail['his_rank'] if str(detail['his_rank']).isdigit()))
while True:
	#获取最新视频的id
	#tid = 24 AMD专区 14 单击联机 65 网游电竞
	start_time = time.time()
	getdata = {"type":"jsonp", "tid":24, "pn":1}
	headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	try:
		r = requests.get('http://api.bilibili.com/archive_rank/getarchiverankbypartion', params = getdata, headers = headers)
	except Exception as error:
		print str(error) + ' ERROR MSG1'
		time.sleep(10)
		continue
	r_data = eval(r.text)
	#一页20条记录
	for i in range(20):
		aid = r_data['data']['archives'][str(i)]['aid']
		if aid not in avid_list:
			avid_list.append(aid)
			insert_av(r_data['data']['archives'][str(i)])
			av_not_change_count[aid] = {}
			av_not_change_count[aid]['last'] = 0
			av_not_change_count[aid]['count'] = 0
	for each in avid_list: #可进行多进程优化
		getdata = {'aid':each}
		try:
			r = requests.get('http://api.bilibili.com/archive_stat/stat', params = getdata, headers=headers)
		except Exception as error:
			print str(error) + ' ERROR MSG2'
			time.sleep(1)
			continue
		r_data = eval(r.text)
		print str(each) + str(r.text)
		insert_detail(each, r_data['data'])
		if av_not_change_count[each]['last'] == r_data['data']['view']:
			av_not_change_count[each]['count'] += 1
			if av_not_change_count[each]['count'] >= 960: #三天内视频播放数为更新则删除
				avid_list.remove(each)
				del av_not_change_count[each]
		else:
			av_not_change_count[each]['last'] = r_data['data']['view']
	end_time = time.time()
	time.sleep(180-(end_time-start_time) if end_time - start_time < 180 else 1)
