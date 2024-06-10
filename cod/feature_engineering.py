import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_time_features(df,output_file):
    logging.info('Добавление новых временных признаков')
    df['order_ts'] = pd.to_datetime(df['order_ts'])
    df['year'] = df['order_ts'].dt.year
    df['month'] = df['order_ts'].dt.month
    df['day'] = df['order_ts'].dt.day
    df['week'] = df['order_ts'].dt.isocalendar().week
    df['hour'] = df['order_ts'].dt.hour
    df['date'] = df['order_ts'].dt.date
    df.to_csv(output_file,index = False)
    logging.info(f'Датасет с новыми признаками сохранен в {output_file}')

    return df
