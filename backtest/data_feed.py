import tushare as ts
import pandas as pd
import backtrader as bt
from datetime import datetime
import os

class TushareData:
    def __init__(self, token=None):
        # 设置token
        self.token = token or os.getenv('TUSHARE_TOKEN')
        if not self.token:
            raise ValueError("Tushare token not found. Please set TUSHARE_TOKEN environment variable.")
        
        print(f"当前使用的Token: {self.token}")  # 打印token用于验证
        
        # 初始化pro接口
        try:
            self.pro = ts.pro_api(self.token)
            # 测试API连接
            test_data = self.pro.stock_basic(limit=1)
            if test_data is None or test_data.empty:
                raise ValueError("Token验证失败，无法获取数据")
            print("Token验证成功！")
        except Exception as e:
            raise ValueError(f"Token验证失败: {str(e)}")
        
    def get_stock_data(self, code, start_date, end_date):
        """获取股票数据"""
        try:
            print(f"正在获取股票{code}从{start_date}到{end_date}的数据...")
            
            # 转换股票代码格式
            if code.startswith('6'):
                ts_code = f"{code}.SH"
            else:
                ts_code = f"{code}.SZ"
            
            # 使用pro接口获取数据
            df = self.pro.daily(ts_code=ts_code,
                              start_date=start_date.replace('-', ''),
                              end_date=end_date.replace('-', ''))
            
            if df is None or df.empty:
                raise ValueError(f"No data found for stock {code} between {start_date} and {end_date}")
            
            print(f"成功获取到{len(df)}条数据")
            
            # 按照交易日期排序
            df = df.sort_values('trade_date')
            
            # 转换为backtrader可用的格式
            df['datetime'] = pd.to_datetime(df['trade_date'])
            df.set_index('datetime', inplace=True)
            
            # 重命名列以匹配backtrader要求
            df = df.rename(columns={
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'vol': 'volume'
            })
            
            # 选择需要的列并返回
            return df[['open', 'high', 'low', 'close', 'volume']]
        except Exception as e:
            raise ValueError(f"Error fetching stock data: {str(e)}")

class PandasData(bt.feeds.PandasData):
    """自定义数据源"""
    params = (
        ('datetime', None),
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'volume'),
        ('openinterest', None),
    )