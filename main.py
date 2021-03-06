
#http://www.grantjenks.com/docs/sortedcontainers/
#https://bigquant.com/community/t/topic/168319
#https://kwgoodman.github.io/bottleneck-doc/reference.html#moving-window-functions
#product,decayexponential,decaylinear仍需要加速
import warnings
warnings.filterwarnings('ignore')
from factor.load_data import local_data
# from factor.compute_engine import ComputeEngine
#
# self = ComputeEngine()
# self.get_local_basics_data(local_data)
# a = self.compute_factor("rank(Close)")
# a = self.compute_factor("delta(Close,5)")
# a = self.compute_factor("Close+High")
# a = self.compute_factor("Close-High")
# a = self.compute_factor("Close*High")
# a = self.compute_factor("Close/High")
# a = self.compute_factor("Close^High")
# a = self.compute_factor("delay(Close,5)")
# a = self.compute_factor("corr(Close,High,5)")
# a = self.compute_factor("exp(Close)")
# a = self.compute_factor("log(Close)")
# a = self.compute_factor("sign(Close)")
# a = self.compute_factor("arccos(Close)")
# a = self.compute_factor("arcsin(Close)")
# a = self.compute_factor("arctan(Close)")
# a = self.compute_factor("arccosh(Close)")
# a = self.compute_factor("arcsinh(Close)")
# a = self.compute_factor("arctanh(Close)")
# a = self.compute_factor("cos(Close)")
# a = self.compute_factor("sin(Close)")
# a = self.compute_factor("tan(Close)")
# a = self.compute_factor("cosh(Close)")
# a = self.compute_factor("tanh(Close)")
# a = self.compute_factor("abs(Close)")
# a = self.compute_factor("ceiling(Close)")
# a = self.compute_factor("floor(Close)")
# a = self.compute_factor("tsmin(Close,5)")
# a = self.compute_factor("tsmax(Close,5)")
# a = self.compute_factor("tsrank(Close,5)")
#
# a = self.compute_factor("std(Close,5)")
# a = self.compute_factor("max(Close,Open)")
# a = self.compute_factor("min(Close,Open)")
# a = self.compute_factor("multimin(Close,Open,Low)")
# a = self.compute_factor("multimax(Close,Open,Low)")
# a = self.compute_factor("sum(Close,5)")
# #a = compute_engine.compute_factor("prod(Close,5)")
# a = self.compute_factor("scale(Close)")
# a = self.compute_factor("lowday(Close,5)")
# a = self.compute_factor("highday(Close,5)")
# a = self.compute_factor("Close!=Close")
# a = self.compute_factor("Close<Open")
# a = self.compute_factor("Close<=Open")
# a = self.compute_factor("Close>Open")
# a = self.compute_factor("Close>=Open")
# a = self.compute_factor("Close==Open")
# a = self.compute_factor("Close&&Open")
# a = self.compute_factor("Close||Open")
# a = self.compute_factor("-Open")
# a = self.compute_factor("(Close>Open)?Close:Open")
#a = compute_engine.compute_factor("count(Close>Open,5)")

if __name__ == "__main__":
    from backtest import BacktestingEngine
    self = BacktestingEngine()
    self.get_local_basics_data(local_data)
    self.add_factor("High-Low")
    self.cross_select()
    self.return_cal()
    self.result_statistic.plot()