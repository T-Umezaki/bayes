# -*- coding: utf-8 -*-

# Pandasをインポート
import pandas as pd
import os
import unicodedata
import difflib
# import codecs

# 設定
_DIR = "C:\\Users\\Takeshi_Umezaki\\Documents\\ocr\\_kari\\"
_RESULT_FILE_NAME = "results_detail.txt"
_CORRECT_FILE_NAME = "karisinsa.csv"
_EVIDENCE_FILE_NAME = "evidence.csv"

if __name__ == '__main__':
    print("start")
    os.chdir(_DIR)

    # 結果CSV
    df_result = pd.read_csv(_RESULT_FILE_NAME, encoding="cp932")
    # 結果CSV
    df_correct = pd.read_csv(_CORRECT_FILE_NAME, encoding="cp932")

    # 処理対象列名リスト
    l_columns = df_result.columns.values

    index = 0
    for column_name in l_columns:
        if index == 0:
            index += 1
            continue
        print(column_name)
        df_evidence = pd.DataFrame(df_correct[column_name][0:200])
        column_r = column_name + "_R"
        print(column_r)
        df_temp = pd.DataFrame(df_result[column_name][0:200])
        df_temp.columns = [column_r]

        df_evidence = pd.concat([df_evidence, df_temp], axis=1)

        column_d = column_name + "_D"
        df_evidence[column_d] = df_evidence.apply(lambda x: difflib.SequenceMatcher(None, x[column_name], x[column_r]).ratio(), axis=1)
        break

    df_evidence.to_csv(_EVIDENCE_FILE_NAME)    
