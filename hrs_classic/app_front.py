from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)
# Le nom du service doit correspondre au docker-compose.yml corrigé (hrs_classic_backend)
BACKEND_URL = "http://hrs_classic_backend:80" 

HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #3498db; border-bottom: 2px solid #2980b9; padding-bottom: 10px; }
    .vulnerability-note { background-color: #3498db; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"] { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; }
    input[type="submit"] { background-color: #2980b9; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; }
    .result { margin-top: 20px; padding: 10px; border: 1px dashed #7f8c8d; }
    .success { color: #2ecc71; font-weight: bold; }
    .error { color: #e74c3c; font-weight: bold; }
</style>
<div class="vulnerability-note">VULNÉRABILITÉ CRITIQUE : HTTP Request Smuggling (HRS - CL.TE) - Port 8124</div>
<h1>Lab 45 - Proxy Frontend</h1>
<p>
    Ce service (Frontend) est vulnérable au Smuggling car il utilise l'en-tête <code>Content-Length</code> alors que le Backend utilise <code>Transfer-Encoding: chunked</code>.
</p>
<p>
    <b>Objectif :</b> Forger une requête HTTP unique pour que le Backend stocke le début d'une requête illégale (le Smuggled request) qui sera ensuite appliquée à la requête d'une victime suivante.
</p>
<form method="POST">
    <label for="data">Données à envoyer (simule le corps de la requête) :</label>
    <input type="text" name="data" id="data" placeholder="Test de HRS">
    <input type="submit" value="Transférer">
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
        data = request.form.get('data', '')
        
        # Simuler le rôle du Frontend (utilisant Content-Length)
        headers = {
            'Host': 'hrs_frontend',
            # Ceci simule une attaque CL.TE, même si le code Python est simple. 
            # L'attaquant forge la requête brute dans Burp ou cURL.
            'Transfer-Encoding': 'chunked' 
        }
        
        # Le frontend passe la requête au backend
        try:
            # Le frontend devrait calculer Content-Length, mais nous laissons l'outil attaquer 
            # avec la requête brute qui contiendra Content-Length ET Transfer-Encoding.
            response = requests.post(BACKEND_URL + '/process', data=data, headers=headers, timeout=5)
            message = f"<p class='success'>Frontend transféré. Réponse du Backend: Status {response.status_code}.</p>"
        except Exception as e:
            message = f"<p class='error'>Erreur de transfert au Backend: {type(e).__name__}</p>"
            
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
