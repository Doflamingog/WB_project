FROM continuumio/miniconda3:4.9.2

RUN curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python -

ENV PATH="/root/.local/bin:${PATH}"

COPY . /app

WORKDIR /app

RUN pdm install

RUN conda install -c conda-forge lightfm

CMD ["pdm", "run", "python", "cod/main.py"]

