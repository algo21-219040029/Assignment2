from factor.basics import basic_factors
from factor.stringtrans import body, repair
from factor.factor_compute import FactorCompute

class ComputeEngine:

    def __init__(self) -> None:
        """Constructor"""
        self.factors = []

        self.factor_ftrans_map = {}
        self.factor_value_map = {}
        self.ftrans_value_map = {}

        self.init_compute_engine()

    def init_compute_engine(self):
        """初始化因子计算类"""
        self.factor_compute = FactorCompute()
        name_trans = {}
        for i in basic_factors:
            name_trans[i] = repair(body(i))
        self.name_trans = name_trans

    def set_basic_factor(self, factor: list):
        """设置基本元"""
        self.factor_compute.set_basic_factor(factor)

    def add_basic_factor(self, factor):
        """添加基本元"""
        self.factor_compute.add_basic_factor(factor)

    def remove_basic_factor(self, factor):
        """删除基本元"""
        self.factor_compute.remove_basic_factor(factor)

    def get_basic_factor(self):
        """获取基本元"""
        return self.factor_compute.get_basic_factor()

    def set_basics_trans(self, name_trans: dict):
        """设置名称转换字典"""
        self.name_trans = name_trans

    def add_basics_trans(self, name, trans_name):
        """添加名称转换"""
        self.name_trans[name] = trans_name

    def remove_basics_trans(self, name):
        """删除名称转换"""
        del self.name_trans[name]

    def compute_factor(self, factor: str):
        """因子计算"""
        self.factors.append(factor)

        factor_trans = repair(body(factor))
        self.factor_ftrans_map[factor] = factor_trans

        value = self.factor_compute.compute(factor)
        self.factor_value_map[factor] = value
        self.ftrans_value_map[factor] = value
        self.factor_compute.remove_value()  # 计算完因子后将除基本元以外的数据删除，避免影响新因子计算的效率
        return value

    def get_local_basics_data(self, data: dict):
        """获取本地基本元数据"""
        for name in data:
            if name in self.name_trans:
                trans_name = self.name_trans[name]
                self.factor_compute.set_value(trans_name, data[name])

            elif name in self.name_trans.values():
                self.factor_compute.set_value(name, data[name])
