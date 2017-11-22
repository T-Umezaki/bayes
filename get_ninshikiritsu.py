# -*- coding: utf-8 -*-

# Pandasをインポート
import pandas as pd
import os
import difflib
import unicodedata
# import codecs

# 設定
_DIR = "C:\\Users\\Takeshi_Umezaki\\Documents\\ocr\\_kari\\"
_RESULT_FILE_NAME = "results_detail.txt"
_CORRECT_FILE_NAME = "karisinsa.csv"
_EVIDENCE_FILE_NAME = "evidence.csv"


# 読み込みは全角数字になってしまうので半角にする。対象外のみ選択
def hankaku(column_name, str_value):
    str_return_value = str_value
    if column_name not in ["お取引店", "住所１", "住所２"]:
        str_return_value = unicodedata.normalize('NFKC', str_value)
    return str_return_value


if __name__ == '__main__':
    print("start")
    os.chdir(_DIR)

    # 結果CSV
    df_result = pd.read_csv(_RESULT_FILE_NAME, encoding="cp932")
    # 結果CSV
    df_correct = pd.read_csv(_CORRECT_FILE_NAME, encoding="cp932")

    # 処理対象列名リスト
    l_columns = df_result.columns.values

    column_no = 0
    for column_name in l_columns:
        column_no += 1
        # 先頭の列はファイル名なので読み飛ばす
        if column_no == 1:
            continue
        print(column_name)
        if column_no == 2:
            df_evidence = pd.DataFrame(df_correct[column_name][0:200])
        else:
            df_evidence[column_name] = df_correct[column_name][0:200]
        column_r = column_name + "_R"
        df_evidence[column_r] = df_result[column_name][0:200]
        # 列追加。本当にこれしかない？
        column_d = column_name + "_D"
        df_evidence[column_d] = [1.000] * len(df_evidence.index)
        for index2, row in df_evidence.iterrows():
            str1 = str(row[column_name])
            str2 = str(row[column_r])
            str2 = hankaku(column_name, str2)
            diff_ratio = difflib.SequenceMatcher(None, str1, str2).ratio()
            df_evidence[column_d][index2] = diff_ratio

    df_evidence.to_csv(_EVIDENCE_FILE_NAME)    
