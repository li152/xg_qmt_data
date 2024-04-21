from xtquant import xtdata
from xtquant import xttrader
from xtquant import xtconstant 
from xtquant import xtbson
from xtquant import xtconn
import time
import pandas as pd
class qmt_data:
    '''
    qmt数据
    stock_code - 合约代码
    格式为 code.market，例如000001.SZ 600000.SH 000300.SH
    period - 周期，用于表示要获取的周期和具体数据类型
    level1数据
    tick - 分笔数据
    1m - 1分钟线
    5m - 5分钟线
    15m - 15分钟线
    30m - 30分钟线
    1h - 1小时线
    1d - 日线
    1w - 周线
    1mon - 月线
    1q - 季度线
    1hy - 半年线
    1y - 年线
    '''
    def __init__(self):
        '''
        小果qmt数据
        '''
        self.xtdata=xtdata
        print('作者:小果')
        print('作者微信:15117320079')
        print('作者微信公众号:数据分析与运用')
        print('公众号链接:https://mp.weixin.qq.com/s/rxGJpZYxdUIHitjvI-US1A')
        print("作者知识星球:金融量化交易研究院")

    def get_all_qmt_data(self):
        '''
        获取原来的qmt全部内容
        '''
        return self.xtdata
    def subscribe_quote(self,stock_code='600031.SH', period='1d', 
                    start_time='20210101', end_time='20240101', count=100, callback=None):
        '''
        释义
        订阅单股的行情数据，返回订阅号
        数据推送从callback返回，数据类型和period指定的周期对应
        数据范围代表请求的历史部分的数据范围，数据返回后会进入缓存，用于保证数据连续，通常情况仅订阅数据时传count = 0即可
        参数
        stock_code - string 合约代码
        period - string 周期
        start_time - string 起始时间
        end_time - string 结束时间
        count - int 数据个数
        callback - 数据推送回调
        回调定义形式为on_data(datas)，回调参数datas格式为 { stock_code : [data1, data2, ...] }
        '''
        stats=self.xtdata.subscribe_quote(stock_code=stock_code,period=period,
                                          start_time=start_time,end_time=end_time,
                                          count=count,callback=callable)
        if stats !=-1:
            print('{}订阅成功'.format(stock_code))
        else:
            print('{}订阅失败'.format(stock_code))
        return stats
    def on_data(self,data):
        # 获取到本次触发的标的代码
        code_list = list(data.keys())    # 获取到本次触发的标的代码
        kline_in_callabck = self.xtdata.get_market_data_ex([],code_list,period = '1m')    # 在回调中获取klines数据
        print(kline_in_callabck)
    def subscribe_whole_quote(self,code_list=['600031.SH'], callback=None):
        '''
        释义
        订阅全推行情数据，返回订阅号
        数据推送从callback返回，数据类型为分笔数据
        参数
        code_list - 代码列表，支持传入市场代码或合约代码两种方式
        传入市场代码代表订阅全市场，示例：['SH', 'SZ']
        传入合约代码代表订阅指定的合约，示例：['600000.SH', '000001.SZ']
        callback - 数据推送回调
        回调定义形式为on_data(datas)，回调参数datas格式为 { stock1 : data1, stock2 : data2, ... }
        '''
        stats=self.xtdata.subscribe_whole_quote(code_list=code_list,callback=callback)
        if stats !=-1:
            print('{}订阅成功'.format(code_list))
        else:
            print('{}订阅失败'.format(code_list))
        return stats
    def on_data_whole_quote(self,datas):
        '''
        全推回调函数
        '''
        for stock_code in datas:
                print(stock_code, datas[stock_code])
    def unsubscribe_quote(self,seq):
        '''
        释义
        反订阅行情数据
        参数
        seq - 订阅时返回的订阅号
        '''
        self.xtdata.unsubscribe_quote(seq=seq)
    def run(self):
        '''
        释义
        阻塞当前线程来维持运行状态，一般用于订阅数据后维持运行状态持续处理回调
        参数
        seq - 订阅时返回的订阅号
        返回
        无
        备注
        实现方式为持续循环sleep，并在唤醒时检查连接状态，若连接断开则抛出异常结束循环

        '''
        self.xtdata.run()
    def get_market_data(self,field_list=[], stock_list=['600031.SH','600111.SH'], 
                        period='1d', start_time='20210101', end_time='20240419',
                        count=-100, dividend_type='none', fill_data=True):
        '''
        数据需要先订阅

        释义
        从缓存获取行情数据，是主动获取行情的主要接口
        参数
        field_list - list 数据字段列表，传空则为全部字段
        stock_list - list 合约代码列表
        period - string 周期
        start_time - string 起始时间
        end_time - string 结束时间
        count - int 数据个数
        默认参数，大于等于0时，若指定了start_time，end_time，此时以end_time为基准向前取count条；若start_time，end_time缺省，默认取本地数据最新的count条数据；若start_time，end_time，count都缺省时，默认取本地全部数据
        dividend_type - string 除权方式
        fill_data - bool 是否向后填充空缺数据
        返回
        period为1m 5m 1d等K线周期时
        返回dict { field1 : value1, field2 : value2, ... }
        field1, field2, ... ：数据字段
        value1, value2, ... ：pd.DataFrame 数据集，index为stock_list，columns为time_list
        各字段对应的DataFrame维度相同、索引相同
        period为tick分笔周期时
        返回dict { stock1 : value1, stock2 : value2, ... }
        stock1, stock2, ... ：合约代码
        value1, value2, ... ：np.ndarray 数据集，按数据时间戳time增序排列
        备注
        获取lv2数据时需要数据终端有lv2数据权限
        时间范围为闭区间
        '''
        df=self.xtdata.get_market_data(field_list, stock_list, period, 
                                       start_time, end_time, count, dividend_type, fill_data)
        return df
    def get_market_data_pandas(self,df,stock_list=['600031.SH','600111.SH']):
        '''
        get_market_data函数转成pandas
        df函数获取的数据
        stock_list股票代码
        '''
        data=pd.DataFrame()
        keys_list=list(df.keys())
        for stock in stock_list:
            for keys in keys_list:
                df1=pd.DataFrame(df[keys])
                df1=df1.T
                data['{}_{}'.format(stock,keys)]=df1[stock]
        return data
    def conv_time(self,ct):
        '''
        conv_time(1476374400000) --> '20161014000000.000'
        '''
        local_time = time.localtime(ct / 1000)
        data_head = time.strftime('%Y%m%d%H%M%S', local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = '%s.%03d' % (data_head, data_secs)
        return time_stamp
    def get_local_data(self,field_list=[], stock_list=['600031.SH','600111.SH'], 
                period='1d', start_time='20210101', end_time='20240419', count=-1000,
               dividend_type='none', fill_data=True, data_dir=None):
        '''
        本地没有的话需要下载补充
        例子
        models=qmt_data()
        stock_list=['600031.SH','600111.SH']
        for stock in stock_list:
            models.download_history_data(stock_code=stock,start_time='20210101',
                                        end_time='20240419',period='1m')
        df=models.get_local_data(stock_list=stock_list,period='1m',start_time='20210101',
                                        end_time='20240419')
        print(df)
        释义
        从本地数据文件获取行情数据，用于快速批量获取历史部分的行情数据
        参数
        field_list - list 数据字段列表，传空则为全部字段
        stock_list - list 合约代码列表
        period - string 周期
        start_time - string 起始时间
        end_time - string 结束时间
        count - int 数据个数
        dividend_type - string 除权方式
        fill_data - bool 是否向后填充空缺数据
        data_dir - string MiniQmt配套路径的userdata_mini路径，用于直接读取数据文件。默认情况下xtdata会通过连接向MiniQmt直接获取此路径，无需额外设置。如果需要调整，可以将数据路径作为data_dir传入，也可以直接修改xtdata.data_dir以改变默认值
        返回
        period为1m 5m 1dK线周期时
        返回dict { field1 : value1, field2 : value2, ... }
        field1, field2, ... ：数据字段
        value1, value2, ... ：pd.DataFrame 数据集，index为stock_list，columns为time_list
        各字段对应的DataFrame维度相同、索引相同
        period为tick分笔周期时
        返回dict { stock1 : value1, stock2 : value2, ... }
        stock1, stock2, ... ：合约代码
        value1, value2, ... ：np.ndarray 数据集，按数据时间戳time增序排列
        备注
        仅用于获取level1数据
        获取全推数据
        '''
        df=self.xtdata.get_local_data(field_list, stock_list, 
                                    period, start_time, end_time, count,
                        dividend_type, fill_data, data_dir)
        return df
    def download_history_data(self,stock_code='600031.SH', period='1m', 
                              start_time='20210101', end_time='20240419', incrementally = None):
        '''
        例子
        models=qmt_data()
        df=models.download_history_data(stock_code='600031.SH',period='1m',start_time='19990101')
        df=models.get_local_data(stock_list=['600031.SH'],period='1m',start_time='19990101')
        print(df)
        释义
        补充历史行情数据
        参数
        stock_code - string 合约代码
        period - string 周期
        start_time - string 起始时间
        end_time - string 结束时间
        incrementally - 是否增量下载
        bool - 是否增量下载
        None - 使用start_time控制，start_time为空则增量下载
        返回
        无
        备注
        同步执行，补充数据完成后返回
        '''
        self.xtdata.download_history_data(stock_code, period, start_time, end_time, incrementally)
    def download_history_data2(self,stock_list=['600031.SH','600111.SH'], period='1d', 
                               start_time='20210101', end_time='20240419', callback=None):
        '''
        例子
        models=qmt_data()
        stock_list=['600031.SH','600111.SH']
        func=models.on_progress
        models.download_history_data2(callback=func)
        models.run()

        释义
        补充历史行情数据，批量版本
        参数
        stock_list - list 合约列表
        period - string 周期
        start_time - string 起始时间
        end_time - string 结束时间
        callback - func 回调函数
        参数为进度信息dict
        total - 总下载个数
        finished - 已完成个数
        stockcode - 本地下载完成的合约代码
        message - 本次信息
        '''
        self.xtdata.download_history_data2(stock_list, period, 
                                           start_time, end_time, callback)
    def on_progress(self,data):
        print(data)
        # {'finished': 1, 'total': 50, 'stockcode': '000001.SZ', 'message': ''}
    def get_full_tick(self,code_list=['600031.SH','600111.SH']):
        '''
        例子
        models=qmt_data()
        stock_list=['600031.SH','600111.SH']
        df=models.get_full_tick()
        print(df)
        释义
        获取全推数据
        参数
        code_list - 代码列表，支持传入市场代码或合约代码两种方式
        传入市场代码代表订阅全市场，示例：['SH', 'SZ']
        传入合约代码代表订阅指定的合约，示例：['600000.SH', '000001.SZ']
        返回
        dict 数据集 { stock1 : data1, stock2 : data2, ... }
        备注
        无
        获取除权数据
        '''
        df=self.xtdata.get_full_tick(code_list=code_list)
        return df
    def get_divid_factors(self,stock_code='600031.SH',start_time='20210101', end_time='20240419'):
        '''
        例子
        models=qmt_data()
        stock_list=['600031.SH','600111.SH']
        df=models.get_divid_factors()
        print(df)
        释义
        获取除权数据
        参数
        stock_code - 合约代码
        start_time - string 起始时间
        end_time - string 结束时间
        返回
        pd.DataFrame 数据集
        '''
        df=self.xtdata.get_divid_factors(stock_code,start_time,end_time)
        return df
    def get_l2_quote(self,field_list=[], stock_code='600031.SH', start_time='20210101', 
                     end_time='20240409', count=-1):
        '''
        先订阅有的证券公司没有这个数据
        models=qmt_data()
        models.subscribe_quote(stock_code='600031.SH')
        df=models.get_l2_quote(stock_code='600031.SH')
        print(df)
        获取level2行情快照数据
        参数
        field_list - list 数据字段列表，传空则为全部字段
        stock_code - string 合约代码
        start_time - string 起始时间
        end_time - string 结束时间
        count - int 数据个数
        返回
        np.ndarray 数据集，按数据时间戳time增序排列
        备注
        需要缓存中有接收过的数据才能获取到
        '''
        df=self.xtdata.get_l2_quote(field_list, stock_code, start_time, end_time, count)
        return df
    def get_l2_order(self,field_list=[], stock_code='600031.SH', start_time='20210101', 
                     end_time='20240101', count=-1):
        '''
        先订阅有的证券公司没有这个数据
        models=qmt_data()
        models.subscribe_quote(stock_code='600031.SH')
        df=models.get_l2_order(stock_code='600031.SH')
        print(df)
        释义
        获取level2逐笔委托数据
        参数
        field_list - list 数据字段列表，传空则为全部字段
        stock_code - string 合约代码
        start_time - string 起始时间
        end_time - string 结束时间
        count - int 数据个数
        返回
        np.ndarray 数据集，按数据时间戳time增序排列
        备注
        需要缓存中有接收过的数据才能获取到
        获取level2逐笔成交数据
        '''
        df=self.xtdata.get_l2_order(field_list, stock_code, start_time, end_time, count)
        return df
    def get_l2_transaction(self,field_list=[], stock_code='600031.SH', start_time='20210101', 
                           end_time='20240101', count=-1):
        '''
        先订阅有的证券公司没有这个数据
        models=qmt_data()
        models.subscribe_quote(stock_code='600031.SH')
        df=models.get_l2_transaction(stock_code='600031.SH')
        释义
        获取level2逐笔成交数据
        参数
        field_list - list 数据字段列表，传空则为全部字段
        stock_code - string 合约代码
        start_time - string 起始时间
        end_time - string 结束时间
        count - int 数据个数
        返回
        np.ndarray 数据集，按数据时间戳time增序排列
        备注
        需要缓存中有接收过的数据才能获取到
        '''
        df=self.xtdata.get_l2_transaction(field_list, stock_code, start_time, end_time, count)
        return df
    def get_holidays(self):
        '''
        释义
        获取截止到当年的节假日日期
        参数
        无
        返回
        list，为8位的日期字符串格式
        备注
        无
        获取交易日
        '''
        df=self.xtdata.get_holidays()
        return df
    def get_trading_calendar(self,market='SH', start_time = '20240101', end_time = '20240401'):
        '''
        models=qmt_data()
        df=models.get_trading_calendar()
        print(df)
        释义
        获取指定市场交易日历
        参数
        market - str 市场
        start_time - str 起始时间，8位字符串。为空表示当前市场首个交易日时间
        end_time - str 结束时间，8位字符串。为空表示当前时间
        返回
        返回list，完整的交易日列表
        备注
        结束时间可以填写未来时间，获取未来交易日。需要下载节假日列表。
        获取交易时段
        '''
        df=self.get_trading_calendar(market,start_time,end_time)
        return df


        
if __name__=="__main__":
    #启动模型
    models=qmt_data()
    df=models.get_trading_calendar()
    print(df)
    
    
     

