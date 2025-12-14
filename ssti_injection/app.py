from flask import Flask, request, render_template_string

app = Flask(__name__)

# La page de base avec le formulaire
HTML_FORM = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"] { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    input[type="submit"] { background-color: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .result-box { margin-top: 20px; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: Server Side Template Injection (SSTI) - Port 8096</div>
<h1>Lab 17 - Page de Bienvenue (Vulnérable SSTI)</h1>

<p>Le moteur de template est configuré de manière non sécurisée.</p>

<form method="GET">
    <label for="name">Votre nom :</label>
    <input type="text" id="name" name="name" placeholder="Entrez votre nom">
    <input type="submit" value="Afficher le message">
</form>

<div class="result-box">
    <h2>Message personnalisé :</h2>
    <pre>{{ message_result }}</pre>
</div>
"""

@app.route('/', methods=['GET'])
def index():
    name = request.args.get('name', 'Utilisateur')
    
    # ⚠️ VULNÉRABILITÉ SSTI : Le moteur de template est utilisé pour rendre
    # une chaîne qui inclut directement l'entrée utilisateur non nettoyée.
    template = f"Bienvenue, {name}!"
    
    # Si l'attaquant injecte une expression Jinja2 comme {{ 7 * 7 }}, 
    # le moteur de template va l'évaluer et afficher 49.
    
    try:
        # L'injection a lieu ici, le moteur de template Jinja2 exécute le code malicieux
        result = render_template_string(HTML_FORM, message_result=render_template_string(template))
    except Exception as e:
        result = render_template_string(HTML_FORM, message_result=f"Erreur de rendu du template : {e}")
        
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
