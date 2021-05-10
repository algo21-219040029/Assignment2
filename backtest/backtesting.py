# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 14:22:02 2019

@author: Administrator
"""
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
import warnings
warnings.filterwarnings('ignore')

from backtest.selectstock import SelectStock
from factor.compute_engine import ComputeEngine
from backtest.resultstatistic import ResultStatistic
from utils.constant import SelectMode1, SelectMode2, Interval

class BacktestingEngine:
    """"""
    
    parameters = ["n_long","n_short","pct_long","pct_short","freq","select_mode1","select_mode2","mask","deal","rate","Interval","benchmark"]
    
    def __init__(self):
        """"""
        self.n_long = 50
        self.n_short = 50
        self.pct_long = 0.2
        self.pct_short = 0.2
        self.freq = 1
        self.select_mode1 = SelectMode1.LONG
        self.select_mode2 = SelectMode2.NUM
        self.mask = ""
        self.deal = "open"
        self.rate = 0.0
        self.Interval = Interval.DAY
        
        self.factor_dict = {}
                
        self.compute_engine = ComputeEngine()
        self.select_stock = SelectStock(self)
        self.result_statistic = ResultStatistic(self)
        
    def set_parameters(self, setting):
        """设置参数，既包括BacktestingEngine的参数，也包括SelectStock和ResultStatistic的参数"""
        for name in setting:
            if name in self.parameters:
                setattr(self, name, setting[name])
            if name in self.select_stock.parameters:
                setattr(self.select_stock, name, setting[name])
            if name in self.result_statistic.parameters:
                setattr(self.result_statistic, name, setting[name])
        
    def add_factor(self, factor: str):
        """添加因子"""
        self.factor_dict[factor] = self.compute_factor(factor)
        self.select_stock.factor_dict[factor] = self.factor_dict[factor]
        self.select_stock.factor = factor
        self.select_stock.factor_data = self.factor_dict[factor]
        
    def remove_factor(self, factor: str):
        """删除因子"""
        del self.factor_dict[factor]
        del self.select_stock.factor_dict[factor]
        self.select_stock.factor = None
        self.select_stock.factor_data = None
        
    def cross_select(self):
        """横截面选股"""
        selection = self.select_stock.cross_select()
        self.selection = selection
        return selection
    
    def return_cal(self):
        """"""
        self.result_statistic.init_returns()
        cum_total_return,cum_bench_return,cum_excess_return = self.result_statistic.return_cal()
        return cum_total_return,cum_bench_return,cum_excess_return
    
    def compute_factor(self, factor: str):
        """"""
        value = self.compute_engine.compute_factor(factor)
        return value
    
    def get_local_basics_data(self, data: dict):
        """获取本地基本元数据"""
        self.compute_engine.get_local_basics_data(data)
    
    def get_backtesting_result(self):
        """得到策略回测指标"""
        return self.result_statistic.indices
    
    def get_daily_select(self, date):
        """得到每日选股情况"""
        selection = self.select_stock.selection
        daily_selection = selection.loc[date, :]
        long_selection = list(daily_selection.loc[daily_selection == 1.0].dropna().index)
        short_selection = list(daily_selection.loc[daily_selection == -1.0].dropna().index)
        
        factor_data = self.select_stock.factor_data
        daily_factor = factor_data.loc[date, :]
        long_factor = daily_factor.loc[long_selection]
        short_factor = daily_factor.loc[short_selection]
        
        return_df = self.result_statistic.return_df.shift(-1)
        daily_return = return_df.loc[date, :]
        long_return = daily_return.loc[long_selection]
        short_return = daily_return.loc[short_selection]
        
        long = pd.concat([long_factor, long_return],axis=1)
        long.columns = ["因子值","未来持有收益率"]
        
        short = pd.concat([short_factor, short_return],axis=1)
        short.columns = ["因子值","未来持有收益率"]
        
        long = long.sort_values(by="因子值",ascending = False)
        short = short.sort_values(by="因子值",ascending = False)
        
        return long, short
    
    def get_basics_data(self, factor = None):
        """获取基本元数据"""
        value = self.compute_engine.factor_compute.get_value(factor)
        return value
    
    def get_computed_factor(self, factor = None):
        """
        获取在回测过程被计算过的因子,
        一般包括筛选股票的因子和排序股票的因子
        """
        if factor:
            value = self.compute_engine.factor_value_map[factor]
        else:
            value = self.compute_engine.factor_value_map
        return value
        
        