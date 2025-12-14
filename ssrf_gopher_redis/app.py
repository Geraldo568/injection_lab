from flask import Flask, request, render_template_string
import requests
import urllib.parse

app = Flask(__name__)

INTERNAL_REDIS_URL = "redis://redis_service:6379"

HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #f39c12; border-bottom: 2px solid #e67e22; padding-bottom: 10px; }
    .vulnerability-note { background-color: #f39c12; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"] { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; }
    input[type="submit"] { background-color: #e67e22; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; }
    .result { margin-top: 20px; padding: 10px; border: 1px dashed #7f8c8d; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ CRITIQUE : SSRF avec Gopher (Redis Attack) - Port 8119</div>
<h1>Lab 40 - Service de vérification d'URL</h1>

<p>
    Ce service vérifie l'accessibilité d'une URL fournie. Le protocole <code>gopher://</code> n'est pas explicitement bloqué, permettant d'attaquer le service Redis interne.
</p>
<p>
    <b>Objectif :</b> Forger un payload <code>gopher://</code> pour envoyer la commande Redis <code>SET SSRF_FLAG_8119 pwned</code> à l'hôte <code>redis_service:6379</code>.
</p>
<form method="POST">
    <label for="url">URL à vérifier (ex: http://localhost/):</label>
    <input type="text" name="url" id="url" placeholder="Entrez l'URL ici...">
    <input type="submit" value="Vérifier l'URL">
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
        if not url:
            message = "<p style='color:#e74c3c;'>Veuillez fournir une URL.</p>"
        else:
            if any(p in url.lower() for p in ["127.0.0.1", "localhost", "172."]):
                message = "<p style='color:#e74c3c;'>Erreur de sécurité : les adresses locales ne sont pas autorisées.</p>"
            
            else:
                try:
                    if url.lower().startswith('gopher'):
                        
                        if "gopher://redis_service:6379" in url and "SET%20SSRF_FLAG_8119" in url:
                            message = f"<p style='color:#2ecc71;'>Requête envoyée via gopher. Vérifiez le serveur Redis (<code>GET SSRF_FLAG_8119</code>).</p>"
                        else:
                            message = f"<p style='color:#2ecc71;'>Requête gopher soumise. (Résultat non affiché - Blind)</p>"

                    elif url.lower().startswith('http') or url.lower().startswith('https'):
                        response = requests.get(url, timeout=5)
                        message = f"<p style='color:#2ecc71;'>Statut HTTP : {response.status_code}. Contenu tronqué: {response.text[:100]}</p>"
                    else:
                        message = f"<p style='color:#e74c3c;'>Protocole non pris en charge.</p>"


                except requests.exceptions.Timeout:
                    message = "<p style='color:#e74c3c;'>Erreur : Timeout lors de la vérification de l'URL.</p>"
                except Exception as e:
                    message = f"<p style='color:#e74c3c;'>Erreur inattendue: {type(e).__name__}</p>"
                
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
