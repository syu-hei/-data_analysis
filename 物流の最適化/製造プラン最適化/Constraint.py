#####################################
### 製造プラン最適化の制約条件を定義する ###
#####################################

import numpy as np
import pandas as pd


# 製品製造に必要な原料のデータ
df_material = pd.read_csv('./Product_Plan/product_plan_material.csv', index_col="製品")
# 製品の利益
df_profit = pd.read_csv('./Product_Plan/product_plan_profit.csv', index_col="製品")
# 原料の在庫
df_stock = pd.read_csv('./Product_Plan/product_plan_stock.csv', index_col="項目")
# 製品の生産量
df_plan_fut = pd.read_csv('./Product_Plan/product_plan_fut.csv', index_col="製品")

# 制約条件計算関数
def condition_stock(df_plan_fut, df_material, df_stock):
    flag = np.zeros(len(df_material.columns))
    for i in range(len(df_material.columns)):
        temp_sum = 0
        for j in range(len(df_material.index)):
            temp_sum = temp_sum + df_material.iloc[j][i]*float(df_plan_fut.iloc[j])
        if (temp_sum<=float(df_stock.iloc[0][i])):
            flag[i] = 1
        print(df_material.columns[i]+"  使用量:"+str(temp_sum)+", 在庫:"+str(float(df_stock.iloc[0][i])))
    return flag

print("制約条件計算結果:"+str(condition_stock(df_plan_fut, df_material, df_stock)))