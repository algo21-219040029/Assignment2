# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 11:11:40 2019

@author: Administrator
"""
import numpy as np
import pandas as pd
from copy import deepcopy
import matplotlib.pyplot as plt

from utils.constant import Interval

class ResultStatistic:
    """回测结果统计"""
    
    parameters = ["deal","rate","Interval","benchmark"]
    
    def __init__(self, backtesting_engine):
        """"""
        self.deal = "open"
        self.rate = 0.0
        self.Interval = Interval.DAY
        self.benchmark = True
        
        self.indices = {}
        
        self.backtesting_engine = backtesting_engine
        
    def set_parameters(self, setting):
        """设置参数"""
        for name in setting:
            if name in self.parameters:
                setattr(self, name, setting[name])
        
    def get_selection(self):
        """获取选股结果"""
        self.selection = self.backtesting_engine.selection
        return self.selection
    
    def init_returns(self):
        """
        初始化股票和基准收益率，
        避免了在计算策略
        收益率时再计算收益率导致反复计算
        
        注：所有收益率的索引都是以收益率开始的时间为准。例如：用2008-03-05到2008-03-06的收盘价计算的收益率的索引为2008-03-05
        """
        
        """股票收益率"""
        if hasattr(self, "return_df"):
            print("收益率dataframe已经初始化")
            return
        
        deal = self.deal
        
        if deal == "open":
            returns = "delta(Open,1)/delay(Open,1)"
            return_df = self.compute_factor(returns).shift(-1)
        elif deal == "close":
            returns = "delta(close,1)/delay(close,1)"
            return_df = self.compute_factor(returns).shift(-1)
        else:
            return
        
        """基准收益率"""
        if self.benchmark:
            bench_return = self.get_basics_value("BenchmarkIndexClose()").pct_change(1).shift(-1)
        
        self.return_df = return_df
        if self.benchmark:
            self.bench_return = bench_return
            return return_df, bench_return
        else:
            return return_df
        
    def compute_factor(self, factor):
        """因子计算，计算收益率时用"""
        value = self.backtesting_engine.compute_factor(factor)
        return value
    
    def get_basics_value(self, basic_factor):
        """获取基本元数据"""
        return self.backtesting_engine.compute_engine.factor_compute.get_value(basic_factor)
    
    def get_portfolio_num(self):
        """获取做多和做空的股票数量"""
        select_stock = self.backtesting_engine.select_stock
        return select_stock.n1, select_stock.n2
    
    def get_turnover_rate(self):
        """获取换手率"""
        select_stock =self.backtesting_engine.select_stock
        return select_stock.turnover_rate
    
    def return_cal(self):
        """
        收益率计算：包括总收益率、基准收益率和超额收益率
        """
        selection = self.get_selection()
        
        return_df = self.return_df
        if self.benchmark:
            bench_return = self.bench_return
        
        select_corr = selection.shift(1)  #selection反映的是因子得到的结果，而select_corr则是实际的选股结果
        weight = deepcopy(select_corr).fillna(0)
        
        n1, n2 = self.get_portfolio_num()
        
        return_per_bar = (return_df*weight).sum(axis=1)/(n1+n2).fillna(0)
        return_per_bar[return_per_bar == np.inf] = 0.0
        return_per_bar[return_per_bar == -np.inf] = 0.0
        
        def func_cum(Series):
            if isinstance(Series, pd.Series):
                Series = Series+1
                Series_ = Series.shift(1)
                Series_.iloc[0] = 1
                cum_return_result = Series_.cumprod()
            elif isinstance(Series, pd.DataFrame):
                df = Series+1
                df_ = df.shift(1)
                df_.iloc[0,:] = 1
                cum_return_result = df_.cumprod()
            return cum_return_result
        
        turnover_rate = self.backtesting_engine.select_stock.turnover_rate
        total_return = return_per_bar - turnover_rate*2*self.rate
        if self.benchmark:
            excess_return = (1+total_return)/(1+bench_return)-1
        
        cum_total_return = func_cum(total_return)
        print(bench_return)
        if self.benchmark:
            cum_bench_return = func_cum(bench_return)
            cum_excess_return = func_cum(excess_return)
        
        self.total_return = total_return
        if self.benchmark:
            self.excess_return = excess_return
        
        self.cum_total_return = cum_total_return
        if self.benchmark:
            self.cum_bench_return = cum_bench_return
            self.cum_excess_return = cum_excess_return
        
        self.indice_statistic()
        self.plot()
        
        if self.benchmark:
            return cum_total_return, cum_bench_return, cum_excess_return
        else:
            return cum_total_return
    
    def indice_statistic(self):
        
        """策略指标的计算"""
        
        cum_total_return = self.cum_total_return
        if self.benchmark:
            cum_bench_return = self.cum_bench_return
            cum_excess_return = self.cum_excess_return
        
        total_return = self.total_return
        if self.benchmark:
            bench_return = self.bench_return
            excess_return = self.excess_return
        
        turnover_rate = self.backtesting_engine.select_stock.turnover_rate
        
        interval = self.Interval
        if interval == Interval.MINUTE:
            times = 60000
        elif interval == Interval.HOUR:
            times = 1000
        elif interval == Interval.DAY:
            times = 250
        elif interval == Interval.WEEK:
            times = 36
        elif interval == Interval.MONTH:
            times = 12
        
        """年化收益"""
        annual_total_return = cum_total_return.iloc[-1]**(times/len(cum_total_return.index))-1
        if self.benchmark:
            annual_bench_return = cum_bench_return.iloc[-1]**(times/len(cum_bench_return.index))-1
            annual_excess_return = cum_excess_return.iloc[-1]**(times/len(cum_excess_return.index))-1
        
        """最大回撤"""
        total_drawdown = (cum_total_return.cummax()-cum_total_return)/cum_total_return.cummax()
        if self.benchmark:
            bench_drawdown = (cum_bench_return.cummax()-cum_bench_return)/cum_bench_return.cummax()
            excess_drawdown = (cum_excess_return.cummax()-cum_excess_return)/cum_excess_return.cummax()
        
        self.total_drawdown = total_drawdown
        if self.benchmark:
            self.bench_drawdown = bench_drawdown
            self.excess_drawdown = excess_drawdown
        
        total_max_drawdown = max(total_drawdown)
        if self.benchmark:
            bench_max_drawdown = max(bench_drawdown)
            excess_max_drawdown = max(excess_drawdown)
        
        """夏普比率"""
        total_sharpe = total_return.mean()/total_return.std()*np.sqrt(times)
        if self.benchmark:
            bench_sharpe = bench_return.mean()/bench_return.std()*np.sqrt(times)
            excess_sharpe = excess_return.mean()/excess_return.std()*np.sqrt(times)
        
        """年换手率"""
        annual_turnover_rate = turnover_rate.sum()*times/len(turnover_rate.index)
        
        """每笔盈利"""
        every_total_profit = annual_total_return/annual_turnover_rate
        if self.benchmark:
            every_excess_profit = annual_excess_return/annual_turnover_rate
        
        self.indices["总年化收益"] = annual_total_return
        if self.benchmark:
            self.indices["基准年化收益"] = annual_bench_return
            self.indices["超额年化收益"] = annual_excess_return
        
        self.indices["总最大回撤"] = total_max_drawdown
        if self.benchmark:
            self.indices["基准最大回撤"] = bench_max_drawdown
            self.indices["超额最大回撤"] = excess_max_drawdown
        
        self.indices["总夏普比率"] = total_sharpe
        if self.benchmark:
            self.indices["基准夏普比率"] = bench_sharpe
            self.indices["超额夏普比率"] = excess_sharpe
        
        self.indices["年换手率"] = annual_turnover_rate
        
        self.indices["总每笔盈利"] = every_total_profit
        if self.benchmark:
            self.indices["超额每笔盈利"] = every_excess_profit
        
    def plot(self):
        """画图"""
        cum_total_return = self.cum_total_return
        if self.benchmark:
            cum_bench_return =self.cum_bench_return
            cum_excess_return = self.cum_excess_return
        
        if self.benchmark:
            all_return_df = pd.concat([cum_total_return,cum_bench_return,cum_excess_return],axis=1)
            all_return_df.columns = ["总累积收益","基准累积收益","超额累积收益"]
        else:
            all_return_df = deepcopy(cum_total_return)
            all_return_df.columns = ["总累积收益"]
        
        all_return_df.plot(figsize=(20,8),logy=True)
        plt.show()