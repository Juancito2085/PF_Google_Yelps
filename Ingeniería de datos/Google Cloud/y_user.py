import pandas as pd

def transform_user(df):

    #Nos quedamos con las columnas que nos interesan
    df=df[['user_id','name','review_count','useful']]

    #Eliminamos las filas duplicadas
    df=df.drop_duplicates(keep='first')

    return df