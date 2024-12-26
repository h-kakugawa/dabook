# 自己安定分散アルゴリズム
# 各プロセス pi の記述

class SS_Algorithm():

    # ネットワーク情報
    pid = None        # プロセス識別子
    procs = None      # プロセス配列
    neighbors = None  # 隣接プロセス集合 (プロセス識別子の集合)

    # 局所変数
    # ...

    def __init__(self, pid, neighbors, procs, how_init = None):
        # ネットワーク情報
        self.pid       = pid
        self.procs     = procs
        self.neighbors = neighbors
        self.init_local_state(how_init)

    # 局所変数の初期化
    def init_local_state(self, how_init):
        pass # ...

    # 全局所変数の値のリスト 
    def state(self):
        return 0 # ...

    # 自己安定分散アルゴリズム  本体
    # ガード付きコマンドの形による記述
    #  action == 'EVAL-GUARD' のとき:
    #   - ガードの値が真の規則番号(>0) (存在する場合) を(ひとつだけ)返す 
    #   - そのようなガードが存在しなければ 0 を返す
    #  action == 'EXEC-COMMAND' のとき:
    #   - ガードの値が真の規則を実行する
    def guarded_command(self, action):
        return 0 # ...
