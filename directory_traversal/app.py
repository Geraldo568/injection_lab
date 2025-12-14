from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
FLAG_FILE = "/etc/secret_flag_8132.txt"
with open(FLAG_FILE, "w") as f:
    f.write("DIRECTORY_TRAVERSAL_SUCCESS")

HTML_TEMPLATE="""
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    .vulnerability-note { background-color: #95a5a6; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    /* ... (Style complet à insérer) ... */
</style>
<div class="vulnerability-note">LAB 53 : Directory Traversal (LFI) - Port 8132</div>
<h1>Service de Lecture de Log</h1>
<p>
    Ce service lit et affiche le contenu des fichiers de log. Il est vulnérable au Directory Traversal.
</p>
<p>
    <b>Objectif :</b> Lire le fichier secret <code>{FLAG_FILE}</code> en utilisant l'injection <code>../</code>.
</p>
<form method="POST">
    <label for="filename">Nom du fichier log :</label>
    <input type="text" name="filename" id="filename" placeholder="Ex: access.log">
    <input type="submit" value="Afficher">
</form>
{% if content %}
    <div class="result">
        <b>Contenu du fichier :</b><pre>{{ content }}</pre>
    </div>
{% endif %}
"""
@app.route('/', methods=['GET', 'POST'])
def index():
    content = None
    if request.method == 'POST':
        filename = request.form.get('filename', 'access.log')
        
        # VULNÉRABILITÉ : Aucune désinfection ou normalisation du chemin
        filepath = os.path.join('/app/logs', filename) 
        
        # Créer un répertoire de logs si nécessaire
        os.makedirs('/app/logs', exist_ok=True) 

        try:
            with open(filepath, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            content = f"Erreur: Fichier '{filename}' non trouvé."
        except Exception as e:
            content = f"Erreur de lecture : {e}"

    return render_template_string(HTML_TEMPLATE, content=content)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
