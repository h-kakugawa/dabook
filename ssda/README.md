# 分散アルゴリズムシミュレータ/状態通信モデル

自己安定分散アルゴリズムのシミュレータです．

## 第11章: 自己安定

### 第11.2節: SSMIS - Shuklaらの極大独立集合アルゴリズム

- ssda/alg_SSMIS.py
  * アルゴリズムSSMISの実装．
  * 以降，ファイルalg_XXX.pyはアルゴリズムXXXを実装したファイルです．
- ssda/run_SSMIS.py
  * アルゴリズムSSMISを実行するためのスクリプト．
  * 以降，ファイルrun_XXX.pyはアルゴリズムXXXを実行するためのスクリプトです．
  * 実行はコマンドラインで以下の通りにします．他のrun_XXX.pyでも同様です．
```sh
$ python3 run_SSMIS.py
```

### 第11.3節: SSCOL - Hedetniemiらの彩色アルゴリズム
- ssda/alg_SSCOL.py
- ssda/run_SSCOL.py

### 第11.4節: SSTR_HC - Huang&ChenのBFS木アルゴリズム
- ssda/alg_SSTR_HC.py
- ssda/run_SSTR_HC.py

### 第11.5節: SSTR_AG - Arora&GoudaのBFS木アルゴリズム
- ssda/alg_SSTR_AG.py
- ssda/run_SSTR_AG.py

### シミュレーター本体
- ssda/simssda.py
  * シミュレーターコア部分．

### 自己安定分散アルゴリズム記述のテンプレート
- ssda/alg_SS.py

### ネットワーク部
- ssda/network.py
  * ネットワーク親クラス．
- ssda/nw_grid.py
  * グリッドの実装．
- ssda/nw_complete.py
  * クリークの実装．
- ssda/nw_file.py
  * 外部ファイル(DIMACSフォーマット)指定の実装．
- ssda/dimacs.py
  * DIMACSフォーマットのファイルのリーダー．
- ssda/pidmap.py
  * プロセス識別子の順序の変更．
