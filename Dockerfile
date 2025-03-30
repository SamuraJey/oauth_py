FROM python:3.13-slim
WORKDIR /usr/
COPY poetry.lock pyproject.toml ./

RUN pip install poetry --no-cache-dir
RUN poetry install

COPY . .

EXPOSE 8080
# CMD ["poetry", "run", "python", "src/run.py"]