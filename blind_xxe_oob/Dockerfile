FROM python:3.9-slim
WORKDIR /app
COPY app.py .
COPY requirements.txt .

# Ajout des dépendances système pour compiler lxml
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Suppression des dépendances de compilation (pour garder l'image petite)
RUN apt-get purge -y --auto-remove build-essential libxml2-dev libxslt1-dev

EXPOSE 80
CMD ["python", "app.py"]
