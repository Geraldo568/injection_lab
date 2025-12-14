from flask import Flask, request, render_template_string
import requests
import re
import socket

app = Flask(__name__)

# Nom DNS de l'endpoint de métadonnées interne (accessible uniquement au réseau Docker)
METADATA_URL = 'http://metadata_endpoint/'

# ⚠️ VULNÉRABILITÉ SSRF AVANCÉ ⚠️ : Liste noire naïve
BLACKLIST = ['127.0.0.1', 'localhost', '169.254.169.254', '0.0.0.0']
# Le conteneur "metadata_endpoint" résout à une IP interne (ex: 172.x.x.x)

HTML_FORM = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"] { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    input[type="submit"] { background-color: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .info { color: #3498db; margin-top: 15px; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: SSRF Avancé (Contournement de Filtre) - Port 8102</div>
<h1>Lab 23 - Vérificateur d'URL avec Liste Noire</h1>

<p>Le serveur tente de bloquer les IPs internes critiques <code>(127.0.0.1, 169.254.169.254, etc.)</code> mais le filtre est contournable.</p>
<p class="info">L'objectif est d'atteindre l'endpoint interne : <code>{{ metadata_url }}</code>.</p>

<form method="POST">
    <label for="url">URL à vérifier :</label>
    <input type="text" id="url" name="url" placeholder="Ex: http://192.168.1.1/resource">
    <input type="submit" value="Vérifier l'URL">
</form>

<h2>Résultat de la Vérification</h2>
<pre>{{ result }}</pre>
"""

def is_blacklisted(url):
    """Vérification naïve de la liste noire avant la requête."""
    
    # 1. Vérification par chaîne directe (naïve)
    for term in BLACKLIST:
        if term in url.lower():
            return True, f"Erreur: Le terme '{term}' est dans la liste noire."
            
    # 2. Tentative de résolution DNS pour vérification d'IP (naïve, car peut être contournée par l'encodage)
    try:
        host = re.search(r'//(.*?)(?:\/|$)', url)
        if host:
            host_name = host.group(1).split(':')[0]
            # Résolution pour obtenir l'IP avant la requête réelle
            ip_address = socket.gethostbyname(host_name)
            
            if ip_address in BLACKLIST:
                return True, f"Erreur: L'IP résolue '{ip_address}' est dans la liste noire."
                
    except Exception as e:
        # Ignore les erreurs de résolution pour les URLs non standard
        pass
        
    return False, None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = "En attente de la vérification de l'URL..."
    
    if request.method == 'POST':
        url = request.form.get('url', '')
        if url:
            is_blocked, reason = is_blacklisted(url)
            
            if is_blocked:
                result = reason
            else:
                try:
                    # La vraie requête est faite ici (elle gère les IP non-standard)
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        result = "Statut 200 OK. Contenu (partiel) :\n" + response.text[:500]
                    else:
                        result = f"Erreur: Statut {response.status_code}"
                except requests.exceptions.RequestException as e:
                    result = f"Erreur de connexion : {e}"
                except Exception as e:
                    result = f"Erreur inattendue : {e}"
        else:
            result = "Veuillez fournir une URL."

    return render_template_string(HTML_FORM, result=result, metadata_url=METADATA_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
