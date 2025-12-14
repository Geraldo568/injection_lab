from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

FLAG_FILE = "/tmp/ssti_rce_flag_8125.txt"
# Le drapeau est la preuve que le RCE a eu lieu
FLAG_CONTENT = "SSTI_RCE_PWNED" 
os.environ['FLAG_ENV'] = FLAG_CONTENT # Le drapeau est stocké dans une variable d'environnement

HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #e74c3c; border-bottom: 2px solid #c0392b; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"] { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; }
    input[type="submit"] { background-color: #c0392b; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; }
    .result { margin-top: 20px; padding: 10px; border: 1px dashed #7f8c8d; }
    .success { color: #2ecc71; font-weight: bold; }
    .error { color: #e74c3c; font-weight: bold; }
</style>
<div class="vulnerability-note">VULNÉRABILITÉ CRITIQUE : Server Side Template Injection (SSTI RCE - Jinja2) - Port 8125</div>
<h1>Lab 46 - Générateur de Message de Bienvenue</h1>
<p>
    L'entrée utilisateur est directement passée à la fonction <code>render_template_string</code>, permettant l'exécution de code Python via les expressions Jinja2.
</p>
<p>
    <b>Objectif :</b> Injecter un payload SSTI (ex: <code>{{ 7*7 }}</code>) pour obtenir l'exécution d'une commande système et lire le secret <code>FLAG_ENV</code>.
</p>
<form method="POST">
    <label for="name">Votre nom :</label>
    <input type="text" name="name" id="name" placeholder="Entrez votre nom ou un payload SSTI">
    <input type="submit" value="Générer">
</form>
{% if result %}
    <div class="result">
        <b>Résultat du Template :</b> {{ result|safe }}
    </div>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        name = request.form.get('name', 'Utilisateur')
        
        template_string = f"Bienvenue, {name}!"
        
        try:
            # VULNÉRABILITÉ : Utilisation de render_template_string avec l'entrée utilisateur
            result = render_template_string(template_string)
            
        except Exception as e:
            result = f"<p class='error'>Erreur d'exécution du template : {type(e).__name__} (Payload probablement bloqué ou malformé).</p>"
            
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
