from flask import Flask, request, render_template_string
import jwt
import base64
import time

app = Flask(__name__)

# Clé secrète du serveur (l'attaquant ne la connaît pas)
SECRET_KEY = base64.b64encode(b"strong_server_secret_key_999").decode()

# Charge utile d'un utilisateur normal
USER_PAYLOAD = {'user': 'guest', 'role': 'user', 'iat': int(time.time())}
# Charge utile de l'administrateur
ADMIN_PAYLOAD = {'user': 'admin', 'role': 'admin', 'iat': int(time.time())}

# Générer un jeton initial (pour référence)
INITIAL_TOKEN = jwt.encode(USER_PAYLOAD, SECRET_KEY, algorithm='HS256')


HTML_FORM = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    textarea { width: 100%; height: 100px; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    input[type="submit"] { background-color: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .info { color: #3498db; margin-top: 15px; }
    .success { color: #27ae60; }
    .error { color: #c0392b; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: Signature Forgery via JWT (Algorithme "none") - Port 8110</div>
<h1>Lab 31 - Vérificateur de Jeton JWT</h1>

<p class="info">Le jeton de session est le JWT. Le serveur le décode et le vérifie pour déterminer votre rôle.</p>
<p>Jeton Initial de l'utilisateur 'guest' : <code>{{ initial_token }}</code></p>

<form method="POST">
    <label for="jwt_token">Jeton JWT à vérifier (Placez ici votre jeton falsifié) :</label>
    <textarea name="jwt_token" id="jwt_token">{{ initial_token }}</textarea>
    <input type="submit" value="Vérifier le Jeton">
</form>

<h2>Résultat de la Vérification</h2>
<pre>{{ result }}</pre>

<h3>Instructions pour l'Attaque "Algorithme none"</h3>
<p><strong>Cible :</strong> Se faire passer pour l'administrateur sans connaître la <code>SECRET_KEY</code>.</p>
<p>1. Décodez le jeton initial (Header et Payload).</p>
<p>2. Modifiez le Payload pour y inclure <code>"role": "admin"</code>.</p>
<p>3. Modifiez l'en-tête (Header) pour que l'algorithme soit <code>"alg": "none"</code>.</p>
<p>4. Falsifiez le jeton : Base64(Header_modifié) . "." . Base64(Payload_modifié) . "."</p>
<p>5. Envoyez ce jeton falsifié (avec la signature vide) au serveur.</p>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = "Jeton vérifié. Veuillez soumettre votre jeton."
    jwt_token = INITIAL_TOKEN
    
    if request.method == 'POST':
        jwt_token = request.form.get('jwt_token', INITIAL_TOKEN)
        
        # ⚠️ VULNÉRABILITÉ JWT ⚠️
        # Le code permet l'algorithme 'none' s'il n'est pas explicitement exclu.
        # Nous allons simuler une implémentation vulnérable qui accepte "none".
        
        try:
            # Note: Par défaut, pyjwt exige l'algorithme, mais une librairie 
            # mal configurée pourrait accepter une liste d'algos incluant 'none'.
            # Ici, nous simulerons le scénario où 'none' est autorisé.
            
            # Tenter de décoder SANS spécifier l'algorithme, laissant la librairie
            # faire la "magie" (la vulnérabilité réelle est dans la configuration)
            
            # Simuler l'acceptation de 'none' si la signature est manquante:
            if jwt_token.endswith('.'):
                 # Si la signature est vide, on tente la désérialisation
                 payload = jwt.decode(jwt_token, algorithms=['none'], options={"verify_signature": False})
            else:
                 # Sinon, on tente une vérification normale (qui échouera sans la clé)
                 # On suppose ici que le secret n'est pas dans le code pour la vulnérabilité
                 # mais pour la démo, on doit pouvoir décoder le jeton de base.
                 payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])

            
            # Vérification du rôle
            role = payload.get('role', 'unknown')
            user = payload.get('user', 'unknown')
            
            if role == 'admin':
                result = f"<span class='status success'>AUTHENTIFICATION RÉUSSIE (ADMIN) :</span> Jeton valide, Bienvenue {user}!"
            else:
                result = f"<span class='status info'>AUTHENTIFICATION RÉUSSIE (USER) :</span> Jeton valide, Bienvenue {user}."

            result += "\n\nPayload décodé:\n" + json.dumps(payload, indent=2)

        except jwt.exceptions.InvalidAlgorithmError:
            result = "<span class='status error'>ERREUR :</span> L'algorithme 'none' n'est pas supporté par défaut dans cette librairie pour la sécurité. L'attaque est bloquée."
            result += "\n\n(Notez que dans un vrai lab, l'implémentation du serveur doit être spécifiquement vulnérable à cette faille)."
        except jwt.exceptions.InvalidSignatureError:
            result = "<span class='status error'>ERREUR :</span> Signature Invalide. Le jeton n'est pas signé correctement avec la clé secrète."
        except Exception as e:
            result = f"<span class='status error'>ERREUR :</span> Jeton invalide ou autre erreur: {e}"

    return render_template_string(HTML_FORM, result=result, initial_token=INITIAL_TOKEN)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
