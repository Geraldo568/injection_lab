from flask import Flask, request, render_template_string
import base64
import pickle
import os

app = Flask(__name__)

class UserSession:
    def __init__(self, username="guest"):
        self.username = username
        self.auth = False

    def __reduce__(self):
        return (UserSession, (self.username,))


HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #d35400; border-bottom: 2px solid #e67e22; padding-bottom: 10px; }
    .vulnerability-note { background-color: #d35400; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    textarea { width: 100%; height: 100px; padding: 10px; border: 1px solid #ccc; }
    input[type="submit"] { background-color: #e67e22; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ CRITIQUE : Insecure Deserialization RCE (Python Pickle) - Port 8117</div>
<h1>Lab 38 - Outil de Désérialisation de Session</h1>

<p>
    Ce service prend un objet de session sérialisé (Base64) et le désérialise en utilisant <code>pickle.loads()</code>.
    Votre objectif est de générer un <b>payload Python Pickle</b> qui exécute la commande <code>touch /tmp/rce_exploit_8117</code> dans le conteneur.
</p>
<form method="POST">
    <label for="session_data">Données de Session Sérialisées (Base64):</label>
    <textarea name="session_data" id="session_data" placeholder="Collez votre payload Base64 ici..."></textarea>
    <input type="submit" value="Charger la Session">
</form>
<div id="output"></div>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        data_b64 = request.form.get('session_data')
        
        try:
            data_bytes = base64.b64decode(data_b64)
            session_object = pickle.loads(data_bytes)
            
            message = f"<p style='color:#2ecc71;'>Succès! Session chargée pour l'utilisateur: <b>{session_object.username}</b></p>"
            
            if os.path.exists('/tmp/rce_exploit_8117'):
                message += f"<p style='color:#e74c3c; font-weight:bold;'>RCE RÉUSSIE: Fichier de preuve /tmp/rce_exploit_8117 trouvé!</p>"
                os.remove('/tmp/rce_exploit_8117') 

        except EOFError:
             message = "<p style='color:#e74c3c;'>Erreur de désérialisation: Le payload Base64 est incomplet ou mal formé.</p>"
        except Exception as e:
            message = f"<p style='color:#e74c3c;'>Erreur: Impossible de charger la session. ({type(e).__name__})</p>"


    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
