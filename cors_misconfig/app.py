from flask import Flask, jsonify, request
# Nous utilisons flask_cors pour simuler une configuration spécifique
from flask_cors import CORS

app = Flask(__name__)

# ⚠️ VULNÉRABILITÉ CORS ⚠️
# Configuration permissive : reflète l'en-tête 'Origin' dans 'Access-Control-Allow-Origin'
CORS(app, resources={r"/api/data": {"origins": "*"}}) 

# Simuler des données d'utilisateur sensibles
SECRET_DATA = {
    "user": "victim_bob",
    "email": "bob.victim@exemple.com",
    "api_key": "PRIVATE-CORS-12345"
}

HTML_INFO = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .info { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: Cross-Origin Resource Sharing (CORS) Misconfiguration - Port 8100</div>
<h1>Lab 21 - API Vulnérable (CORS)</h1>

<p>Cette API est configurée pour permettre l'accès à partir de n'importe quel domaine (<code>Access-Control-Allow-Origin: *</code>).</p>
<p><strong>Cible :</strong> Utiliser un script sur un domaine externe (simulé par un autre lab, non nécessaire ici) pour récupérer les données de l'API.</p>

<h2>Endpoint : <code>/api/data</code></h2>
<p>Ceci est une ressource protégée par CORS.</p>
<pre class="info">
{
  "user": "victim_bob",
  "api_key": "PRIVATE-CORS-12345"
}
</pre>

<h3>Instructions pour le Test</h3>
<p>1. Ouvrez l'endpoint directement dans votre navigateur : <code>http://localhost:8100/api/data</code>. Vous verrez les données JSON.</p>
<p>2. Pour confirmer l'exploit, vous auriez besoin d'une page HTML hébergée sur un autre port (ex: 8101) contenant un script JavaScript qui tente de faire un <code>fetch('/api/data')</code> vers <code>localhost:8100</code>.</p>
<p>Puisque le serveur renvoie <code>Access-Control-Allow-Origin: *</code> (ou reflète l'origine), le navigateur de la victime autoriserait le script malveillant à lire la réponse.</p>

"""

@app.route('/')
def index():
    return HTML_INFO

@app.route('/api/data')
def api_data():
    return jsonify(SECRET_DATA)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
