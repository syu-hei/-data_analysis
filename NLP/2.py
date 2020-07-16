############################################
### 該当アンケートのデータから街の特徴を分析します。 ###
############################################

### 満足度の高い単語(子育て)が含まれるコメント(子育て支援が嬉しい)を元に、それに類似するコメントを見つけます。 ###


import numpy as np
import pandas as pd
import MeCab

# 該当アンケートのデータ
survey = pd.read_csv("survey.csv")

# データ整形 #
survey = survey.dropna()
survey["comment"] = survey["comment"].str.replace("\(.+?\)", "", regex=True)    # 括弧内は補助的な情報であり、重要度は低いため除去
survey["comment"] = survey["comment"].str.replace("\（.+?\）", "", regex=True)  # 全角も同じく除去


# 形態素解析 # survey.csvを元にワードリスト作成
tagger = MeCab.Tagger()
parts = ["名詞"]
all_words_df = pd.DataFrame()
satisfaction = []
for n in range(len(survey)):
    text = survey["comment"].iloc[n]
    words = tagger.parse(text).splitlines()
    words_df = pd.DataFrame()
    for i in words:
        if i == "EOS" or i == "": continue
        word_tmp = i.split()[0]
        part = i.split()[1].split(",")[0]
        if not (part in parts):continue
        words_df[word_tmp] = [1]
    all_words_df = pd.concat([all_words_df, words_df] ,ignore_index=True)
all_words_df = all_words_df.fillna(0)


# 気になるコメント("子育て支援が嬉しい")
target_text = all_words_df.iloc[2]

# コサイン類似度計算
cos_sim = []
for i in range(len(all_words_df)):
    cos_text = all_words_df.iloc[i]
    cos = np.dot(target_text, cos_text) / (np.linalg.norm(target_text) * np.linalg.norm(cos_text))
    cos_sim.append(cos)
all_words_df["cos_sim"] = cos_sim

# 類似度の高い順に集計し、csv化
all_words_df = all_words_df.sort_values("cos_sim",ascending=False)
all_words_df.to_csv("result2/similar_comment.csv")

# 類似度の高い順にコメントを表示
print(survey["comment"].iloc[2])
print(survey["comment"].iloc[24])
print(survey["comment"].iloc[15])
print(survey["comment"].iloc[33])