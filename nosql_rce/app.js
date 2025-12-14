const express = require('express');
const { MongoClient } = require('mongodb');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
const port = 80;

const MONGO_URL = 'mongodb://mongodb:27017';
const DB_NAME = 'nosql_rce_db';
const CLIENT = new MongoClient(MONGO_URL);

const RCE_FLAG_FILE = '/usr/src/app/rce_flag_8121.txt';

async function initDb() {
    try {
        await CLIENT.connect();
        const db = CLIENT.db(DB_NAME);
        const users = db.collection('users');

        await users.deleteMany({});
        await users.insertOne({ username: 'admin', password: 'ADMIN_PASSWORD_8121', secret: 'FLAG_NOSQL_RCE_SUCCESS' });
        await users.insertOne({ username: 'user', password: 'user123', secret: 'standard_user_data' });
        
        console.log("MongoDB initialized with admin and user accounts.");
    } catch (e) {
        console.error("Failed to initialize MongoDB:", e);
    }
}

initDb();

app.use(bodyParser.urlencoded({ extended: true }));

const HTML_TEMPLATE = `
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2ecc71; border-bottom: 2px solid #27ae60; padding-bottom: 10px; }
    .vulnerability-note { background-color: #2ecc71; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; }
    input[type="submit"] { background-color: #27ae60; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; }
    .result { margin-top: 20px; padding: 10px; border: 1px dashed #7f8c8d; }
    .error { color: #e74c3c; font-weight: bold; }
    .success { color: #2ecc71; font-weight: bold; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ CRITIQUE : NoSQL Injection (MongoDB) - RCE via $where - Port 8121</div>
<h1>Lab 42 - Connexion d'Administrateur</h1>

<p>
    Ce service effectue une requête MongoDB en construisant l'objet de requête à partir de l'entrée utilisateur non assainie, utilisant accidentellement l'opérateur <code>$where</code>.
</p>
<p>
    <b>Objectif :</b> Injecter un payload dans le champ 'username' pour exécuter la commande <code>touch ${RCE_FLAG_FILE}</code> sur le serveur MongoDB.
</p>

<form method="POST" action="/login">
    <label for="username">Nom d'utilisateur:</label>
    <input type="text" name="username" id="username" placeholder="Entrez votre nom d'utilisateur">
    <label for="password">Mot de passe:</label>
    <input type="password" name="password" id="password" placeholder="Mot de passe (non utilisé pour l'exploit)">
    <input type="submit" value="Se connecter">
</form>
`;

app.get('/', (req, res) => {
    res.send(HTML_TEMPLATE);
});

app.post('/login', async (req, res) => {
    const { username } = req.body;
    let message = '';

    if (!username) {
        message = '<p class="error">Veuillez entrer un nom d\'utilisateur.</p>';
    } else {
        try {
            const db = CLIENT.db(DB_NAME);
            const users = db.collection('users');

            const query = { $where: `this.username == '${username}'` };
            
            const user = await users.findOne(query);

            if (fs.existsSync(RCE_FLAG_FILE)) {
                message += `<p class="success">RCE RÉUSSIE : Le fichier drapeau <code>${RCE_FLAG_FILE}</code> a été créé !</p>`;
                fs.unlinkSync(RCE_FLAG_FILE); 
            }

            if (user) {
                message += `<p class="success">Connexion réussie pour l'utilisateur: <b>${user.username}</b></p>`;
            } else {
                message += '<p class="error">Nom d\'utilisateur non trouvé ou mot de passe incorrect.</p>';
            }

        } catch (e) {
            message = `<p class="error">Erreur de connexion MongoDB: ${e.message}</p>`;
        }
    }

    res.send(HTML_TEMPLATE + `<div class="result">${message}</div>`);
});

app.listen(port, () => {
    console.log(`Lab 42 running on http://localhost:${port}`);
});
