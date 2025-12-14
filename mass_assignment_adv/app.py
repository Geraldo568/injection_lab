from flask import Flask, request, render_template_string

app = Flask(__name__)

# Simule la base de données utilisateur
USER_DB = {
    'normal_user': {'username': 'normal_user', 'email': 'user@example.com', 'is_admin': False, 'flag': 'ADMIN_FLAG_8129_ACCESS'}
}

class User:
    def __init__(self, username, email, is_admin=False, flag=''):
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.flag = flag

    def to_dict(self):
        return {'username': self.username, 'email': self.email, 'is_admin': self.is_admin}

# Charge l'utilisateur par défaut pour la démo
CURRENT_USER = User(**USER_DB['normal_user'])

HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #27ae60; border-bottom: 2px solid #2ecc71; padding-bottom: 10px; }
    .vulnerability-note { background-color: #27ae60; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"] { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; }
    input[type="submit"] { background-color: #2ecc71; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; }
    .result { margin-top: 20px; padding: 10px; border: 1px dashed #7f8c8d; }
    .success { color: #2ecc71; font-weight: bold; }
    .error { color: #e74c3c; font-weight: bold; }
    .info { background: #ecf0f1; padding: 10px; border-radius: 4px; }
</style>
<div class="vulnerability-note">VULNÉRABILITÉ CRITIQUE : Mass Assignment (Mise à jour d'un champ Admin) - Port 8129</div>
<h1>Lab 50 - Modification de Profil</h1>

<div class="info">
    Utilisateur Actuel : <b>{{ user.username }}</b> (Admin: {{ user.is_admin }})
    {% if user.is_admin %}
        <p class="success">DRAPEAU ADMIN : {{ user.flag }}</p>
    {% endif %}
</div>

<p>
    Ce service met à jour les propriétés de l'utilisateur directement à partir de l'objet <code>request.form</code> sans liste blanche (whitelisting).
</p>
<p>
    <b>Objectif :</b> Envoyer une requête POST contenant le champ caché <code>is_admin=True</code> pour élever vos privilèges et afficher le drapeau admin.
</p>
<form method="POST">
    <label for="email">Nouvel Email :</label>
    <input type="text" name="email" id="email" value="{{ user.email }}">
    <input type="submit" value="Mettre à jour le Profil">
</form>
{% if message %}
    <div class="result">
        {{ message|safe }}
    </div>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def profile():
    message = None
    
    if request.method == 'POST':
        # VULNÉRABILITÉ : Utilisation directe de request.form pour mettre à jour l'objet
        for key, value in request.form.items():
            if hasattr(CURRENT_USER, key):
                # Conversion simple de type (surtout pour 'is_admin')
                if key == 'is_admin':
                    setattr(CURRENT_USER, key, value.lower() in ('true', '1', 't'))
                else:
                    setattr(CURRENT_USER, key, value)
        
        message = f"<p class='success'>Profil mis à jour. Vérifiez le statut d'administrateur ci-dessus!</p>"

    context = CURRENT_USER.to_dict()
    context['flag'] = CURRENT_USER.flag # Passons le flag pour l'affichage conditionnel
    
    return render_template_string(HTML_TEMPLATE, user=context, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
