#############################################
### 輸送コストと生産コストをまとめて最適化設計します。 ###
#############################################

import numpy as np
import pandas as pd
from ortoolpy import logistics_network

製品 = list('AB')
需要地 = list('PQ')
工場 = list('XY')
レーン = (2,2)

# 輸送費表 #
tc = pd.DataFrame(((j,k) for j in 需要地 for k in 工場), columns=['需要地','工場'])
tc['輸送費'] = [1,2,3,1]


# 需要表 #
demand = pd.DataFrame(((j,i) for j in 需要地 for i in 製品), columns=['需要地','製品'])
demand['需要'] = [10,10,20,20]


# 生産表 #
product = pd.DataFrame(((k,l,i,0,np.inf) for k,nl in zip (工場,レーン) for l in range(nl) for i in 製品), 
                    columns=['工場','レーン','製品','下限','上限'])
product['生産費'] = [1,np.nan,np.nan,1,3,np.nan,5,3]
product.dropna(inplace=True)
product.loc[4,'上限']=10

# ロジスティックネットワークで最適化
_, tc2, _ = logistics_network(demand,tc,product)


# 総生産コスト
print(product)
product_cost = 0
for i in range(len(product.index)):
    product_cost += product["生産費"].iloc[i]*product["ValY"].iloc[i]
print("総生産コスト:"+str(product_cost))


# 総輸送コスト
print(tc2)
trans_cost = 0
for i in range(len(tc2.index)):
    trans_cost += tc2["輸送費"].iloc[i]*tc2["ValX"].iloc[i]
print("総輸送コスト:"+str(trans_cost))