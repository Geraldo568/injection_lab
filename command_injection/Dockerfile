FROM node:18-alpine

# Créer un répertoire de travail
WORKDIR /usr/src/app

# Copier le fichier de dépendances
COPY package.json .

# Installer les dépendances
RUN npm install

# Copier le fichier de l'application
COPY app.js .

# Exposer le port de l'application
EXPOSE 3002

# Commande de démarrage
CMD ["node", "app.js"]
