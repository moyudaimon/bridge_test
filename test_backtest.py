import requests
import json
import time
from datetime import datetime
import os

def test_backtest_api():
    # 设置Tushare Token
    os.environ['TUSHARE_TOKEN'] = "a5f5490d817d202f**********e0d9ff70b938f50d79"
    
    # API基础URL
    base_url = "http://127.0.0.1:8000"
    
    # 测试参数
    test_params = {
        "code": "000001",  # 平安银行
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    }
    
    try:
        print("开始测试回测API...")
        print(f"\n1. 测试参数: {json.dumps(test_params, ensure_ascii=False, indent=2)}")
        
        # 发送回测配置请求
        print("\n2. 发送回测配置请求...")
        config_response = requests.post(
            f"{base_url}/backtest/config",
            json=test_params
        )
        
        if config_response.status_code == 200:
            print("回测配置成功!")
            print(f"响应内容: {json.dumps(config_response.json(), ensure_ascii=False, indent=2)}")
        else:
            print(f"回测配置失败! 状态码: {config_response.status_code}")
            print(f"错误信息: {config_response.text}")
            return
        
        # 等待一秒确保回测完成
        time.sleep(1)
        
        # 获取回测结果
        print("\n3. 获取回测结果...")
        result_response = requests.get(f"{base_url}/backtest/result")
        
        if result_response.status_code == 200:
            result = result_response.json()
            print("回测结果获取成功!")
            print("\n回测结果:")
            print(f"初始资金: {result['initial_value']:,.2f}")
            print(f"最终资金: {result['final_value']:,.2f}")
            print(f"收益率: {result['returns']*100:.2f}%")
        else:
            print(f"获取回测结果失败! 状态码: {result_response.status_code}")
            print(f"错误信息: {result_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("连接错误: 请确保FastAPI服务已启动")
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")

if __name__ == "__main__":
    # 检查当前时间是否在交易时间内
    current_time = datetime.now().time()
    print(f"当前时间: {current_time}")
    
    # 运行测试
    test_backtest_api() 