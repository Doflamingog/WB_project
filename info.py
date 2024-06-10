#Основные переменные

path_to_in = "data/wb_school_task_1.csv"
path_to_out = 'data/recommendations.csv'
path_to_new_df = 'data/df_with_fich.csv'
path_to_user = "data/user.csv"
path_to_item = "data/item.csv"
days_for_test = 20

#Переменные для подбора гиперпараметров
do_tune = False
path_to_hyperparams = "data/best_hyperparameters.json"
for_test = 0.2
components = [10, 30, 50]
learning_rates = [0.01, 0.05, 0.1]
loss_functions = ['logistic', 'bpr', 'warp', 'warp-kos']

#Есть ли у нас уже готовые user_df и item_df или мы хотим создать

read = False
create = True

path_to_read_user = "data/user.csv"
path_to_read_item = "data/item.csv"