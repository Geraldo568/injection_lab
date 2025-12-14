from flask import Flask, request, session, redirect, url_for, render_template_string
from flask_session import Session
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Simuler l'état utilisateur et le code MFA (stocké en session)
VALID_USER = "admin"
VALID_PASS = "securepassword"

HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"], input[type="password"] { padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; width: 100%; }
    input[type="submit"] { background-color: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; }
    .success { color: #27ae60; font-weight: bold; }
    .error { color: #c0392b; font-weight: bold; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: Contournement MFA par Logique - Port 8115</div>
<h1>Lab 36 - Connexion Admin avec MFA</h1>

<h2>{% if logged_in %}Page Protégée{% else %}Étape 1: Connexion{% endif %}</h2>

{% if logged_in %}
    <p class="success">ACCÈS ADMINISTRATEUR !</p>
    <p>Félicitations, vous êtes connecté en tant que {{ session.get('user') }}.</p>
    <p>Le secret est : **MFA-BYPASS-7890**</p>
    <p><a href="{{ url_for('logout') }}">Déconnexion</a></p>

{% elif session.get('mfa_required') %}
    <h3>Étape 2: Vérification MFA (Code: 123456)</h3>
    <p>Veuillez entrer le code MFA simulé (123456) ou **tenter l'attaque de contournement**.</p>
    <form method="POST" action="{{ url_for('mfa_verify') }}">
        <label for="mfa_code">Code MFA:</label>
        <input type="text" id="mfa_code" name="mfa_code" required>
        <input type="submit" value="Vérifier">
    </form>
    {% if error %}<p class="error">{{ error }}</p>{% endif %}

{% else %}
    <p>Connectez-vous avec Admin / securepassword. L'étape MFA sera déclenchée.</p>
    <form method="POST" action="{{ url_for('login') }}">
        <label for="username">Utilisateur:</label>
        <input type="text" id="username" name="username" value="admin" required>
        <label for="password">Mot de passe:</label>
        <input type="password" id="password" name="password" value="securepassword" required>
        <input type="submit" value="Connexion">
    </form>
{% endif %}
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE, logged_in=session.get('logged_in'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == VALID_USER and password == VALID_PASS:
        session['user'] = username
        session['mfa_required'] = True
        return redirect(url_for('mfa_verify'))
    
    return render_template_string(HTML_TEMPLATE, error="Identifiants invalides.")

@app.route('/mfa_verify', methods=['GET', 'POST'])
def mfa_verify():
    if not session.get('user'):
        return redirect(url_for('index'))

    # ⚠️ VULNÉRABILITÉ LOGIQUE MFA ⚠️
    bypass_param = request.args.get('mfa_passed') 
    
    if bypass_param and bypass_param.lower() == 'true':
        # LE BYPASS RÉUSSIT !
        session['mfa_required'] = False
        session['logged_in'] = True
        return redirect(url_for('index'))

    # Vérification normale du code (si pas de bypass)
    if request.method == 'POST':
        mfa_code = request.form.get('mfa_code')
        if mfa_code == '123456':
            session['mfa_required'] = False
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template_string(HTML_TEMPLATE, logged_in=False, mfa_required=True, error="Code MFA incorrect.")
    
    return render_template_string(HTML_TEMPLATE, logged_in=False, mfa_required=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
