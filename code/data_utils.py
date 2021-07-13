import tushare as ts
import pandas as pd
import os
import time
import glob

# tushare 验证token


# ----------------------下载某只股票数据------------------- #
# code:股票编码 日期格式：2019-05-21 filename：写到要存放数据的根目录即可如D:\data\
# length是筛选股票长度，默认值为False，既不做筛选，可人为指定长度，如200，既少于200天的股票不保存
def get_stock_data(code, date1, date2, filename, length=-1):
	df = ts.get_hist_data(code, start=date1, end=date2)
	df1 = pd.DataFrame(df)
	df1 = df1.sort_values(by='trade_date')
	df1 = df1[['trade_date','open', 'high', 'close', 'low', 'vol', 'change']]
	print('共有%s天数据' % len(df1))
	if length == -1:
		path = code + '.csv'
		df1.to_csv(os.path.join(filename, path))
	else:
		if len(df1) >= length:
			path = code + '.csv'
			df1.to_csv(os.path.join(filename, path),index=False)


# ----------------------下载某只股票逐天数据------------------- #
def get_stock_data_daily(pro,code, date1, date2, filename, length=-1):
	df = pro.daily(ts_code=code, start_date=date1, end_date=date2)
	df1 = pd.DataFrame(df)
	df1 = df1.sort_values(by='trade_date')
	df1 = df1[['trade_date','open', 'high', 'close', 'low', 'vol', 'change']]
	if length == -1:
		path = code + '.csv'
		print(code,'共有%s天数据' % len(df1))
		df1.to_csv(os.path.join(filename, path))
	else:
		if len(df1) >= length:
			path = code + '.csv'
			print(code,'共有%s天数据' % len(df1))
			df1.to_csv(os.path.join(filename, path),index=False)


# ----------------------下载沪深300指数数据------------------- #
# date1是开始日期，date2是截止日期，filename是文件存放目录
def get_hs300_data(pro,date1, date2, filename):
	df = pro.index_daily(ts_code='399300.SZ', start_date=date1, end_date=date2)
	df1 = pd.DataFrame(df)
	df1 = df1.sort_values(by='trade_date')
	df1 = df1[['trade_date','open', 'high', 'close', 'low', 'vol', 'change']]
	print('399300.SZ 共有%s天数据' % len(df1))
	df1.to_csv(os.path.join(filename, '399300.csv'),index=False)


# ------------------------更新股票数据------------------------ #
# 将股票数据从本地文件的最后日期更新至当日
# filename:具体到文件名如d:\data\000001.csv
def update_stock_data(filename):
	(filepath, tempfilename) = os.path.split(filename)
	(stock_code, extension) = os.path.splitext(tempfilename)
	f = open(filename, 'r')
	df = pd.read_csv(f)
	print('股票{}文件中的最新日期为:{}'.format(stock_code, df.iloc[-1, 0]))
	data_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
	print('更新日期至：%s' % data_now)
	nf = ts.get_hist_data(stock_code, str(df.iloc[-1, 0]), data_now)
	nf = nf.sort_values(by='trade_date')
	nf = nf.iloc[1:]
	print('共有%s天数据' % len(nf))
	nf = pd.DataFrame(nf)
	nf = nf[['trade_date','open', 'high', 'close', 'low', 'vol', 'change']]
	nf.to_csv(filename, mode='a', header=False)
	f.close()



# ------------------------获取股票长度----------------------- #
# 辅助函数
def get_data_len(file_path):
	with open(file_path) as f:
		df = pd.read_csv(f)
		return len(df)


# --------------------------日期筛选------------------------- #
# 对已经再本地的文件按照日期筛选，date1是开始数据，date2是结束数据
# file1是源文件夹，file2是筛选日期后文件存放的文件夹
def select_stock_data(file1, file2, date1, date2):
	csv_list = glob.glob(file1 + '*.csv')
	print(u'共发现%s个CSV文件' % len(csv_list))
	file_list = []
	for i in csv_list:
		(filepath, filename) = os.path.split(i)
		file_list.append(filename)
	for i in file_list:
		f = open(os.path.join(file1, i), 'r')
		df1 = pd.read_csv(f, header=0)
		df1['trade_date'] = pd.to_datetime(df1['trade_date'])
		df1 = df1.set_index('trade_date')
		df2 = df1[date1:date2]
		df2.to_csv(os.path.join(file2, i))


def crop_stock(df, date):
	start = df.loc[df['日期'] == date].index[0]
	return df[start:]


# --------------------------停盘填充------------------------- #
# 按照沪深300指数来对个股停盘数据进行填充，填充为该股上一交易日的数据
# target为参照股票，sfile为原文件夹，tfile为填充完要存放文件夹
def fill_stock_data(target, sfile, tfile):
	tf = open(target)
	tf = pd.read_csv(tf)
	csv_list = glob.glob(sfile + '*.csv')
	print(u'共发现%s个CSV文件' % len(csv_list))
	i = 1
	for item in csv_list:
		f1 = open(item)
		print('正在处理第%s个文件' % i)
		df2 = pd.read_csv(f1)
		# print(df2)
		mix_data = pd.merge(tf, df2, how='outer', on="trade_date")
		mix_data = mix_data.fillna(method='pad')
		# print(mix_data)
		d1 = mix_data[['trade_date', 'open_y', 'high_y', 'close_y', 'low_y', 'vol_y', 'change_y']]
		d1.rename(columns={'open_y': 'open', 'high_y': 'high', 'close_y': 'close', 'low_y': 'low',  'vol_y': 'vol', 'change_y': 'change'}, inplace=True)
		(filepath, filename) = os.path.split(item)
		if not os.path.exists(tfile):
			os.makedirs(tfile)
		d1.to_csv(os.path.join(tfile, filename), index=False)
		i += 1


# --------------------------文件合并------------------------- #
# 将多个文件合并为一个文件，在文件末尾添加
# filename是需要合并的文件夹，tfile是存放合并后文件的文件夹
def merge_stock_data(filename, tfile):
	csv_list = glob.glob(filename + '*.csv')
	print(u'共发现%s个CSV文件' % len(csv_list))
	f = open(csv_list[0])
	df = pd.read_csv(f)
	for i in range(1, len(csv_list)):
		f1 = open(csv_list[i], 'rb')
		df1 = pd.read_csv(f1)
		df = pd.concat([df, df1])
	df.to_csv(tfile+'train_mix.csv', index=None)


def quchong(file):
	f = open(file)
	df = pd.read_csv(f, header=0)
	datalist = df.drop_duplicates()
	datalist.to_csv(file)


if __name__ == '__main__':
	import random
	pro = ts.pro_api('d7ec361542dc1140a1d15e7de5f1f3469da6837cd344bacd6f92a0e4')
	data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
	stock_list=data['ts_code'].tolist()
	maxlen=len(stock_list)
	# 随机取部分股票进行下载
	for i in range(20):
		get_stock_data_daily(pro,stock_list[random.randint(0,maxlen-1)],'20010101', '20200705', './data/')
	# %%
	get_hs300_data(pro=pro, date1='20010101', date2='20200705', filename='./data/')

	# %%
	fill_stock_data(target='./data/600569.SH.csv', sfile='./data/', tfile='./data1/')


