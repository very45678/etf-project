# d:\etf\backend\test_tiantian_fund.py
import akshare as ak
import pandas as pd
from rich.console import Console
from rich.table import Table

def test_tiantian_fund_511880():
    """测试天天基金网接口获取511880净值数据"""
    console = Console()
    fund_code = '511880'
    
    console.print("[bold blue]=== 测试天天基金网接口获取511880净值数据 ===[/bold blue]")
    
    # 1. 使用fund_open_fund_daily_em接口（基于天天基金网）
    console.print("\n[bold green]1. 使用fund_open_fund_daily_em接口[/bold green]")
    try:
        nav_data = ak.fund_open_fund_daily_em()
        nav_511880 = nav_data[nav_data['基金代码'] == fund_code]
        
        if not nav_511880.empty:
            console.print(f"[green]✅ 成功找到511880数据[/green]")
            
            # 显示所有列名
            console.print("[blue]可用字段:[/blue]")
            for col in nav_data.columns:
                console.print(f"  - {col}")
            
            # 显示511880的完整数据
            console.print("\n[blue]511880完整数据:[/blue]")
            nav_511880 = nav_511880.iloc[0]
            for col, value in nav_511880.items():
                console.print(f"  {col}: {value}")
            
            # 提取净值相关字段
            nav_fields = [col for col in nav_511880.index if '单位净值' in col and '-' in col]
            if nav_fields:
                console.print("\n[blue]净值字段:[/blue]")
                nav_fields.sort(reverse=True)
                for field in nav_fields[:10]:  # 显示最近10天的净值
                    nav_value = nav_511880[field]
                    console.print(f"  {field}: {nav_value}")
            
        else:
            console.print(f"[red]❌ 未找到511880数据[/red]")
            
    except Exception as e:
        console.print(f"[red]❌ 接口调用失败: {str(e)}[/red]")
    
    # 2. 尝试使用fund_open_fund_info_em接口获取历史数据
    console.print("\n[bold green]2. 使用fund_open_fund_info_em接口获取历史数据[/bold green]")
    try:
        hist_data = ak.fund_open_fund_info_em(symbol=fund_code, indicator="单位净值走势")
        if not hist_data.empty:
            console.print(f"[green]✅ 成功获取历史数据，共{len(hist_data)}条记录[/green]")
            console.print("[blue]历史数据前5条:[/blue]")
            console.print(hist_data.head())
            
            # 显示列名
            console.print("\n[blue]历史数据字段:[/blue]")
            for col in hist_data.columns:
                console.print(f"  - {col}")
        else:
            console.print(f"[red]❌ 未获取到历史数据[/red]")
            
    except Exception as e:
        console.print(f"[red]❌ 历史数据接口调用失败: {str(e)}[/red]")
    
    # 3. 尝试使用fund_value_estimation_em接口获取估值数据
    console.print("\n[bold green]3. 使用fund_value_estimation_em接口获取估值数据[/bold green]")
    try:
        estimation_data = ak.fund_value_estimation_em()
        estimation_511880 = estimation_data[estimation_data['基金代码'] == fund_code]
        
        if not estimation_511880.empty:
            console.print(f"[green]✅ 成功获取估值数据[/green]")
            estimation_511880 = estimation_511880.iloc[0]
            
            # 显示估值字段
            console.print("[blue]估值字段:[/blue]")
            for col, value in estimation_511880.items():
                if '估算' in col:
                    console.print(f"  {col}: {value}")
        else:
            console.print(f"[red]❌ 未找到估值数据[/red]")
            
    except Exception as e:
        console.print(f"[red]❌ 估值数据接口调用失败: {str(e)}[/red]")

if __name__ == "__main__":
    test_tiantian_fund_511880()