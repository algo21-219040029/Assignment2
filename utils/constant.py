
from enum import Enum

class SelectMode1(Enum):
    """"""
    LONG_SHORT = "多空"
    LONG = "做多"
    SHORT = "做空"
    
class SelectMode2(Enum):
    """"""
    NUM = "数量"
    PCT = "比例"
    
class Interval(Enum):
    """"""
    MINUTE = "分钟"
    HOUR = "小时"
    DAY = "天"
    WEEK = "周"
    MONTH = "月"