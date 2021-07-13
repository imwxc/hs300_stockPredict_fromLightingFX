from data_utils import *


# -------------------参数配置----------------- #
class Arg:
    def __init__(self):
        # tushare相关参数
        self.token='d7ec361542dc1140a1d15e7de5f1f3469da6837cd344bacd6f92a0e4'
        # 模型存放路径
        self.train_model_dir = './checkpoints/'
        # fining-turn模型存放路径
        self.fining_turn_model_dir = './checkpoints/finet/'
        # 训练图存放路径
        self.train_graph_dir = './logfile\\rain\\'
        # 验证loss存放路径
        self.val_graph_dir = './logfile\\val\\'
        # 模型名称
        self.model_name = 'model_test1'
        self.model_name_ft = 'model-ft-01-03'
        self.rnn_unit = 128     # 隐层节点数
        self.input_size = 6     # 输入维度（既用几个特征） 无需改动
        self.output_size = 6    # 输出维度（既使用分类类数预测） 无需改动
        self.layer_num = 3      # 隐藏层层数
        self.lr = 0.0006         # 学习率
        self.time_step = 10     # 时间步长
        self.epoch = 200        # 训练次数
        self.epoch_fining = 30  # 微调的迭代次数
        self.batch_size = 1024  # batch_size
        self.ratio = 0.8        # 训练集验证集比例
