import logging
from data_loading import load_data, log_unique_counts
from feature_engineering import create_time_features
from user_item_processing import process_user_data,process_item_data, filter_data_by_date
from model_training import create_interaction_matrix, train_lightfm_model, tune_hyperparameters
from recommendations import generate_all_recommendations
import os
import sys
import pandas as pd


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from info import path_to_in,path_to_out,days_for_test ,path_to_item,path_to_user,path_to_new_df,create,read,path_to_read_item,path_to_read_user,do_tune,path_to_hyperparams

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Загрузка данных
    df = load_data(path_to_in)
    log_unique_counts(df)

    # Создание временных признаков
    df = create_time_features(df,output_file= path_to_new_df)

    if create:
        user_df = process_user_data(df,output_file= path_to_user)
        item_id = process_item_data(df,output_file= path_to_item)
    if read:
        user_df = pd.read_to_csv(path_to_read_user)
        item_df = pd.read_to_csv(path_to_read_item)

    df, test_df = filter_data_by_date(df, days_back=days_for_test)

    # Создание матрицы взаимодействий и обучение модели
    interaction_matrix = create_interaction_matrix(df)
    model = train_lightfm_model(interaction_matrix)

    # Подбор гиперпараметров
    if do_tune:
        best_params = tune_hyperparameters(interaction_matrix,output_file= path_to_hyperparams)

    # Генерация рекомендаций
    user_ids = test_df['user_id'].unique()
    item_ids = df['item_id'].unique()
    all_recommendations = generate_all_recommendations(user_ids, model, item_ids, output_file= path_to_out)
    logging.info('Рекомендации сгенерированы')

if __name__ == "__main__":
    main()
