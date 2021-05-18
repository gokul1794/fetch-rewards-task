# -*- coding: utf-8 -*-
"""
This python file, extracts, transforms and stores the data in a postgres database.
Created on Mon May 17 15:44:58 2021

@author: gokul
"""
import pandas as pd
import json

#This function reads the files
def readFiles(filename):
    with open(filename) as f:
        lines = f.readlines()
    df = []
    for line in lines:
        df.append(json.loads(line))
    return df

#Replace the file paths with your path - in hindsight this should've probably been relative 
brands = readFiles('D:\\Assesment\\fetch-rewards-task\\data\\brands.json')
users = readFiles('D:\\Assesment\\fetch-rewards-task\\data\\users.json')
receipts = readFiles('D:\\Assesment\\fetch-rewards-task\\data\\receipts.json')

#We first work with just users and brands json and normalize it.
usersdf = pd.json_normalize(users,max_level=1)
brandsdf = pd.json_normalize(brands,max_level=2)

#Renaming some columns and changing unix epoch time to a readable format
usersdf.rename(columns={'_id.$oid': 'user_id', 'createdDate.$date': 'createdDate', 'lastLogin.$date': 'lastLogin'}, inplace=True)
usersdf['createdDate'] = pd.to_datetime(usersdf['createdDate']/1000,unit='s')
usersdf['lastLogin'] = pd.to_datetime(usersdf['lastLogin']/1000,unit='s')

usersdf.to_csv(r'D:\Assesment\fetch-rewards-task\data\CleanFiles\users.csv',index=False)

#We repeat the above steps we did with Users json, to brands.
brandsdf.rename(columns={'_id.$oid': 'brand_id', 'cpg.$id.$oid': 'cpgOid', 'cpg.$ref': 'cpgRef'}, inplace=True)

#Data Quality check 1
#Dropping duplicate keys for brand_id's since I plan to use this as my primary key.
brandsdf = brandsdf.drop_duplicates(subset='brand_id').reset_index(drop=True)
brandsdf.to_csv(r'D:\Assesment\fetch-rewards-task\data\CleanFiles\brands.csv',index=False)

#Normalizing receipts
receiptsdf = pd.json_normalize(receipts)
receiptsdfUpper = receiptsdf.drop(['rewardsReceiptItemList'], axis=1)
receiptsdfUpper.rename(columns={'_id.$oid': 'receipt_id', 'createDate.$date': 'createDate', 'pointsAwardedDate.$date': 'pointsAwardedDate'}, inplace=True)
receiptsdfUpper['createDate'] = pd.to_datetime(receiptsdfUpper['createDate']/1000,unit='s')
receiptsdfUpper['pointsAwardedDate'] = pd.to_datetime(receiptsdfUpper['pointsAwardedDate']/1000,unit='s')
receiptsdfUpper.drop(['dateScanned.$date', 'finishedDate.$date',
       'modifyDate.$date','purchaseDate.$date'], axis=1,inplace=True)

receiptsdfUpper.to_csv(r'D:\Assesment\fetch-rewards-task\data\CleanFiles\receipts.csv',index=False)

#Inserting Barcode and Description as they're non null keys in my schema 
[item.update({'rewardsReceiptItemList':[{'barcode':None,'description':None}]}) for item in receipts if 'rewardsReceiptItemList' not in item.keys()]

#Normalizing the ReceiptItemList data
ReceiptItemList_df = pd.json_normalize(receipts, record_path='rewardsReceiptItemList',meta=[["_id","$oid"]])
ReceiptItemList_df.rename(columns={'_id.$oid': 'receipt_id'}, inplace=True)
#keeping columns I need
ReceiptItemList_df = ReceiptItemList_df[['receipt_id','barcode','description','finalPrice','itemPrice','brandCode']]

ReceiptItemList_df.to_csv(r'D:\Assesment\fetch-rewards-task\data\CleanFiles\receiptsItemList.csv',index=False)

