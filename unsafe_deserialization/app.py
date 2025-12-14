from flask import Flask, request, render_template_string, make_response
import pickle
import base64
import os

app = Flask(__name__)

# Classe simple utilisée pour stocker les données d'utilisateur
class UserData:
    def __init__(self, username, level="guest"):
        self.username = username
        self.level = level

# Simuler la sérialisation des données d'un utilisateur invité
GUEST_DATA = UserData("guest_user")
GUEST_SERIALIZED = base64.b64encode(pickle.dumps(GUEST_DATA)).decode()

HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .info { color: #3498db; margin-top: 15px; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: Unsafe Deserialization - Port 8105</div>
<h1>Lab 26 - Application de Session Sérialisée</h1>

<p class="info">Vos informations de session sont stockées dans le cookie <code>session_data</code> (Base64 encodé en utilisant Python Pickle).</p>
<p>Pickle, utilisé pour la sérialisation, peut être exploité pour l'exécution de code à distance (RCE) si les données ne sont pas fiables.</p>

<h2>Statut de la Session</h2>
<pre>
Utilisateur : {{ user.username }}
Niveau d'accès : {{ user.level }}
</pre>

<h3>Instructions pour l'Attaque</h3>
<p><strong>Cible :</strong> Générer une charge utile Python Pickle (qui exécute une commande shell) et la remplacer dans le cookie <code>session_data</code>.</p>
<p>1. Capturez le cookie <code>session_data</code>.</p>
<p>2. Générez une charge utile Pickle malveillante (ex: pour exécuter <code>ls -la</code>) en utilisant le module <code>subprocess</code> ou <code>os</code> en Python.</p>
<p>3. Encodez la charge utile en Base64 et remplacez la valeur du cookie.</p>
<p>4. La prochaine requête déclenchera la RCE lors de la désérialisation.</p>
"""

@app.route('/', methods=['GET'])
def index():
    user_data_b64 = request.cookies.get('session_data', GUEST_SERIALIZED)
    
    try:
        # ⚠️ VULNÉRABILITÉ DESERIALIZATION ⚠️
        # Désérialisation de données non fiables du cookie
        serialized_data = base64.b64decode(user_data_b64)
        user = pickle.loads(serialized_data)
        
    except Exception as e:
        # Si la désérialisation échoue (y compris RCE), afficher l'erreur ou réinitialiser.
        user = UserData("hacker", "RCE_FAILED")
        
    response = make_response(render_template_string(HTML_TEMPLATE, user=user))
    
    # Assurez-vous que le cookie est toujours là si c'était l'utilisateur invité
    if user_data_b64 == GUEST_SERIALIZED:
        response.set_cookie('session_data', GUEST_SERIALIZED)

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
