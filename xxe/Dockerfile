FROM php:7.4-apache
WORKDIR /var/www/html

# Étape CLÉ : Installer les dépendances système pour l'extension XML
RUN apt-get update && \
    apt-get install -y libxml2-dev && \
    rm -rf /var/lib/apt/lists/*

# Installer l'extension XML (maintenant que les dépendances sont là)
RUN docker-php-ext-install xml

COPY index.php .
