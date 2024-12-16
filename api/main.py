from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from backtest.backtest import Backtest
import os

# 设置Tushare Token
os.environ['TUSHARE_TOKEN'] = "a5f5490d81**********f70b938f50d79"

app = FastAPI(title="股票回测API")

# 全局回测实例
backtest_instance = Backtest()

class BacktestConfig(BaseModel):
    code: str
    start_date: str
    end_date: str

@app.post("/backtest/config")
async def set_backtest_config(config: BacktestConfig):
    """设置回测配置并运行回测"""
    try:
        # 验证日期格式
        try:
            datetime.strptime(config.start_date, '%Y-%m-%d')
            datetime.strptime(config.end_date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用YYYY-MM-DD格式")
        
        # 验证Tushare Token
        if not os.getenv('TUSHARE_TOKEN'):
            raise HTTPException(
                status_code=500,
                detail="未设置Tushare Token，请设置TUSHARE_TOKEN环境变量"
            )
        
        # 运行回测
        try:
            result = backtest_instance.run_backtest(
                code=config.code,
                start_date=config.start_date,
                end_date=config.end_date
            )
            return {"message": "回测完成", "status": "success"}
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"回测过程中出现错误: {str(e)}")

@app.get("/backtest/result")
async def get_backtest_result():
    """获取回测结果"""
    result = backtest_instance.get_result()
    if 'error' in result:
        raise HTTPException(status_code=404, detail="没有可用的回测结果")
    return result 