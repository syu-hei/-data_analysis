######################################
### 最適化を行った製造プランから得る利益 #####
######################################

import pandas as pd
from pulp import LpVariable, lpSum, value
from ortoolpy import model_max, addvars, addvals

# 製品製造に必要な原料のデータ
df_material = pd.read_csv('./Product_Plan/product_plan_material.csv', index_col="製品")
# 製品の利益
df_profit = pd.read_csv('./Product_Plan/product_plan_profit.csv', index_col="製品")
# 原料の在庫
df_stock = pd.read_csv('./Product_Plan/product_plan_stock.csv', index_col="項目")
# 製品の生産量
df_plan = pd.read_csv('./Product_Plan/product_plan.csv', index_col="製品")


df = df_material.copy()
inv = df_stock

m = model_max()
v1 = {(i):LpVariable('v%d'%(i),lowBound=0) for i in range(len(df_profit))}
m += lpSum(df_profit.iloc[i]*v1[i] for i in range(len(df_profit)))
for i in range(len(df_material.columns)):
    m += lpSum(df_material.iloc[j,i]*v1[j] for j in range(len(df_profit)) ) <= df_stock.iloc[:,i]
m.solve()

df_plan_fut = df_plan.copy()
for k,x in v1.items():
    df_plan_fut.iloc[k] = value(x)

df_plan_fut.to_csv("./Product_Plan/product_plan_fut.csv")

print("総利益:"+str(value(m.objective)))