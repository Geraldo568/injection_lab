from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2ecc71; border-bottom: 2px solid #27ae60; padding-bottom: 10px; }
    .vulnerability-note { background-color: #2ecc71; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"] { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; }
    input[type="submit"] { background-color: #27ae60; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; }
    .result { margin-top: 20px; padding: 10px; border: 1px dashed #7f8c8d; }
    .success { color: #2ecc71; font-weight: bold; }
    .error { color: #e74c3c; font-weight: bold; }
</style>
<div class="vulnerability-note">VULNÉRABILITÉ CRITIQUE : SSRF Blind OOB - Port 8123</div>
<h1>Lab 44 - Service de notification de statut</h1>
<p>
    Ce service vérifie le statut d'une ressource via une URL. Il n'affiche AUCUN résultat (Blind) mais permet l'utilisation de schémas d'URI non conventionnels.
</p>
<p>
    <b>Objectif :</b> Utiliser un payload OOB (Out-of-Band, ex: un protocole non HTTP comme <code>http://attacker.com/</code>) pour prouver que le serveur a interagi avec un hôte externe.
    (L'exploitation nécessite un serveur d'écoute externe, par exemple, Burp Collaborator ou un serveur DNS/HTTP personnel).
</p>
<form method="POST">
    <label for="url">URL de ressource à vérifier :</label>
    <input type="text" name="url" id="url" placeholder="Entrez l'URL OOB ici...">
    <input type="submit" value="Notif. Statut">
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
        url = request.form.get('url')
        
        # Filtre basique pour forcer l'OOB
        if any(p in url.lower() for p in ["127.0.0.1", "localhost"]):
            message = "<p class='error'>Erreur de sécurité : les adresses locales sont bloquées.</p>"
            return render_template_string(HTML_TEMPLATE, message=message)

        try:
            # Blind : Pas de données retournées. Le but est juste que la requête sorte.
            requests.get(url, timeout=3)
            message = "<p class='success'>Vérification de statut envoyée. Si la requête est sortie du réseau, vous devriez voir un ping sur votre serveur OOB.</p>"
        except Exception as e:
            message = f"<p class='error'>Erreur de connexion (c'est normal si le serveur OOB n'est pas actif) : {type(e).__name__}.</p>"
            
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
