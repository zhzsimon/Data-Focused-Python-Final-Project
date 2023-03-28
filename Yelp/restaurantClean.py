"""
By: Xueting Meng and Ruidi Chang

This file clean the detail page data

This file creates detailPage_clean.csv containing cleaned restaurant detail page information

"""
import pandas as pd
import numpy as np
import os

def cleandetail():
    in_path = "./Yelp/data_completed/"
    data_path = "./Yelp/data_scrape/"
    out_path = os.path.join(data_path, 'detailPage_clean.csv')
    detailpage_path = os.path.join(in_path, 'detailPage.csv')

    df=pd.read_csv(detailpage_path,encoding='utf-8')
    # If the price column is words other than '$', put the value to 'NULL'
    for i in range(0,len(df.index)):
        if df.iloc[i,2]!='$$$$' and df.iloc[i,2]!='$$$' and df.iloc[i,2]!='$$' and df.iloc[i,2]!='$':
            df.iloc[i,2]='NULL'

    # Reference Yelp's price per-capita standards, make the price column more readable
    df['Price'].replace(['$$$$','$$$','$$','$'],['Splurge, Above 61','Spendy, 31 to 60','Moderate, 11 to 30','Cheap, Under 10'],inplace =True)
    # Only keep the numbers
    df['Review_new']=df['Review_num'].str.split(" ",expand=True)[0]
    # Only keep the numbers
    df['Star_new']=df['Star'].str.split(" ",expand=True)[0]
    # Only keep the useful information
    df['Need']=df['Address'].str.split("\'Location & Hours\', \'",expand=True)[1]
    # Find the address part
    df['Address_new']=df['Need'].str.split("\', \'",expand=True)[0]
    # Delete unnecessary information
    df['Address_new']=df['Address_new'].str.split("Get directions",expand=True)[0]
    # Find open time part
    df['OpenTime_new']=df['Need'].str.split("\', \'",expand=True)[2]
    # Find the Amentities part
    df['Amentities']=df['Need'].str.split("\'Amenities and More\', ",expand=True)[1]
    df['Amentities']=df['Amentities'].str.split(", \'Ask the Community\'",expand=True)[0]
    # Drop no needed column
    df=df.drop(['Review_num','Star','Address','Time','Need'],axis=1)
    # Clean the open time column
    df['OpenTime_new']=df['OpenTime_new'].str.split("Edit business info",expand=True)[0]

    # Delete unnecessary character of the menupage link column
    for i in range(0,len(df.index)):
        if df.iloc[i,4]!='':
            df.iloc[i,5]=str(df.iloc[i,5]).replace('[\'','')
            df.iloc[i,5]=str(df.iloc[i,5]).replace('\']','')
            df.iloc[i,5]=str(df.iloc[i,5]).replace('[\"','')
            df.iloc[i,5]=str(df.iloc[i,5]).replace('\"]','')

    # Delete unnecessary character of the address column
    for i in range(0,len(df.index)):
        if df.iloc[i,3]!='':
            df.iloc[i,3]=str(df.iloc[i,3]).replace('[\'','')
            df.iloc[i,3]=str(df.iloc[i,3]).replace('\']','')
            df.iloc[i,3]=str(df.iloc[i,3]).replace('[\"','')
            df.iloc[i,3]=str(df.iloc[i,3]).replace('\"]','')
    for i in range(0,len(df.index)):
        if df.iloc[i,3]!='':
            df.iloc[i,3]=str(df.iloc[i,3]).replace("\\n",',')
            df.iloc[i,3]=str(df.iloc[i,3]).replace("[]",'')

    # Delete unnecessary words of the open time column
    for i in range(0,len(df.index)):
        if df.iloc[i,9]!='':
            df.iloc[i,9]=str(df.iloc[i,9]).replace(" (Next day)",'')
            df.iloc[i,9]=str(df.iloc[i,9]).replace("Closed now\\n",'')

    # only keep the dish name of the menu column
    for i in range(0,len(df.index)):
        if(df.iloc[i,3]!=''):
            a=str(df.iloc[i,3]).split(",")
            df.iloc[i,3] = ''
            b=len(a)
            for j in range(0,b):
                if a[j][0] == '$':
                    a[j] = ''
                elif a[j][0].isdigit():
                    a[j] = ''
            a = [i for i in a if i != '']
            for k in range(0,len(a)):
                if k != len(a) - 1:
                    df.iloc[i, 3] = df.iloc[i,3] + a[k] + ','
                else:
                    df.iloc[i, 3] = df.iloc[i, 3] + a[k]

    df.to_csv(out_path,index=False,encoding='utf-8')


if __name__ == '__main__':
    cleandetail()