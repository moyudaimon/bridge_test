# 股票回测系统

这是一个基于FastAPI和Backtrader的股票回测系统，实现了一个简单的均线交叉策略。

## 环境要求

- Python 3.8+
- 安装依赖：`pip install -r requirements.txt`
- 需要设置Tushare API Token环境变量：`TUSHARE_TOKEN`

## 运行方式

1. 设置Tushare Token：
```bash
# Windows
set TUSHARE_TOKEN=你的token值

# Linux/Mac
export TUSHARE_TOKEN=你的token值
```

2. 启动服务：
```bash
uvicorn api.main:app --reload
```

## API使用说明

### 1. 设置回测配置

**请求方式：** POST

**接口地址：** `/backtest/config`

**请求参数：**
```json
{
    "code": "000001",  // 股票代码（平安银行）
    "start_date": "2023-01-01",  // 开始日期
    "end_date": "2023-12-31"     // 结束日期
}
```

**响应示例：**
```json
{
    "message": "回测完成",
    "status": "success"
}
```

### 2. 获取回测结果

**请求方式：** GET

**接口地址：** `/backtest/result`

**响应示例：**
```json
{
    "initial_value": 1000000,    // 初始资金
    "final_value": 1150000,      // 最终资金
    "returns": 0.15              // 收益率
}
```

## 策略说明

- 使用12日均线和26日均线
- 当12日均线上穿26日均线时买入
- 当价格跌破26日均线时卖出
- 每次买入使用20%的资金
- 考虑了万分之一的滑点

## 注意事项

1. 请确保正确设置了Tushare Token
2. 回测结果包含了手续费和滑点的影响
3. 每次只能运行一个回测实例



