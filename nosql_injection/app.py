from flask import Flask, request, render_template_string
import json

app = Flask(__name__)

# Simuler la base de données MongoDB
USERS_COLLECTION = [
    {"username": "admin", "password": "secure_admin_password_987"},
    {"username": "bob", "password": "bob_password_123"},
]

HTML_FORM = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    input[type="submit"] { background-color: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .status { margin-top: 15px; font-weight: bold; }
    .success { color: #27ae60; }
    .error { color: #c0392b; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: NoSQL Injection (MongoDB Simulation) - Port 8106</div>
<h1>Lab 27 - Page de Connexion NoSQL</h1>

<p>L'application construit la requête d'authentification sans nettoyer l'entrée, permettant l'injection d'opérateurs MongoDB.</p>

<form method="POST">
    <label for="username">Nom d'utilisateur :</label>
    <input type="text" id="username" name="username" placeholder="Ex: admin">
    <label for="password">Mot de passe :</label>
    <input type="password" id="password" name="password" placeholder="Mot de passe">
    <input type="submit" value="Se connecter">
</form>

<h2>Statut</h2>
<pre>{{ result }}</pre>

<h3>Instructions pour l'Attaque</h3>
<p><strong>Cible :</strong> Se connecter en tant qu'administrateur sans connaître le mot de passe.</p>
<p>1. L'injection classique "OR '1'='1" ne fonctionne pas ici.</p>
<p>2. Injectez un opérateur MongoDB dans le champ mot de passe pour que la condition de requête soit toujours vraie ou ignorée.</p>
<p><strong>Charge Utile :</strong></p>
<ul>
    <li>Username: <code>admin</code></li>
    <li>Password: <code>{"$ne": null}</code> (injecté dans le JSON, cela signifie : "où le mot de passe n'est pas nul", ce qui est toujours vrai pour les champs existants).</li>
</ul>
<p>Attention : Vous devez intercepter la requête et modifier le mot de passe pour le transmettre en JSON brut ou utiliser un opérateur dans l'URL si l'application le permet (moins probable ici).</p>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = "En attente de la connexion..."
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # ⚠️ VULNÉRABILITÉ NOSQL INJECTION ⚠️
        # Construction de l'objet de requête non sécurisé (simulé)
        
        # Dans un vrai scénario, si l'application prend le mot de passe en JSON:
        # query = {'username': username, 'password': password}
        # Si password contient '{"$ne": null}', la base de données l'interprète.
        
        # Pour simuler cela en formulaire POST, nous allons vérifier si le mot de passe
        # est un JSON valide qui contient un opérateur, simulant l'injection.
        
        simulated_query = {"username": username, "password": password}
        
        # Tentative d'interpréter le mot de passe comme un opérateur MongoDB
        is_injected = False
        try:
            # Si le mot de passe est un JSON valide et contient un opérateur MongoDB ($...)
            parsed_password = json.loads(password)
            if any(key.startswith('$') for key in parsed_password.keys()):
                simulated_query["password"] = parsed_password
                is_injected = True
        except json.JSONDecodeError:
            # Le mot de passe est une chaîne normale
            pass

        # Recherche simulée dans la collection
        found_user = None
        for user in USERS_COLLECTION:
            match = True
            
            # 1. Vérification du nom d'utilisateur
            if user['username'] != simulated_query['username']:
                continue
                
            # 2. Vérification du mot de passe (point de l'injection)
            if is_injected:
                # Simuler l'opérateur $ne: null (toujours vrai si la clé 'password' existe)
                if '$ne' in simulated_query['password'] and simulated_query['password']['$ne'] is None:
                    found_user = user
                    break
            
            # Si pas d'injection, vérification normale de mot de passe
            elif user['password'] == simulated_query['password']:
                found_user = user
                break

        if found_user:
            if found_user['username'] == 'admin':
                result = f"<span class='status success'>CONNEXION RÉUSSIE : Vous êtes connecté en tant qu'ADMIN !</span>"
            else:
                result = f"<span class='status success'>CONNEXION RÉUSSIE : Vous êtes connecté en tant que {found_user['username']}.</span>"
        else:
            result = "<span class='status error'>ÉCHEC DE LA CONNEXION : Nom d'utilisateur ou mot de passe incorrect.</span>"
    
    return render_template_string(HTML_FORM, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
