##############################
### 現在の製造プランから得る利益 ###
##############################

import pandas as pd


# 製品製造に必要な原料のデータ
df_material = pd.read_csv('./Product_Plan/product_plan_material.csv', index_col="製品")
# 製品の利益
df_profit = pd.read_csv('./Product_Plan/product_plan_profit.csv', index_col="製品")
# 原料の在庫
df_stock = pd.read_csv('./Product_Plan/product_plan_stock.csv', index_col="項目")
# 製品の生産量
df_plan = pd.read_csv('./Product_Plan/product_plan.csv', index_col="製品")



# 利益計算関数
def product_plan(df_profit,df_plan):
    profit = 0
    for i in range(len(df_profit.index)):
        for j in range(len(df_plan.columns)):
            profit += df_profit.iloc[i][j]*df_plan.iloc[i][j]
    return profit

print("総利益:"+str(product_plan(df_profit,df_plan)))