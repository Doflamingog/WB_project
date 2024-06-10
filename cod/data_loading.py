import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(filepath):
    logging.info('Загрузка данных из CSV файла')
    df = pd.read_csv(filepath)
    return df

def log_unique_counts(df):
    logging.info(f"Уникальные user_id: {df.user_id.nunique()}")
    logging.info(f"Уникальные item_id: {df.item_id.nunique()}")
