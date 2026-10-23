FROM python:3.11-slim

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/locationtime && echo ${TZ} > /etc/timezone

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["python", "-m", "app.bot"]