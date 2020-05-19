#################################
### 輸送ルート最適化の制約条件を定義 ###
#################################

import numpy as np
import pandas as pd

# 輸送ルートデータ
df_tr_fut = pd.read_csv('./Trans_Route/trans_cost_fut.csv', index_col="工場")
df_demand = pd.read_csv('./Trans_Route/demand.csv')
df_supply = pd.read_csv('./Trans_Route/supply.csv')

# 制約条件計算関数
# 需要側
def condition_demand(df_tr_fut,df_demand):
    flag = np.zeros(len(df_demand.columns))
    for i in range(len(df_demand.columns)):
        temp_sum = sum(df_tr_fut[df_demand.columns[i]])
        if (temp_sum>=df_demand.iloc[0][i]):
            flag[i] = 1
    return flag

# 供給側
def condition_supply(df_tr_fut,df_supply):
    flag = np.zeros(len(df_supply.columns))
    for i in range(len(df_supply.columns)):
        temp_sum = sum(df_tr_fut.loc[df_supply.columns[i]])
        if temp_sum<=df_supply.iloc[0][i]:
            flag[i] = 1
    return flag

print("需要条件計算結果:"+str(condition_demand(df_tr_fut,df_demand)))
print("供給条件計算結果:"+str(condition_supply(df_tr_fut,df_supply)))