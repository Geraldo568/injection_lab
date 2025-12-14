from flask import Flask, request, render_template_string, jsonify
import re
import time
import os

app = Flask(__name__)

# Simuler une session utilisateur
# L'attaquant doit inciter la victime (user_id=1) à visiter l'URL de cache malveillante.
SESSION_DATA = {
    'is_authenticated': True,
    'username': 'victim_alice',
    'secret_token': 'WCD-SECRET-TOKEN-12345',
    'last_login': time.ctime()
}

# Simuler un cache simple pour le lab
CACHE = {}
CACHE_TTL = 30 # 30 secondes

HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .info { color: #3498db; margin-top: 15px; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: Web Cache Deception (WCD) - Port 8113</div>
<h1>Lab 34 - Page de Profil Utilisateur (Vulnérable au Cache)</h1>

<p class="info">Vous êtes connecté en tant que <strong>{{ user_data['username'] }}</strong>. Cette page contient votre jeton secret.</p>
<p>Le serveur de cache (simulé) est mal configuré et met en cache tout ce qui se termine par une extension de fichier statique, même si le chemin d'accès n'existe pas et renvoie du contenu dynamique.</p>

<h2>Détails de Session Sensibles</h2>
<pre>
{{ session_details }}
</pre>

<h3>Instructions pour l'Attaque</h3>
<p><strong>Cible :</strong> Obtenir le <code>secret_token</code> d'une victime connectée.</p>
<p>1. L'attaquant envoie une requête pour un chemin inexistant mais statique, comme <code>/profile/sensible_data.css</code> ou <code>/profile/avatar.png</code>.</p>
<p>2. Le serveur d'application répond avec la page de profil dynamique <code>/profile</code>, car <code>/profile/avatar.png</code> n'existe pas.</p>
<p>3. La configuration du cache voit l'extension `.png` et met en cache la réponse (la page de profil sensible).</p>
<p>4. L'attaquant accède ensuite à la même URL, récupérant la page de profil de la victime à partir du cache.</p>

<p><strong>URL d'Attaque (Victime doit visiter) :</strong> <code>http://localhost:8113/profile/cache_leak.jpg</code></p>
<p><strong>URL d'Attaque (Attaquant doit visiter ensuite) :</strong> <code>http://localhost:8113/profile/cache_leak.jpg</code></p>
"""

def get_session_details():
    """Récupère les données sensibles de l'utilisateur."""
    # Simuler le fait que ces données ne sont générées que si l'utilisateur est authentifié
    return jsonify(SESSION_DATA).get_data(as_text=True)

@app.route('/profile/', defaults={'path': ''}, methods=['GET'])
@app.route('/profile/<path:path>', methods=['GET'])
def profile(path):
    
    current_time = time.time()
    
    # ⚠️ VULNÉRABILITÉ WCD (Simulée) ⚠️
    # La logique de cache vérifie l'extension finale
    
    # Si le chemin se termine par une extension statique (.jpg, .png, .css, etc.)
    if path and re.search(r'\.(jpg|png|css|js)$', path.lower()):
        cache_key = request.url # Utiliser l'URL complète comme clé de cache
        
        # 1. Vérification du cache
        if cache_key in CACHE and CACHE[cache_key]['expiry'] > current_time:
            # Succès de l'attaque WCD : l'attaquant récupère le contenu de la victime
            return f"*** CONTENU SERVI PAR LE CACHE (WCD réussi) ***\n\n{CACHE[cache_key]['content']}"

        # 2. Sinon, générer le contenu dynamique (page de profil)
        session_details = get_session_details()
        
        # 3. Mise en cache du contenu dynamique (WCD vulnérable)
        cache_entry = {
            'content': render_template_string(HTML_TEMPLATE, user_data=SESSION_DATA, session_details=session_details),
            'expiry': current_time + CACHE_TTL
        }
        CACHE[cache_key] = cache_entry
        
        return f"*** CACHE MIS À JOUR ({path} - Clé: {cache_key}) ***\n\n{cache_entry['content']}"

    # Route de profil normale
    session_details = get_session_details()
    return render_template_string(HTML_TEMPLATE, user_data=SESSION_DATA, session_details=session_details)


@app.route('/', methods=['GET'])
def home():
    return """
    <style>
        body { 
            font-family: 'Arial', sans-serif; 
            background-color: #1c2331; /* Bleu foncé / Charbon */
            color: #ecf0f1; /* Blanc cassé */
            margin: 0; 
            padding: 40px;
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #2c3e50; /* Bleu foncé */
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        }
        h1 { 
            color: #3498db; /* Bleu vif */
            border-bottom: 3px solid #e74c3c; /* Rouge pour le danger */
            padding-bottom: 15px;
            margin-top: 0;
            font-size: 2em;
        }
        h2 {
            color: #f1c40f; /* Jaune pour l'avertissement */
            margin-top: 25px;
        }
        .vulnerability-info {
            background-color: #c0392b; /* Rouge fort */
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            font-size: 1.1em;
            font-weight: bold;
        }
        a {
            color: #2ecc71; /* Vert pour le lien */
            text-decoration: none;
            font-weight: bold;
            transition: color 0.3s;
        }
        a:hover {
            color: #1abc9c;
        }
        .instruction-box {
            text-align: left;
            margin-top: 30px;
            border-top: 1px dashed #7f8c8d;
            padding-top: 20px;
        }
    </style>
    <div class="container">
        <div class="vulnerability-info">
            VULNÉRABILITÉ LAB 34 : Web Cache Deception (WCD) - Port 8113
        </div>
        <h1>Bienvenue à l'Atelier d'Exploitation</h1>
        
        <h2>Objectif du Lab</h2>
        <p>Ce laboratoire simule un serveur mal configuré où un attaquant peut forcer la mise en cache de données de session privées appartenant à d'autres utilisateurs (victimes).</p>
        
        <div class="instruction-box">
            <h3>Commencer l'Exploitation :</h3>
            <p>1. **Point d'Accès Sensible :** Naviguez vers la page de profil pour voir les données de session sensibles (simulées) :</p>
            <p style="font-size: 1.2em;">
                → <a href="/profile/">http://localhost:8113/profile/</a>
            </p>
            <p>2. **Scénario d'Attaque :** Pour exploiter le WCD, vous devrez utiliser une URL qui trompe le mécanisme de cache du serveur (par exemple, une URL se terminant par une extension statique comme `.jpg`).</p>
        </div>
    </div>
    """


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
