FROM node:18-alpine
WORKDIR /usr/src/app
COPY package.json .
RUN npm install
COPY app.js .
EXPOSE 3003
CMD ["node", "app.js"]
