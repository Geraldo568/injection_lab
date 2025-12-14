FROM php:7.4-apache
WORKDIR /var/www/html

# Activer le module de réécriture (nécessaire pour certaines configurations)
RUN a2enmod rewrite

# Créer le répertoire d'upload et définir les permissions larges (vulnérable)
RUN mkdir uploads
RUN chown -R www-data:www-data uploads
RUN chmod -R 777 uploads

COPY index.php .
