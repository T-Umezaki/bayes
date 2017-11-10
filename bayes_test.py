# coding:utf-8
from bayes import BayesianFilter

bf = BayesianFilter()
# テキストを学習
bf.fit("激安セール - 今日だけ三割引", "pr")
bf.fit("クーポンプレゼント&送料無料", "pr")
bf.fit("店内改装セール実地中", "pr")
bf.fit("美味しくなって再登場", "pr")
bf.fit("本日の予定の確認です。", "imp")
bf.fit("プロジェクトの進捗確認をお願いします。","imp")
bf.fit("打合せよろしくお願いします。","imp")
bf.fit("会議の議事録です。","imp")
# 予測
pre, scorelist = bf.predict("激安、在庫一掃セール、送料無料")
print("result=", pre)
print(scorelist)
pre, scorelist = bf.predict("ようこそ、わが社へ")
print(u"result=", pre)
print(scorelist)
