const express = require('express');
const fetch = require('node-fetch');
const app = express();
const port = 3003;

app.use(express.urlencoded({ extended: true }));

// CSS intégré pour le rendu esthétique
const PAGE_STYLE = `
<style>
    body { font-family: 'Arial', sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    h2, h3 { color: #34495e; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"] { 
        width: 100%; padding: 10px; margin: 8px 0; display: inline-block; 
        border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; 
    }
    input[type="submit"] { 
        background-color: #9b59b6; /* Violet pour SSRF */
        color: white; padding: 10px 20px; 
        border: none; border-radius: 4px; cursor: pointer; font-size: 16px;
    }
    input[type="submit"]:hover { background-color: #8e44ad; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .result { margin-top: 20px; }
</style>
`;

// Route GET (Formulaire de base)
app.get('/', (req, res) => {
    res.send(`
        <html>
        <head>
            <title>SSRF Lab</title>
            ${PAGE_STYLE}
        </head>
        <body>
            <div class="vulnerability-note">VULNÉRABILITÉ: Server-Side Request Forgery (SSRF) - Port 8086</div>
            <h1>SSRF Lab - Outil de Vérification d'URL</h1>
            <p><strong>Cible:</strong> Forcer le serveur à accéder à des ressources internes (ex: <code>http://localhost:8080/</code>, <code>http://127.0.0.1/</code>, ou même <code>file:///etc/passwd</code>).</p>
            <form method="POST" action="/fetch">
                <label for="url">URL à vérifier (ex: https://example.com):</label><br>
                <input type="text" id="url" name="url" value="http://example.com" required><br><br>
                <input type="submit" value="Vérifier l'URL">
            </form>
            <hr>
            <h3>Instructions</h3>
            <p>Essayez d'utiliser des adresses internes pour prouver que le serveur exécute la requête sans restriction.</p>
        </body>
        </html>
    `);
});

// Route POST (Logique SSRF)
app.post('/fetch', async (req, res) => {
    const urlToFetch = req.body.url;
    let resultOutput = '';
    let status = 'Succès';

    // ⚠️ VULNÉRABILITÉ SSRF ⚠️: La fonction fetch exécute la requête sur le serveur sans valider l'URL cible.
    try {
        const response = await fetch(urlToFetch, { timeout: 5000 });
        const text = await response.text();
        
        resultOutput = `Statut HTTP: ${response.status}\nContenu (premiers 500 caractères):\n\n${text.substring(0, 500)}...`;
        
        if (response.status >= 400) {
            status = 'Erreur HTTP';
        }

    } catch (error) {
        resultOutput = `Erreur lors de la requête: ${error.message}`;
        status = 'Échec';
    }

    res.send(`
        <html>
        <head>
            <title>SSRF Lab - Résultat</title>
            ${PAGE_STYLE}
        </head>
        <body>
            <div class="vulnerability-note">RÉSULTAT SSRF</div>
            <h1>SSRF Lab - Outil de Vérification d'URL</h1>
            <form method="POST" action="/fetch">
                <label for="url">URL à vérifier:</label><br>
                <input type="text" id="url" name="url" value="${urlToFetch}" required><br><br>
                <input type="submit" value="Vérifier l'URL">
            </form>
            <hr>
            <h3>Résultat pour <code>${urlToFetch}</code> (Statut: ${status})</h3>
            <pre class="result">${resultOutput}</pre>
            <a href="/">Retour au Lab</a>
        </body>
        </html>
    `);
});

app.listen(port, () => {
    console.log('SSRF Lab listening on port ' + port);
});
