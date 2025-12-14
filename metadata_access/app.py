from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
# Nom DNS de notre conteneur simulateur de metadata
METADATA_ENDPOINT_SIMULATOR = 'http://metadata_endpoint/' 

HTML_FORM = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"] { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    input[type="submit"] { background-color: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: Cloud Metadata Endpoint Access (SSRF Avancé) - Port 8092</div>
<h1>Lab 13 - Vérificateur d'URL (Vulnérable)</h1>

<p>Le développeur n'a pas filtré les URLs et fait confiance au réseau interne. Le point de terminaison de métadonnées est accessible via l'URL interne <code>{{ endpoint }}</code>.</p>
<p><strong>Cible :</strong> Utiliser le SSRF pour accéder à l'URL interne et récupérer les clés de sécurité.</p>

<form method="POST">
    <label for="url">URL à vérifier :</label>
    <input type="text" id="url" name="url" placeholder="Ex: https://google.com">
    <input type="submit" value="Vérifier l'URL">
</form>

<h2>Résultat de la Vérification</h2>
<pre>{{ result }}</pre>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = "En attente de la vérification de l'URL..."
    
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            try:
                # ⚠️ VULNÉRABILITÉ : Aucun filtrage ou liste blanche (SSRF).
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    # Pour la démo, nous affichons les 500 premiers caractères de la réponse
                    result = "Statut 200 OK.\n\nContenu (partiel) :\n" + response.text[:500]
                else:
                    result = f"Erreur: Statut {response.status_code}"
            except requests.exceptions.RequestException as e:
                result = f"Erreur de connexion (Probablement IP Interdite/Timeout) : {e}"
            except Exception as e:
                result = f"Erreur inattendue : {e}"
        else:
            result = "Veuillez fournir une URL."

    return render_template_string(HTML_FORM, result=result, endpoint=METADATA_ENDPOINT_SIMULATOR)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
