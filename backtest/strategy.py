import backtrader as bt

class MAStrategy(bt.Strategy):
    params = (
        ('fast_period', 12),  # 快速均线周期
        ('slow_period', 26),  # 慢速均线周期
        ('position_size', 0.2),  # 仓位比例
    )

    def __init__(self):
        # 计算快速和慢速移动平均线
        self.fast_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.fast_period)
        self.slow_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.slow_period)
        
        # 交叉信号
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
        
        # 用于跟踪是否持仓
        self.holding = False

    def next(self):
        # 如果没有持仓且快线上穿慢线
        if not self.holding and self.crossover > 0:
            # 计算购买数量（本金的20%）
            size = int((self.broker.get_cash() * self.params.position_size) / self.data.close[0])
            self.buy(size=size)
            self.holding = True
            
        # 如果持仓且价格跌破慢速均线
        elif self.holding and self.data.close[0] < self.slow_ma[0]:
            self.sell()
            self.holding = False 