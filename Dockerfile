# Использование базового образа Miniconda, поддерживающего ARM
FROM continuumio/miniconda3:4.9.2

# Установка PDM
RUN curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python -

# Добавление PDM в PATH
ENV PATH="/root/.local/bin:${PATH}"

# Копирование файлов проекта
COPY . /app

# Установка рабочей директории
WORKDIR /app

# Установка зависимостей проекта
RUN pdm install

# Установка LightFM через conda
RUN conda install -c conda-forge lightfm

# Запуск основного Python скрипта
CMD ["pdm", "run", "python", "cod/main.py"]

