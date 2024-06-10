import pandas as pd
import logging
from datetime import timedelta
import csv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def process_user_data(df,output_file):
    logging.info('Обработка данных пользователей')
    df.sort_values(by=['user_id', 'order_ts'], inplace=True)
    df['time_diff'] = df.groupby('user_id')['order_ts'].diff().dt.days
    average_days = df.groupby('user_id')['time_diff'].mean().reset_index()
    user_df = df.groupby(df['user_id'])['order_ts'].agg(['min', 'max']).reset_index().rename(columns={'min': 'first_date', 'max': 'last_date'})
    user_df = user_df.merge(average_days, how='left', on='user_id')
    user_df['time_diff'] = user_df['time_diff'].round(1)
    user_df.to_csv(output_file,index = False)
    logging.info(f'Данные пользователей записаны в {output_file}')

    return user_df

def process_item_data(df,output_file):
    logging.info('Обработка данных товаров')
    item_df = df.groupby(df['item_id'])['order_ts'].agg(['min', 'max']).reset_index().rename(columns={'min': 'first_date', 'max': 'last_date'})
    item_df.to_csv(output_file,index = False)
    logging.info(f'Данные товаров записаны в {output_file}')
    return item_df

def filter_data_by_date(df, days_back=20):
    last_days_in_df = df['date'].max()
    last_days_in_train = last_days_in_df - timedelta(days=days_back)
    test_df = df[df['date'] > last_days_in_train]
    df = df[df['date'] <= last_days_in_train]
    return df, test_df
