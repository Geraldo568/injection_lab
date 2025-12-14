FROM python:3.9-slim
WORKDIR /app
COPY app.py .
COPY requirements.txt .

# Copier le dossier du package malveillant dans le conteneur.
COPY internal-logger /app/internal-logger

# VULNÉRABILITÉ : pip installe le paquet malveillant
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
CMD ["python", "app.py"]
