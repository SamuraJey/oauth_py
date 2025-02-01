FROM python:3.13-slim
WORKDIR /usr/
COPY . .

RUN pip install poetry --no-cache-dir && \
	poetry install

EXPOSE 8080
CMD ["poetry", "run", "python", "src/run.py"]