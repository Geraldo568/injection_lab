from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

# Simule un modèle de classification de spam/non-spam simple (très vulnérable)
def ml_model_predict(text):
    # Logique de détection très simple simulant la vulnérabilité aux bruits/espaces/caractères invisibles
    
    # 1. Filtre normal : bloque 'spam' et 'viagra'
    if "spam" in text.lower() or "viagra" in text.lower():
        return "Spam détecté (Score 0.95)"
    
    # 2. Filtre vulnérable : si des caractères d'échappement sont ajoutés, le modèle se trompe
    if re.search(r"s\s*p\s*a\s*m", text.lower()):
        return "Non-Spam (Score 0.10). Attaque Adversarial Réussie."
        
    return "Non-Spam (Score 0.05)"

HTML_TEMPLATE="""
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    .vulnerability-note { background-color: #795548; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    /* ... (Style complet à insérer) ... */
</style>
<div class="vulnerability-note">LAB 54 (IA) : Adversarial Input Attack - Port 8133</div>
<h1>Classificateur de Spam/Non-Spam</h1>
<p>
    Ce service simule un modèle ML naïf pour classer les messages. Il est vulnérable aux entrées contradictoires (Adversarial Inputs) qui peuvent tromper le modèle.
</p>
<p>
    <b>Objectif :</b> Entrez le mot "spam" dans le champ, mais d'une manière qui force le modèle à le classer comme "Non-Spam".
    (Astuce : Utiliser des caractères invisibles ou des espaces pour le "bruit".)
</p>
<form method="POST">
    <label for="message">Message :</label>
    <input type="text" name="message" id="message" placeholder="Tenter de faire passer 'spam'">
    <input type="submit" value="Classer">
</form>
{% if prediction %}
    <div class="result">
        <b>Prédiction :</b> {{ prediction|safe }}
    </div>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        message = request.form.get('message', '')
        prediction = ml_model_predict(message)
            
    return render_template_string(HTML_TEMPLATE, prediction=prediction)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
