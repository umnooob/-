#-*- coding:utf-8 -*-
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
import datetime

def count_businessday(start_day, end_day):
    """计算工作日日志

    Args:
        start_day: 开始时间
        end_day: 结束时间

    Returns:
        每周工作日:list[list[datetime.datetime]]
    """
    # 公共假期
    b = CustomBusinessDay(holidays=[
        '2023-01-02', '2023-01-21', '2023-01-22', '2023-01-23', '2023-01-24', '2023-01-25', '2023-01-26', '2023-01-27'
    ])
    # 工作日
    bus_day = pd.date_range(start=start_day, end=end_day, freq=b)
    my_datetimes = [t.to_pydatetime() for t in bus_day]

    # 按周分类
    my_dict = {}
    for dt in my_datetimes:
        current_week_first_day = dt - datetime.timedelta(days=dt.weekday())
        current_week_start_date = current_week_first_day.date()
        if current_week_start_date not in my_dict:
            my_dict[current_week_start_date] = []
        my_dict[current_week_start_date].append(dt)
    weeks:list[list[datetime.datetime]] = list(my_dict.values())
    return weeks

def generate_prompt(start_day, end_day):
    """生成chatGPT相关输入
    """
    weeks = count_businessday(start_day,end_day)
    #每周工作的核心词
    keywords = [
        "深度学习基础学习以及了解图神经网络包括GCN,GAT,GraphSAGE",
    ]
    for i, week in enumerate(weeks):
        prompt = f"{i+1}:请根据以下一周工作的内容提供{len(week)}点工作内容：“日期：{week[0].strftime('%Y年%m月%d日')}至{week[-1].strftime('%Y年%m月%d日')} {keywords[i]}”\n根据这些工作内容再分别填充为{len(week)}篇内容连续的毕设日报（每篇500字左右），每篇之间以---分割，毕设日报格式为“工作内容 工作进展 总结”"
        print(prompt)

if __name__ == '__main__':
    start_day = '2022-11-06'
    end_day = '2022-11-11'
    generate_prompt(start_day, end_day)
