from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Simuler l'endpoint où un attaquant essaierait de lire un fichier
@app.route('/', methods=['GET', 'POST'])
def index():
    file_path = request.args.get('path', 'info.txt')
    content = ""
    
    HTML_FORM = f"""
    <style>
        body {{ font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .vulnerability-note {{ background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }}
        pre {{ background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }}
        .info {{ color: #3498db; margin-top: 15px; }}
    </style>

    <div class="vulnerability-note">VULNÉRABILITÉ: Exposition de Variables d'Environnement Docker - Port 8107</div>
    <h1>Lab 28 - Lecteur de Fichier (Simulé LFI)</h1>

    <p>Cette application simule une faille d'inclusion de fichier (LFI) qui permet à l'attaquant de lire des fichiers système, y compris <code>/proc/self/environ</code>.</p>
    <p class="info">La clé secrète est passée via les variables d'environnement Docker et est vulnérable à la lecture.</p>
    
    <p>URL actuelle: <code>http://localhost:8107/?path={file_path}</code></p>
    
    <h3>Instructions pour l'Attaque</h3>
    <p><strong>Cible :</strong> Lire la variable d'environnement <code>SECRET_API_KEY</code>.</p>
    <p>1. L'attaquant doit lire le fichier système spécial <code>/proc/self/environ</code>, qui contient toutes les variables d'environnement du processus en cours.</p>
    <p>2. Modifiez l'URL pour : <code>http://localhost:8107/?path=/proc/self/environ</code></p>
    <p>3. Le contenu du fichier doit afficher la clé secrète : <code>SECRET_API_KEY=EXPOSED_DOCKER_SECRET_456</code></p>
    
    <h2>Contenu du Fichier : {file_path}</h2>
    <pre>{content}</pre>
    """
    
    if file_path == 'info.txt':
        content = "Fichier d'information par défaut. Utilisez le paramètre 'path' pour attaquer le système."
    
    # ⚠️ VULNÉRABILITÉ LFI SIMULÉE ⚠️
    # Tentative de lecture du fichier spécifié par l'utilisateur
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                # Les variables d'environnement dans /proc/self/environ sont séparées par des octets nuls, 
                # nous les remplaçons par des sauts de ligne pour la lisibilité.
                content = content.replace('\x00', '\n')
        else:
            content = "Erreur: Fichier introuvable."
    except Exception as e:
        content = f"Erreur de lecture : {e}"

    return render_template_string(HTML_FORM, file_path=file_path, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
