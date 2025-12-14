from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# --- WAF SIMULÉ ---
def simple_waf(query_param):
    """Bloque les mots-clés SQL sensibles (OR, SELECT, UNION, etc.)."""
    keywords = ['OR', 'SELECT', 'UNION', 'AND', 'SLEEP', 'WAITFOR', 'SCRIPT']
    if any(keyword in query_param.upper() for keyword in keywords):
        return True
    return False

# --- CONFIGURATION DB ---
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, secret TEXT)''')
    c.execute("INSERT INTO users VALUES (1, 'alice', 'USER_SECRET_456')")
    c.execute("INSERT INTO users VALUES (101, 'admin', 'FLAG_HPP_IS_FUN_7890')")
    conn.commit()
    conn.close()

init_db()


HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #27ae60; border-bottom: 2px solid #2ecc71; padding-bottom: 10px; }
    .vulnerability-note { background-color: #27ae60; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .query-box { background: #ecf0f1; padding: 15px; border-radius: 4px; margin-top: 15px; }
    .result { margin-top: 20px; padding: 10px; border: 1px dashed #7f8c8d; }
    .error { color: #e74c3c; font-weight: bold; }
    .success { color: #27ae60; font-weight: bold; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ AVANCÉE : HTTP Parameter Pollution (HPP) / WAF Bypass - Port 8118</div>
<h1>Lab 39 - Filtrage de Comptes Utilisateur</h1>

<p>
    L'application recherche un utilisateur par son <code>id</code>. La requête SQL est vulnérable, mais un WAF rudimentaire tente de bloquer les injections.
</p>

<p>
    <b>Objectif :</b> Contourner le WAF pour obtenir le <code>secret</code> de l'utilisateur <code>admin</code> (ID 101).
</p>

<div class="query-box">
    Exemple d'accès : <code>/?id=1</code>
</div>

{% if message %}
    <div class="result">
        {{ message|safe }}
    </div>
{% endif %}
"""

@app.route('/', methods=['GET'])
def index():
    user_id_list = request.args.getlist('id')
    message = None
    
    if not user_id_list:
        return render_template_string(HTML_TEMPLATE, message=None)

    # 1. --- LOGIQUE DU WAF SIMULÉ ---
    waf_check = user_id_list[0]
    if simple_waf(waf_check):
        message = f"<p class='error'>WAF Block: La valeur '{waf_check}' a déclenché le filtre de sécurité.</p>"
        return render_template_string(HTML_TEMPLATE, message=message)
        
    # 2. --- LOGIQUE DE L'APPLICATION VULNÉRABLE (HPP) ---
    user_id_to_query = user_id_list[-1] # VULNÉRABLE : Prend la dernière valeur non filtrée
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    sql_query = f"SELECT username, secret FROM users WHERE id = {user_id_to_query}"
    
    try:
        c.execute(sql_query)
        result = c.fetchall()
        
        if result:
            output = ["<p class='success'>Résultat(s) trouvé(s) :</p><ul>"]
            for username, secret in result:
                output.append(f"<li>Utilisateur: <b>{username}</b> | Secret: <b>{secret}</b></li>")
            output.append("</ul>")
            message = "".join(output)
        else:
            message = "<p class='error'>Aucun utilisateur trouvé.</p>"

    except sqlite3.OperationalError as e:
        message = f"<p class='error'>Erreur SQL: {e}</p>"
    
    conn.close()
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
