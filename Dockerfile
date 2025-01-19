FROM python:3.13-slim
WORKDIR /usr/src/app
COPY . .
RUN apk add --no-cache make
RUN make init
EXPOSE 8080
CMD ["python", "app.py"]