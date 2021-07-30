import os
import sys
import numpy as np
import glob
import json
import boto3
import tabloo
import botocore
import matplotlib
import pandas as pd
import pandasql as ps
from pandasgui import show
from functools import reduce
import matplotlib.pyplot as plt
from IPython.display import display
from dynamodb_json import json_util as json


S3_BUCKET = "vitesco-data-ops-assignment-2021"
path_local = "C:/Users/furqu/Documents/GitHub/data-ops-assignment/data"
path_aws = "s3:/"+S3_BUCKET+".s3-website-ap-us-east-1.amazonaws.com"
df_all_csv = []
s3 = boto3.resource('s3')
all_files = glob.glob(path_local+"/plant/plant_data_0*.csv")

######################    READING PLANT DATA FROM S3  #########################
#Mock Reading of all CSVs from S3 Bucket
# prefix_objs = S3_BUCKET.objects.filter(Prefix="plant/plant_data_0*.csv")
# prefix_df = []
# for obj in prefix_objs:
#     key = obj.key
#     body = obj.get()['Body'].read()
#     temp = pd.read_csv(io.BytesIO(body), encoding='utf8')
#     prefix_df.append(temp)

#Read CSVs locally
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df_all_csv.append(df)

plants_df = pd.concat(df_all_csv, ignore_index=True)
df.id.astype(str)


#####################    READING USERS DATA FROM DynamoDB  ###############
#Mock Reading of DynamoDB Data
# def query_movies(year, dynamodb=None):
#     if not dynamodb:
#         dynamodb = boto3.client('dynamodb', region_name='us-east-1')
#
#     table = dynamodb.Table('vitesco-users')
#     response = table.query(
#         KeyConditionExpression=Key('id')
#     )
#     return response['Items']
#
# users = query_movies(query_id)
# users_df = pd.DataFrame(json.loads(users))\

#Reading users.json locally
users_df = pd.read_json(path_local+"/user/users.json")
df.id.astype(str)

######################    READING DEFECTS DATA FROM XLSX  #########################
defects_df = pd.read_excel(path_local+"/defects/defects.xlsx")

merged_df = pd.merge(plants_df, defects_df, how='inner', left_on=['part_id'], right_on=['part_id'])
merged_final_df = pd.merge(merged_df, users_df, how = 'inner', left_on='buyer_id', right_on='id')

df1 = merged_final_df.drop(["product_id", 'part_color_y','id_y'], axis=1)
df2 = df1.rename(columns={"id_x": "product_id", "part_color_x": "part_color"})

mean = df2["temperature"].mean()
model_count = ps.sqldf("select count(distinct car_model) from plants_df")

faulty_parts = ps.sqldf("select * from plants_df a left join defects_df b on a.part_id = b.part_id ")

df3 = ps.sqldf("""
select
c.part_color,
count(distinct car_model)
--car_color,
from plants_df a
join defects_df b
on a.part_id = b.part_id
join users_df c
on b.buyer_id = c.id
group by 1
""")

#print(matplotlib.colors.cnames["purple"])
#print(model_count)
tabloo.show(df2)
#show(df2)

#print(type(df2))
#display(df2)
#print(df2.columns)
#print(merged_final_df[''])
#df = pd.DataFrame(df_all_csv,columns=['id','production_date','car_model','car_color','part_id','part_color','part_material','plant_location','temperature','humidity','pressure'])
#print(df)
#df_all_csv.head(1)
