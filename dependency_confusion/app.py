from flask import Flask, render_template_string
import os
import shutil

app = Flask(__name__)

if os.path.exists('EXPLOIT_PROOF.txt'):
    shutil.copyfile('EXPLOIT_PROOF.txt', '/tmp/EXPLOIT_PROOF_RUN.txt')


HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .success { color: #27ae60; font-weight: bold; }
    .error { color: #c0392b; font-weight: bold; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: Confusion des Dépendances (Dependency Confusion) - Port 8114</div>
<h1>Lab 35 - Application utilisant des dépendances internes</h1>

<p>Cette application utilise une dépendance (internal-logger) dont l'installation est vulnérable à la confusion des dépendances.</p>

<h2>Statut de l'Exploitation (Vérification dans le conteneur)</h2>
{% if exploit_status %}
    <p class="success">{{ exploit_status }}</p>
    <p>Le code malveillant a réussi à s'exécuter DANS le conteneur pendant l'étape de <code>pip install</code>.</p>
{% else %}
    <p class="error">Le fichier de preuve d'exploitation n'a pas été trouvé (EXPLOIT_PROOF.txt).</p>
    <p>L'application n'a pas été exploitée lors de la dernière construction.</p>
{% endif %}

<h3>Instructions pour l'Attaque (Exploitation par Attaquant Externe)</h3>
<p>
    L'attaque est lancée par l'exécution de la commande <code>pip install</code> sans configuration de dépôt privé.
</p>
<p>
    1. **Hypothèse Attaquant :** L'attaquant publie un paquet nommé <code>internal-logger</code> sur PyPI avec une version supérieure.
</p>
<p>
    2. **Exploitation :** Lors de la construction Docker, <code>pip</code> choisit la version publique malveillante et exécute le code malveillant dans <code>setup.py</code>.
</p>
"""

@app.route('/', methods=['GET'])
def index():
    exploit_status = None
    if os.path.exists('EXPLOIT_PROOF.txt'):
         with open('EXPLOIT_PROOF.txt', 'r') as f:
             exploit_status = f.read().strip()
             
    # Supprimer le fichier après la lecture pour réinitialiser le test
    if os.path.exists('EXPLOIT_PROOF.txt'):
        os.remove('EXPLOIT_PROOF.txt')
        
    return render_template_string(HTML_TEMPLATE, exploit_status=exploit_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
