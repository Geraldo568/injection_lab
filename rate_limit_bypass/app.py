from flask import Flask, request, render_template_string
import time
app = Flask(__name__)
# Liste des IP/Tentatives (Simule le Rate Limit)
ATTEMPTS = {}
OTP_SECRET = "9999"

HTML_TEMPLATE="""
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    .vulnerability-note { background-color: #e91e63; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    /* ... (Style complet à insérer) ... */
</style>
<div class="vulnerability-note">LAB 52 : Rate Limit Bypass (Contournement de Limite de Taux) - Port 8131</div>
<h1>Vérification d'OTP Vulnérable</h1>
<p>
    Ce service implémente une limite de tentatives basée sur l'IP, mais peut être contourné.
</p>
<p>
    <b>Objectif :</b> Trouver l'OTP secret (<code>9999</code>) en bruteforçant le champ de saisie tout en contournant le limiteur de taux.
    (Piste : Chercher l'absence de vérification sur un paramètre secondaire de la requête.)
</p>
<form method="POST">
    <label for="otp">Entrez l'OTP à 4 chiffres :</label>
    <input type="text" name="otp" id="otp" placeholder="Ex: 1234">
    <input type="submit" value="Vérifier">
</form>
{% if message %}
    <div class="result">
        {{ message|safe }}
    </div>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.remote_addr
    message = None

    # VULNÉRABILITÉ : La limite de taux ne gère pas les paramètres secondaires (ex: Host, Headers X-Forwarded-For bidons)
    if ATTEMPTS.get(ip, 0) >= 5:
         return render_template_string(HTML_TEMPLATE, message="<p class='error'>Limite de tentatives atteinte pour cette IP.</p>")
    
    if request.method == 'POST':
        otp = request.form.get('otp')
        ATTEMPTS[ip] = ATTEMPTS.get(ip, 0) + 1 # Incrémentation du compteur de tentatives
        
        # VULNÉRABILITÉ D'AUTHENTIFICATION : OTP non sécurisé
        if otp == OTP_SECRET:
            message = "<p class='success'>OTP correct ! DRAPEAU : RATE_LIMIT_BYPASS_SUCCESS</p>"
        else:
            message = f"<p class='error'>OTP incorrect. Tentatives restantes : {5 - ATTEMPTS.get(ip, 0)}</p>"
            
    return render_template_string(HTML_TEMPLATE, message=message)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
