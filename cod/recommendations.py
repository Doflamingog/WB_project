import numpy as np
from concurrent.futures import ThreadPoolExecutor
import logging
import csv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def generate_recommendations_batch(user_ids, model, item_ids, n_rec=30):
    recommendations = {}
    for user_id in user_ids:
        user_id = int(user_id) if isinstance(user_id, (np.integer, np.int64)) else user_id
        scores = model.predict(user_id, item_ids, num_threads=1)
        top_items_indices = np.argsort(-scores)[:n_rec]
        recommendations[user_id] = item_ids[top_items_indices].tolist()
    return recommendations

def generate_all_recommendations(user_ids, model, item_ids, output_file, n_rec=30):
    user_id_batches = np.array_split(user_ids, 30)
    all_recommendations = {}

    logging.info('Генерация рекомендаций в баче')
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda batch: generate_recommendations_batch(batch, model, item_ids, n_rec), user_id_batches))

    for batch_result in results:
        all_recommendations.update(batch_result)

    # Save recommendations to a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['user_id', 'recommended_item_ids']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user_id, recommended_items in all_recommendations.items():
            writer.writerow({'user_id': user_id, 'recommended_item_ids': ','.join(map(str, recommended_items))})

    logging.info(f'Рекомендации сохранены в  {output_file}')

    return all_recommendations
