from flask import Flask, request, render_template_string
import re
import urllib.parse

app = Flask(__name__)

# WAF SIMULÉ : Filtre les mots-clés SQL et XSS courants
def waf_filter(data):
    # 1. Filtre XSS : Balises script et évènements
    xss_patterns = [
        r"<script.*?>",
        r"on\w+=", # ex: onerror=, onload=
        r"javascript:",
        r"\<\s*\/\s*script\s*\>"
    ]
    # 2. Filtre SQLi : Mots-clés en minuscules/majuscules
    sqli_patterns = [
        r"select\s+",
        r"union\s+",
        r"sleep\s*\("
    ]

    # Combine et applique les filtres
    for pattern in xss_patterns + sqli_patterns:
        if re.search(pattern, data, re.IGNORECASE):
            return True, f"WAF BLOCKÉ : Motif interdit détecté ({pattern})"
    
    return False, "WAF DÉPASSÉ. Tentative en cours..."

HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #f1c40f; border-bottom: 2px solid #f39c12; padding-bottom: 10px; }
    .vulnerability-note { background-color: #f1c40f; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"] { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; }
    input[type="submit"] { background-color: #f39c12; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; }
    .result { margin-top: 20px; padding: 10px; border: 1px dashed #7f8c8d; }
    .success { color: #2ecc71; font-weight: bold; }
    .error { color: #e74c3c; font-weight: bold; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ CRITIQUE : Contournement de WAF (Web Application Firewall) - Port 8122</div>
<h1>Lab 43 - Simulateur de Requêtes Filtrées</h1>

<p>
    Ce service prend une chaîne d'entrée et tente de l'exécuter. Un WAF simple est en place pour bloquer les attaques XSS et SQLi connues.
</p>
<p>
    <b>Objectif :</b> Contourner le WAF pour que la chaîne d'entrée soit affichée SANS être bloquée.
    Un contournement réussi est l'affichage de la chaîne <code>WA F_BYPASS_SUCCESS</code>.
</p>
<form method="POST">
    <label for="payload">Chaîne d'entrée :</label>
    <input type="text" name="payload" id="payload" placeholder="Ex: <script>alert(1)</script> ou SELECT * FROM users">
    <input type="submit" value="Soumettre au WAF">
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
        payload = request.form.get('payload', '')
        
        # Le WAF vérifie l'entrée
        is_blocked, waf_message = waf_filter(payload)
        
        if is_blocked:
            message = f"<p class='error'>{waf_message}</p>"
        else:
            # Si le WAF est contourné, la chaîne est soumise.
            # Le "vrai" code vulnérable vérifie si le payload contient le drapeau secret après filtrage
            if "WA F_BYPASS_SUCCESS" in payload:
                # La vulnérabilité est l'affichage direct du payload non encodé
                message = f"<p class='success'>WAF Contourné ! Drapeaux affiché : {payload}</p>"
            else:
                message = f"<p class='success'>WAF Contourné, mais pas le drapeau. Payload affiché : {payload}</p>"
                
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
