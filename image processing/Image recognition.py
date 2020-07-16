######################################
### 2つの映像から人通りの変化を分析します。 ###
######################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2


# 映像から人を検出し移動人数を時系列化する関数
def people(mov, df):
    # 映像取得 #
    cap = cv2.VideoCapture(mov)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # hog宣言(人を認識させる) #
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    hogParams = {'winStride': (8, 8), 'padding': (32, 32), 'scale': 1.05, 'hitThreshold':0, 'finalThreshold':5}

    num = 0
    df = pd.DataFrame( columns=['time','people'] )
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            if (num%10==0):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                human, r = hog.detectMultiScale(gray, **hogParams)
                if (len(human)>0):
                    for (x, y, w, h) in human:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255,255,255), 3)
                tmp_se = pd.Series( [num/fps,len(human) ], index=df.columns )
                df = df.append( tmp_se, ignore_index=True )
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            break
        num = num + 1
    cap.release()
    cv2.destroyAllWindows()
    return df

# mov01とmov02の時系列データ作成
list_df = people("mov/mov01.avi", list())
list_df2 = people("mov/mov02.avi", list())


# ノイズ除去のための平均化関数
def moving_average(x, y):
    y_conv = np.convolve(y, np.ones(5)/float(5), mode='valid')
    x_dat = np.linspace(np.min(x), np.max(x), np.size(y_conv))
    return x_dat, y_conv

ma_x, ma_y = moving_average(list_df["time"], list_df["people"])
ma_x2, ma_y2 = moving_average(list_df2["time"], list_df2["people"])


# 平均化した時系列をグラフで表示
plt.plot(ma_x,ma_y, label="1st")
plt.plot(ma_x2,ma_y2, label="2nd")
plt.xlabel('time(sec.)')
plt.ylabel('population')
plt.ylim(0,15)
plt.legend()
plt.show()