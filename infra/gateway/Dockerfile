FROM python:3.12-slim
WORKDIR /app
COPY services /app/services
COPY web /app/web
RUN pip install --no-cache-dir kafka-python==2.0.2 psycopg[binary]==3.2.3
EXPOSE 8088
CMD ["python", "-m", "services.gateway"]
