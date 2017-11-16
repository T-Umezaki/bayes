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
        print(type(df_result[column_name][0:200]))
        print(len(df_evidence))
        # l1 = list(pd.DataFrame(df_result[column_name][0:200].valus.flatten()))
        # print(len(l1))
        df_evidence[column_r] = df_result[column_name][0:200]
        print(df_evidence.columns)
        # df_temp = pd.DataFrame(df_result[column_name][0:200])
        # df_temp.columns = [column_r]

        # df_evidence = pd.concat([df_evidence, df_temp], axis=1)
        print(type(df_evidence))
                
        # 列追加。本当にこれしかない？
        column_d = column_name + "_D"
        df_evidence[column_d] = [1] * len(df_evidence.index)
        print(df_evidence.columns)
        # df_evidence[column_d] = df_evidence.apply(lambda x: difflib.SequenceMatcher(None, x[column_name], x[column_r]).ratio(), axis=1)
        i = 0
        for index, row in df_evidence.iterrows():
            str1 = str(row[column_name])
            str2 = str(row[column_r])
            print(type(str1))
            diff_ratio = difflib.SequenceMatcher(None, str1, str2).ratio()
            df_evidence[column_d][index] = diff_ratio
            i += 1

        break
        #df_evidence[column_d] = ratio

    df_evidence.to_csv(_EVIDENCE_FILE_NAME)    
