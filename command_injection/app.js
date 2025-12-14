const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 3002;

app.use(express.urlencoded({ extended: true }));

// CSS intégré pour le rendu esthétique
const PAGE_STYLE = `
<style>
    body { font-family: 'Arial', sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    h2, h3 { color: #34495e; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
    input[type="text"] { 
        width: 100%; padding: 10px; margin: 8px 0; display: inline-block; 
        border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; 
    }
    input[type="submit"] { 
        background-color: #3498db; color: white; padding: 10px 20px; 
        border: none; border-radius: 4px; cursor: pointer; font-size: 16px;
    }
    input[type="submit"]:hover { background-color: #2980b9; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .vulnerability-note { background-color: #f39c12; color: white; padding: 5px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .success { color: green; font-weight: bold; }
    .error { color: red; font-weight: bold; }
</style>
`;

// Route GET (Formulaire de base)
app.get('/', (req, res) => {
    res.send(`
        <html>
        <head>
            <title>OS Command Injection Lab</title>
            ${PAGE_STYLE}
        </head>
        <body>
            <div class="vulnerability-note">VULNÉRABILITÉ: OS Command Injection (Port 8082)</div>
            <h1>OS Command Injection Lab (Ping Utility)</h1>
            <p><strong>Cible:</strong> Injecter une commande shell via le champ IP.</p>
            <form method="POST" action="/lookup">
                <label for="ip">Entrez l'IP à pinger (e.g., 127.0.0.1):</label><br>
                <input type="text" id="ip" name="ip" value="127.0.0.1" style="width: 80%;"><br><br>
                <input type="submit" value="Ping">
            </form>
            <hr>
            <h3>Instructions</h3>
            <p>Utilisez des séparateurs de commandes (e.g., <code>;</code>, <code>&&</code>, <code>|</code>) pour échapper à la commande <code>ping</code> et exécuter votre propre commande (e.g., <code>ls</code> ou <code>cat /etc/passwd</code>).</p>
        </body>
        </html>
    `);
});

// Route POST (Logique vulnérable)
app.post('/lookup', (req, res) => {
    const ip = req.body.ip; 
    
    // ⚠️ VULNÉRABILITÉ ⚠️: L'entrée 'ip' est concaténée directement dans la commande shell.
    const command = 'ping -c 4 ' + ip; 

    exec(command, (error, stdout, stderr) => {
        let output = '';
        if (error) {
            output = `Error: ${stderr}`;
        } else {
            output = stdout;
        }

        // Utilisation de Template Literals pour la réponse POST
        res.send(`
            <html>
            <head>
                <title>OS Command Injection Lab - Résultat</title>
                ${PAGE_STYLE}
            </head>
            <body>
                <div class="vulnerability-note">RÉSULTAT DE L'EXÉCUTION</div>
                <h1>OS Command Injection Lab (Ping Utility)</h1>
                <form method="POST" action="/lookup">
                    <label for="ip">Entrez l'IP à pinger (e.g., 127.0.0.1):</label><br>
                    <input type="text" id="ip" name="ip" value="${ip}" style="width: 80%;"><br><br>
                    <input type="submit" value="Ping">
                </form>
                <hr>
                <h3>Commande exécutée: <code>${command}</code></h3>
                <pre id="output">${output}</pre>
                <a href="/">Retour au Lab</a>
            </body>
            </html>
        `);
    });
});

app.listen(port, () => {
    console.log('Command Injection Lab listening on port ' + port);
});
