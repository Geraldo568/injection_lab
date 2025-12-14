from flask import Flask, request, render_template_string
import jwt
import os

app = Flask(__name__)
# Clé publique RS256 utilisée par le serveur pour VÉRIFIER les jetons (simulée)
# En réalité, c'est la clé PRIVÉE qui doit être utilisée par l'attaquant pour HS256
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEt112Uf+zK20g8Tz+l/92zN4H5q+Q
07m1vX1X0Q7z4zI8B5y0l+s9mF4g5y0l+s9mF4g5y0l+s9mF4g5y0l+s9mF4g5y0l
-----END PUBLIC KEY-----"""
# La clé HS256 sera la clé publique elle-même, exploitant la confusion

FLAG_ADMIN = "JWT_CONFUSION_SUCCESS"

HTML_TEMPLATE="""
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    .vulnerability-note { background-color: #3f51b5; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    /* ... (Style complet à insérer) ... */
</style>
<div class="vulnerability-note">LAB 55 : JWT Algorithm Confusion (RS256 vers HS256) - Port 8134</div>
<h1>Vérificateur de Jeton d'Authentification</h1>
<p>
    Ce service utilise RS256 pour signer les jetons, mais est vulnérable à l'attaque d'Algorithme Confusion.
    Il peut être forcé d'utiliser la clé publique comme clé secrète pour l'algorithme symétrique HS256.
</p>
<p>
    <b>Objectif :</b> Créer un jeton signé avec HS256 en utilisant la clé publique RS256 comme clé secrète. Modifiez le payload pour obtenir le rôle 'admin'.
</p>
<form method="POST">
    <label for="jwt_token">Votre Jeton JWT :</label>
    <input type="text" name="jwt_token" id="jwt_token" placeholder="Entrez votre jeton JWT forgé ici...">
    <input type="submit" value="Vérifier">
</form>
{% if message %}
    <div class="result">
        {{ message|safe }}
    </div>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        token = request.form.get('jwt_token')
        
        try:
            # VULNÉRABILITÉ : Le serveur fait confiance à l'algorithme spécifié dans l'en-tête du jeton (par défaut)
            # Il tente de vérifier le jeton en utilisant la CLÉ PUBLIQUE (PUBLIC_KEY) avec l'algorithme spécifié.
            # Si l'attaquant spécifie 'HS256' dans le jeton, le serveur utilisera la clé publique comme clé SECRÈTE HS256.
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256", "HS256"])
            
            if payload.get('role') == 'admin':
                message = f"<p class='success'>Authentification Admin Réussie ! Drapeaux : {FLAG_ADMIN}</p>"
            else:
                message = "<p>Authentification réussie, mais rôle non-admin.</p>"
                
        except jwt.exceptions.InvalidAlgorithmError:
            message = "<p class='error'>Algorithme invalide dans le jeton.</p>"
        except jwt.exceptions.InvalidSignatureError:
            message = "<p class='error'>Signature JWT invalide.</p>"
        except Exception as e:
             message = f"<p class='error'>Erreur de décodage du JWT: {e}</p>"
            
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
