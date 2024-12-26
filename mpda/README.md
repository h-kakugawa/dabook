# 分散アルゴリズムシミュレータ/メッセージ伝達モデル

メッセージ伝達モデルの分散アルゴリズムシミュレータです．

## 第3章: フラッディング

### 3.2節: FL - フラディングアルゴリズム
- mpda/alg_FL.py
  * アルゴリズムFLの実装．
  * 以降，ファイルalg_XXX.pyはアルゴリズムXXXを実装したファイルです．
- mpda/run_FL.py
  * アルゴリズムFLを実行するためのスクリプト．
  * 以降，ファイルrun_XXX.pyはアルゴリズムXXXを実行するためのスクリプトです．
  * 実行はコマンドラインで以下の通りにします．他のrun_XXX.pyでも同様です．
```sh
$ python3 run_FL.py
```

### 3.3節: SP - 最短経路アルゴリズム
- mpda/alg_SP.py
- mpda/run_SP.py

## 第4章: ウェーブ

### 4.2節: WV_R - リングアルゴリズム
- mpda/alg_WV_R.py
- mpda/run_WV_R.py

### 4.3節: WV_P - ポーリングアルゴリズム
- mpda/alg_WV_P.py
- mpda/run_WV_P.py

### 4.4節: WV_E - エコーアルゴリズム
- mpda/alg_WV_E.py
- mpda/run_WV_E.py

## 第5章: リーダー選挙

### 5.2節: LE_L, LeLannのアルゴリズム
- mpda/alg_LE_L.py
- mpda/run_LE_L.py

### 5.3節: LE_CR, Chang&Robertのアルゴリズム
- mpda/alg_LE_CR.py
- mpda/run_LE_CR.py

### 5.4節: LE_P, Petersonのアルゴリズム
- mpda/alg_LE_P.py
- mpda/run_LE_P.py

## 第6章: 論理時計

### 6.2節: LC_SC, Lamportのスカラ論理時計アルゴリズム
- mpda/alg_LC_SC.py
- mpda/run_LC_SC.py

### 6.3節: LC_VC, Matternのベクトル論理時計アルゴリズム
- mpda/alg_LC_VC.py
- mpda/run_LC_VC.py

## 第7章: 相互排除

### 7.2節: MX_L, Lamportのアルゴリズム
- mpda/alg_MX_L.py
- mpda/run_MX_L.py

### 7.3節: MX_RA, Ricart&Agrawalaのアルゴリズム
- mpda/alg_MX_RA.py
- mpda/run_MX_RA.py

### 7.4節: MX_SK, 鈴木・嵩のアルゴリズム
- mpda/alg_MX_SK.py
- mpda/run_MX_SK.py

### 7.5節: MX_M, 前川のアルゴリズム
- mpda/alg_MX_M.py
- mpda/run_MX_M.py
- mpda/coterie.py
  * コータリークラスの定義．
- mpda/cot_maj.py
  * 多数決コータリーの実装．
- mpda/cot_grid.py
  * グリッドコータリーの実装．
- mpda/cot_fpp.py
  * 有限射影平面コータリーの実装．

## 第9章: スナップショット

### 9.2節: SN_CL, Chandy&Lamportのアルゴリズム
- mpda/alg_SN_CL.py
- mpda/run_SN_CL.py
- mpda/alg_sn_basic.py
  * 応用アルゴリズムクラスの定義．
- mpda/alg_if_sn.py
  * 局所スナップショット取得インターフェース定義．

## 第10章: 停止判定

### 10.2節: TD_DS, Dijkstra&Choltenのアルゴリズム
- mpda/alg_TD_DS.py
- mpda/run_TD_DS_SP.py
  * alg_SP_TD.pyを実行するためのスクリプト．
- mpda/run_TD_DS_WV_P.py
  * alg_WP_P.pyを実行するためのスクリプト．
- mpda/alg_if_td.py
  * 基本アルゴリズムインターフェース定義．

### 10.3節: TD_CR, Matternの債権回収アルゴリズム
- mpda/alg_TD_CR.py
- mpda/run_TD_CR_SP.py
  * alg_SP_TD.pyを実行するためのスクリプト．
- mpda/run_TD_CR_WV_P.py
  * alg_WP_P.pyを実行するためのスクリプト．

### 応用アルゴリズム用ラッパークラス
- mpda/alg_SP_TD.py
  * アルゴリズムSPへ適用するためのクラス
- mpda/alg_WV_P_TD.py
  * アルゴリズムWP_Pへ適用するためのクラス

## 離散事象シミュレータ(メッセージ伝達モデル)

### シミュレーター本体
- mpda/simulator.py
  * シミュレーターコア部分．
- mpda/process_if.py
  * プロセス実装クラスのインターフェース．
- mpda/algorithm.py
  * プロセス記述の親クラス．

### 分散アルゴリズム記述のテンプレート
- mpda/alg_TEMPLATE.py

### ネットワーク部
- mpda/network.py
  * ネットワーク親クラス．
- mpda/nw_ring_unidir.py
  * 単方向リングの実装．
- mpda/nw_grid.py
  * グリッドの実装．
- mpda/nw_complete.py
  * クリークの実装．
- mpda/nw_file.py
  * 外部ファイル(DIMACSフォーマット)指定の実装．
- mpda/dimacs.py
  * DIMACSフォーマットのファイルのリーダー．
- mpda/dim2dot.py
  * DIMACSフォーマットからDOT言語(Graphviz)へのコンバーター．
- mpda/pidmap.py
  * プロセス識別子の順序の変更．

## DIMACSフォーマットの外部ファイル例

### 例1
- mpda/g_sp_a_1.dat
- mpda/g_sp_a_1.dot
- mpda/g_sp_a_1.eps
- mpda/g_sp_a_1.pdf
- mpda/g_sp_a_1.png
- mpda/g_sp_a_1.svg

### 例2
- mpda/g_sn_cl_1.dat
- mpda/g_sn_cl_1.dot
- mpda/g_sn_cl_1.eps
- mpda/g_sn_cl_1.pdf
- mpda/g_sn_cl_1.png
- mpda/g_sn_cl_1.svg

### 例3
- mpda/g_td_1.dat
- mpda/g_td_1.dot
- mpda/g_td_1.eps
- mpda/g_td_1.pdf
- mpda/g_td_1.png
- mpda/g_td_1.svg
