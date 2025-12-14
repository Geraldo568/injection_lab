from flask import Flask, request, render_template_string, make_response
import hashlib
import time

app = Flask(__name__)

# Simule une session utilisateur authentifiée
SECRET_SESSION_DATA = "WCD_FLAG_8128:Votre_Jeton_Secret_d_Admin"

def is_authenticated():
    # Simule l'authentification basée sur un cookie simple
    return request.cookies.get('auth') == 'admin_token'

def get_user_content():
    # Contenu sensible qui ne devrait pas être mis en cache
    if is_authenticated():
        # Contenu sensible, incluant le drapeau
        return f"""
        <h2>Espace Personnel Sécurisé</h2>
        <p>Bienvenue, Admin!</p>
        <p class="secret">Le secret de votre session est : <code>{SECRET_SESSION_DATA}</code></p>
        <p>Ce contenu est censé être pour usage unique et ne jamais être mis en cache.</p>
        """
    return "<h2>Connexion Requise</h2><p>Veuillez vous connecter pour voir votre contenu.</p>"

HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #f1c40f; border-bottom: 2px solid #f39c12; padding-bottom: 10px; }
    .vulnerability-note { background-color: #f1c40f; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .content-box { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    .secret { color: #c0392b; font-weight: bold; border: 1px dashed #c0392b; padding: 5px; }
</style>
<div class="vulnerability-note">VULNÉRABILITÉ CRITIQUE : Web Cache Deception (WCD) - Port 8128</div>
<h1>Lab 49 - Profil Utilisateur (Service de Cache Vulnérable)</h1>

<p>
    Ce service met en cache le contenu des pages pour améliorer les performances. Il est vulnérable au WCD car il ne gère pas correctement les terminaisons d'URL inconnues.
</p>
<p>
    <b>Objectif :</b> Tromper le serveur de cache pour qu'il stocke le contenu sensible de la victime (obtenu via le cookie <code>auth=admin_token</code>) sous une URL publique, en utilisant une URL de la forme <code>/profile/some-resource.jpg</code>.
</p>

<div class="content-box">
    {{ user_content|safe }}
</div>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def profile(path):
    user_content = get_user_content()
    
    response = make_response(render_template_string(HTML_TEMPLATE, user_content=user_content))
    
    # Simuler la mauvaise configuration du Cache (le défaut de ne pas vérifier les extensions)
    if 'profile' in request.path and '.' in path:
        response.headers['Cache-Control'] = 'public, max-age=3600'
    else:
        response.headers['Cache-Control'] = 'no-store'

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
