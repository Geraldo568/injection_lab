from flask import Flask, request, render_template_string
app = Flask(__name__)
HTML_TEMPLATE="""
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    .vulnerability-note { background-color: #9c27b0; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
</style>
<div class="vulnerability-note">LAB 51 (IA) : Model Inversion Attack - Port 8130</div>
<h1>Classification des Données Utilisateurs</h1>
<p>
    Ce service simule un modèle ML entraîné sur des données sensibles (comme le nom secret d'un utilisateur). 
    L'API est mal conçue et expose les probabilités de sortie directement.
</p>
<p>
    <b>Objectif :</b> Utiliser l'accès à l'API pour effectuer une attaque d'Inversion de Modèle et deviner le nom d'entraînement secret (<code>SECRET_USER_NAME</code>) en fonction des probabilités de sortie.
</p>
<p>
    Le modèle est stocké en mémoire et n'est pas directement vulnérable à l'injection de code, mais à l'inférence statistique.
</p>
"""
@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
