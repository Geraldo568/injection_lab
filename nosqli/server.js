const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient } = require('mongodb');

const app = express();
const port = 3000;
const mongoUri = process.env.MONGODB_URI || 'mongodb://mongodb:27017/nosql_lab';

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

let db;

// CSS intégré pour le rendu esthétique
const PAGE_STYLE = `
<style>
    body { font-family: 'Arial', sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    h2, h3 { color: #34495e; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
    input[type="text"], input[type="password"] { 
        width: 100%; padding: 10px; margin: 8px 0; display: inline-block; 
        border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; 
    }
    input[type="submit"], button { 
        background-color: #3498db; color: white; padding: 10px 20px; 
        border: none; border-radius: 4px; cursor: pointer; font-size: 16px;
    }
    input[type="submit"]:hover, button:hover { background-color: #2980b9; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .vulnerability-note { background-color: #f39c12; color: white; padding: 5px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .success { color: green; font-weight: bold; }
    .error { color: red; font-weight: bold; }
</style>
`;

// 1. Connect to MongoDB and seed data
MongoClient.connect(mongoUri)
    .then(client => {
        db = client.db('nosql_lab');
        // Seed the user we need to bypass
        db.collection('users').updateOne(
            { username: 'admin' }, 
            { $set: { username: 'admin', password: 'HardToGuessPassword!', role: 'admin' } }, 
            { upsert: true }
        );
        db.collection('users').updateOne(
            { username: 'guest' }, 
            { $set: { username: 'guest', password: 'guestpassword', role: 'user' } }, 
            { upsert: true }
        );
        console.log("MongoDB connected and user 'admin' seeded.");
    })
    .catch(err => {
        console.error("Failed to connect to MongoDB:", err.message);
    });

// 2. Vulnerable Login Endpoint
app.post('/login', async (req, res) => {
    // CRITICAL VULNERABILITY: The entire query object is constructed directly from user input
    const query = req.body; 
    
    if (!query.username) {
        return res.status(400).send("Username required.");
    }

    try {
        const user = await db.collection('users').findOne(query); // VULNERABLE FIND OPERATION
        
        if (user) {
            let responseHtml = `
                <html><head><title>Login Success</title>${PAGE_STYLE}</head><body>
                <div class="vulnerability-note">RÉSULTAT DE L'ATTAQUE</div>
                <h1 class="success">SUCCESS! Logged in as: ${user.username}</h1>
                <p>Role: ${user.role}</p>
                <p>Le mot de passe pour '${user.username}' est: <strong>${user.password}</strong></p>
                <hr><a href="/">Retour au Lab</a>
                </body></html>`;
            return res.send(responseHtml);
        } else {
            let responseHtml = `
                <html><head><title>Login Failed</title>${PAGE_STYLE}</head><body>
                <div class="vulnerability-note">RÉSULTAT DE L'ATTAQUE</div>
                <h1 class="error">Login failed: Invalid credentials.</h1>
                <p>Astuce: Essayez une injection JSON pour le champ 'password'.</p>
                <hr><a href="/">Retour au Lab</a>
                </body></html>`;
            return res.status(401).send(responseHtml);
        }
    } catch (e) {
        console.error("Query error:", e);
        return res.status(500).send(`
            <html><head><title>Server Error</title>${PAGE_STYLE}</head><body>
            <h1 class="error">Server error during login. (Check logs)</h1>
            </body></html>`);
    }
});

// 3. Simple HTML Form
app.get('/', (req, res) => {
    res.send(`
        <html>
        <head>
            <title>NoSQL Injection Lab</title>
            ${PAGE_STYLE}
        </head>
        <body>
            <div class="vulnerability-note">VULNÉRABILITÉ: NoSQL Injection via Opérateur JSON</div>
            <h1>NoSQL Injection Lab (Port 8081)</h1>
            <p>Target: Log in as 'admin' without knowing the password.</p>
            <p>Hint: You need to send a **raw JSON POST** request to bypass the logic using a MongoDB query operator.</p>
            <hr>
            <form id="loginForm">
                Username: <input type="text" id="username" value="admin"><br>
                Password: <input type="password" id="password" value="password"><br>
                <button type="submit">Login (This form won't work - use cURL/Proxy!)</button>
            </form>
            <p>Use a tool like **cURL** or **Burp Suite** to craft the expert JSON payload to the <code>/login</code> endpoint.</p>
            <p>Example cURL Structure:</p>
            <pre>
curl -X POST http://localhost:8081/login \\
-H "Content-Type: application/json" \\
-d '{"username":"admin", "password": {"$ne": null}}'
            </pre>
            <script>
            document.getElementById('loginForm').onsubmit = (e) => {
                e.preventDefault();
                alert("The standard form submission sends URL-encoded data. You must use a tool for raw JSON injection!");
            }
            </script>
        </body>
        </html>
    `);
});

app.listen(port, () => {
    console.log('NoSQLi app listening on port ' + port);
});
