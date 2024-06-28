import pandas as pd
import datetime

df=pd.read_json(r'E:\Data Science\PF\Datasets\Yelp\review1.json', lines=True)

def transform_reviews(df):
    #Nos quedamos con las columnas que nos interesan
    df=df[['review_id','business_id','user_id','stars','useful','text','date']]

    #Nos quedamos con los reviews que estan entre los años 2016 y 2021q
    df['date']=pd.to_datetime(df['date'])
    df=df[(df['date']>='2016-01-01') & (df['date']<='2021-12-31')]
    return df

df=transform_reviews(df)
print(df.columns)