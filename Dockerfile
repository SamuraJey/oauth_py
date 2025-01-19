FROM python:3.13-slim
WORKDIR /usr/src/app
COPY . .

RUN pip install --upgrade pip && \
	pip install poetry && \
	poetry install

EXPOSE 8080
CMD ["poetry", "run", "python", "app.py"]