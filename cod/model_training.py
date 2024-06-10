from scipy.sparse import csr_matrix
from lightfm import LightFM
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from info import for_test,components,learning_rates,loss_functions
from lightfm.cross_validation import random_train_test_split
from lightfm.evaluation import precision_at_k

import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levellevel)s - %(message)s')

def read_model_config(file_path='cod/model/model_config.json'):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


def create_interaction_matrix(df):
    logging.info('Создание матрицы взаимодействий')
    interaction_matrix = csr_matrix((df['user_id'].count() * [1], (df['user_id'], df['item_id'])))
    return interaction_matrix

def train_lightfm_model(interaction_matrix, epochs=30):
    logging.info('Обучение модели LightFM')
    model_config = read_model_config()
    model = LightFM(**model_config)
    model.fit(interaction_matrix, epochs=epochs)
    return model

def tune_hyperparameters(interactions,output_file, user_features=None, item_features=None, num_epochs=30):


    train, test = random_train_test_split(interactions, test_percentage= for_test)

    best_precision = 0
    best_params = {}

    logging.info('Начало подбора гиперпараметров')
    for component in components:
        for learning_rate in learning_rates:
            for loss in loss_functions:
                model = LightFM(no_components=component, learning_rate=learning_rate, loss=loss)
                model.fit(train, user_features=user_features, item_features=item_features, epochs=num_epochs, num_threads=2)
                precision = precision_at_k(model, test, k=10, user_features=user_features, item_features=item_features).mean()
                logging.info(f'Precision: {precision:.4f} with components: {component}, learning_rate: {learning_rate}, loss: {loss}')
                if precision > best_precision:
                    best_precision = precision
                    best_params = {
                        'no_components': component,
                        'learning_rate': learning_rate,
                        'loss': loss
                    }

    logging.info(f'Best precision: {best_precision:.4f}')
    logging.info(f'Best parameters: {best_params}')

    with open(output_file, 'w') as f:
        json.dump(best_params, f, indent=4)

    return best_params
