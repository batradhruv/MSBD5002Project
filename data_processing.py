import pandas as pd
import os
import sys
from sklearn import preprocessing

def combine_files():
    files = os.listdir(dir)
    for fid in range(len(files)):
        path = dir + files[fid]
        data = pd.read_csv(path)
        df1 = data[columns]
        df1 = df1.dropna()
        if fid == 0:
            df = df1
            continue
        df = df.append(df1, ignore_index=True)
    return df

def preprocess(df):
    df['c_count'] = df.groupby('CUST_CODE')['CUST_CODE'].transform('count')
    df = df[df['c_count'] > 50]
    df = df[df['c_count'] < 2500]

    df['t_count'] = df.groupby('PROD_CODE')['PROD_CODE'].transform('count')
    df = df[df['t_count'] < 2000]
    df = df.drop(['c_count', 't_count'], axis=1)

    df["CUST_label"] = le.fit_transform(df["CUST_CODE"])
    df["PROD_CODE"] = le.fit_transform(df["PROD_CODE"])
    return df

def train_test_split(df, num):
    num_train = int(num * 0.7)
    num_valid = int(num * 0.8)

    df_train = df[df["CUST_label"] < num_train].drop(columns="CUST_label")
    df_train = df_train.groupby(['CUST_CODE', 'SHOP_DATE'], as_index=True)['PROD_CODE'].apply(list)
    df_train.groupby(['CUST_CODE']).apply(list).to_json(r'..\data\dh_train.json', orient="index")

    df_valiadte = df[(df["CUST_label"] >= num_train) & (df["CUST_label"] < num_valid)].drop(columns="CUST_label")
    df_valiadte = df_valiadte.groupby(['CUST_CODE', 'SHOP_DATE'], as_index=True)['PROD_CODE'].apply(list)
    df_valiadte.groupby(['CUST_CODE']).apply(list).to_json(r'..\data\dh_valid.json',orient="index")

    df_test = df[df["CUST_label"] >= num_valid].drop(columns="CUST_label")
    df_test = df_test.groupby(['CUST_CODE', 'SHOP_DATE'], as_index=True)['PROD_CODE'].apply(list)
    df_test.groupby(['CUST_CODE']).apply(list).to_json(r'..\data\dh_test.json',orient="index")
    #combined json files manually
    return


if __name__ == '__main__':
    dir = './dunnhumby_5K/'
    le = preprocessing.LabelEncoder()
    columns = ["SHOP_DATE", "PROD_CODE", "CUST_CODE"]
    df = combine_files()
    df = preprocess(df)
    num_cust = len(df["CUST_CODE"].unique())
    train_test_split(df, num_cust)
