############################################
### 該当アンケートのデータから街の特徴を分析します。 ###
############################################

import pandas as pd
import MeCab

# 該当アンケートのデータ
survey = pd.read_csv("survey.csv")

# データ整形 #
survey = survey.dropna()
survey["comment"] = survey["comment"].str.replace("\(.+?\)", "", regex=True)    # 括弧内は補助的な情報であり、重要度は低いため除去
survey["comment"] = survey["comment"].str.replace("\（.+?\）", "", regex=True)  # 全角も同じく除去


# 形態素解析 #  (survey.csvを元にワードリスト作成)
tagger = MeCab.Tagger()
del_words = ["の"]     # ワードリストに含まない"除去ワードリスト"を作成
parts = ["名詞"]
all_words = []
satisfaction = []
for i in range(len(survey)):
    text = survey["comment"].iloc[i]
    words = tagger.parse(text).splitlines()
    words_arr = []
    for j in words:
        if j == "EOS" or j == "": continue
        word_tmp = j.split()[0]
        part = j.split()[1].split(",")[0]
        if not (part in parts):continue
        if word_tmp in del_words:continue
        words_arr.append(word_tmp)
        satisfaction.append(survey["satisfaction"].iloc[i])
    all_words.extend(words_arr)


# 頻出単語と顧客満足度を集計し、csv化(単語は3つ以上カウントされたもの)
all_words_df = pd.DataFrame({"words":all_words, "satisfaction":satisfaction, "count":len(all_words)*[1]})
words_satisfaction = all_words_df.groupby("words").mean()["satisfaction"]
words_count = all_words_df.groupby("words").sum()["count"]
words_df = pd.concat([words_satisfaction.round(1), words_count], axis=1)
words_df = words_df.loc[words_df["count"]>=3].sort_values("satisfaction", ascending=False)

words_df.to_csv("result1/satisfaction.csv")