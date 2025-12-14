from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Simuler la base de données utilisateur (ID 1 est le compte de l'attaquant, ID 2 est le compte admin)
USERS = {
    1: {'username': 'attacker_alice', 'email': 'alice@example.com', 'role': 'user', 'credit': 100},
    2: {'username': 'admin_bob', 'email': 'bob@admin.com', 'role': 'admin', 'credit': 99999}
}

# Utilisateur actuellement authentifié (Alice)
CURRENT_USER_ID = 1

HTML_FORM = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .info { color: #3498db; margin-top: 15px; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: Mass Assignment - Port 8104</div>
<h1>Lab 25 - API de Mise à Jour de Profil (Vulnérable)</h1>

<p class="info">Vous êtes connecté en tant que <strong>{{ user_data['username'] }}</strong> (ID: {{ CURRENT_USER_ID }}). Rôle actuel: <strong>{{ user_data['role'] }}</strong>.</p>
<p>L'API de mise à jour de profil est vulnérable à la sur-liaison (Mass Assignment) et permet de modifier des champs sensibles.</p>

<h2>Requête de Mise à Jour Typique (POST /api/user/{{ CURRENT_USER_ID }})</h2>
<pre>
{
    "email": "new.alice@example.com",
    "credit": 500
}
</pre>

<h3>Instructions pour l'Attaque</h3>
<p><strong>Cible :</strong> Changer votre rôle de 'user' à 'admin'.</p>
<p>1. Utilisez un outil (comme cURL ou Burp Repeater) pour envoyer une requête POST à <code>http://localhost:8104/api/user/{{ CURRENT_USER_ID }}</code>.</p>
<p>2. Injectez le champ sensible <code>"role"</code> dans le corps JSON :</p>
<pre>
POST /api/user/1 HTTP/1.1
Host: localhost:8104
Content-Type: application/json
Content-Length: [Calculé]

{
    "email": "alice.hacked@example.com",
    "role": "admin" 
}
</pre>
<p>3. Vérifiez votre nouveau rôle en visitant la page.</p>

<h2>Statut Actuel de l'Utilisateur</h2>
<pre>{{ current_status }}</pre>
"""

@app.route('/', methods=['GET'])
def index():
    user_data = USERS.get(CURRENT_USER_ID, {})
    current_status = jsonify(user_data).get_data(as_text=True)
    return render_template_string(HTML_FORM, user_data=user_data, CURRENT_USER_ID=CURRENT_USER_ID, current_status=current_status)

@app.route('/api/user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    if user_id != CURRENT_USER_ID:
        return jsonify({"error": "Unauthorized access to another user's profile."}), 403

    if user_id not in USERS:
        return jsonify({"error": "User not found"}), 404

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        # ⚠️ VULNÉRABILITÉ MASS ASSIGNMENT ⚠️
        # Mise à jour directe de l'objet utilisateur avec les données du JSON
        USERS[user_id].update(data)
        
        return jsonify({"message": "Profile updated successfully (possibly mass assigned).", "new_data": USERS[user_id]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
