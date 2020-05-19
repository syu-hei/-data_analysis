###########################################
### 輸送コスト最適化を行った場合にかかる輸送コスト ###
###########################################

import numpy as np
import pandas as pd
from itertools import product
from pulp import LpVariable, lpSum, value
from ortoolpy import model_min, addvars, addvals

df_tc = pd.read_csv('./Trans_Cost/trans_cost.csv', index_col="工場")
df_demand = pd.read_csv('./Trans_Cost/demand.csv')
df_supply = pd.read_csv('./Trans_Cost/supply.csv')


# 初期設定 #
np.random.seed(1)
nw = len(df_tc.index)
nf = len(df_tc.columns)
pr = list(product(range(nw), range(nf)))

# 数理モデル作成 #
m1 = model_min()
v1 = {(i,j):LpVariable('v%d_%d'%(i,j),lowBound=0) for i,j in pr}

m1 += lpSum(df_tc.iloc[i][j]*v1[i,j] for i,j in pr)
for i in range(nw):
    m1 += lpSum(v1[i,j] for j in range(nf)) <= df_supply.iloc[0][i]
for j in range(nf):
    m1 += lpSum(v1[i,j] for i in range(nw)) >= df_demand.iloc[0][j]
m1.solve()

# 総輸送コスト計算 #
df_tr_fut = df_tc.copy()
total_cost = 0
for k,x in v1.items():
    i,j = k[0],k[1]
    df_tr_fut.iloc[i][j] = value(x)
    total_cost += df_tc.iloc[i][j]*value(x)

df_tr_fut.to_csv("./Trans_Cost/trans_cost_fut.csv")

print("総輸送コスト:"+str(total_cost))