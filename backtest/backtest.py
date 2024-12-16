import backtrader as bt
from .strategy import MAStrategy
from .data_feed import TushareData, PandasData
import os
from datetime import datetime

class Backtest:
    def __init__(self):
        self.cerebro = None
        self.result = None
        
    def run_backtest(self, code, start_date, end_date, 
                    initial_cash=1000000, commission=0.0001):
        """运行回测"""
        try:
            # 初始化回测引擎
            self.cerebro = bt.Cerebro()
            
            # 设置初始资金
            self.cerebro.broker.set_cash(initial_cash)
            
            # 设置手续费
            self.cerebro.broker.setcommission(commission=commission)
            
            # 获取数据
            try:
                tushare_data = TushareData()
                data = tushare_data.get_stock_data(code, start_date, end_date)
            except ValueError as e:
                raise ValueError(f"数据获取失败: {str(e)}")
            
            if data.empty:
                raise ValueError(f"没有获取到股票 {code} 在 {start_date} 到 {end_date} 期间的数据")
            
            # 添加数据到回测引擎
            data_feed = PandasData(dataname=data)
            self.cerebro.adddata(data_feed)
            
            # 添加策略
            self.cerebro.addstrategy(MAStrategy)
            
            # 运行回测
            initial_portfolio_value = self.cerebro.broker.getvalue()
            results = self.cerebro.run()
            final_portfolio_value = self.cerebro.broker.getvalue()
            
            # 计算收益率
            returns = (final_portfolio_value - initial_portfolio_value) / initial_portfolio_value
            
            # 保存结果
            self.result = {
                'initial_value': initial_portfolio_value,
                'final_value': final_portfolio_value,
                'returns': returns
            }
            
            return self.result
            
        except Exception as e:
            raise ValueError(f"回测执行失败: {str(e)}")
    
    def get_result(self):
        """获取回测结果"""
        if self.result is None:
            return {'error': 'No backtest results available'}
        return self.result