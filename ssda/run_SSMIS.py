# SSMIS 実行スクリプト

from simssda import SimSSDA
from clnw import CLNetwork

from alg_SSMIS import SSMIS
name="SSMIS"
arg_nw_name="grid"
arg_nw_size="4x4"
arg_lvinit="random"
arg_rseed="1"

# パラメータ
simparams = {
    'topology':     arg_nw_name,  # ネットワーク名
    'nprocs':       arg_nw_size,  # ネットワークサイズパラメータ
    'proc_arrange': 'ascend',  # ダミー値
    'init_procs':   [],        # ダミー値
    'link_delay':   0.0,       # ダミー値
    'ordering':     None       # ダミー値
}
nw = CLNetwork.generate(simparams, 'any-bidir')

ssalg_class = globals()[name]
desc = ssalg_class.get_name()

# シミュレータ
s = SimSSDA(ssalg_class, nw,
            duration = None,
            how_init = arg_lvinit,
            rseed = arg_rseed)
# 実行
s.start(None)

