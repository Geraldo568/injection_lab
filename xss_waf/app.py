from flask import Flask, request, render_template_string, redirect, url_for
import re

app = Flask(__name__)

# Simuler la base de données des commentaires
COMMENTS = []

# WAF SIMULÉ : Filtrage agressif
def waf_filter(text):
    """Bloque les payloads XSS courants en utilisant un filtre par liste noire."""
    if not text:
        return ""
    
    # ⚠️ WAF VULNÉRABLE ⚠️: Liste noire simple et sensible à la casse
    text = text.lower() # Naïveté: convertit en minuscule, contournable via encodage/non-casse
    
    # Tentative de bloquer les balises et événements fréquents
    blacklist = [
        r'<script', r'</script>', 
        r'onload', r'onerror', 
        r'alert', r'prompt', 
        r'javascript:', r'document\.', 
        r'eval\('
    ]
    
    for term in blacklist:
        text = re.sub(term, '***BLOCKED***', text) # Remplacement simple
        
    return text.upper() # Conversion en majuscule pour rendre l'injection difficile (mais pas impossible)


HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    textarea { width: 100%; height: 80px; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    input[type="submit"] { background-color: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
    .comment { border: 1px solid #bdc3c7; padding: 10px; margin-top: 10px; background: #fff; border-radius: 4px; }
    .info { color: #3498db; margin-top: 15px; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: XSS Stocké Avancé (WAF Evasion) - Port 8112</div>
<h1>Lab 33 - Blog avec WAF Inefficace</h1>

<p class="info">Le serveur utilise un WAF pour filtrer les balises <code>&lt;script&gt;</code>, <code>alert()</code>, <code>onerror</code>, etc., mais il est contournable.</p>

<h3>Ajouter un Commentaire (Point d'Injection)</h3>
<form method="POST" action="{{ url_for('add_comment') }}">
    <label for="comment">Votre Commentaire :</label>
    <textarea name="comment" id="comment" placeholder="Entrez un commentaire. Essayez un payload XSS pour voir le WAF en action."></textarea>
    <input type="submit" value="Soumettre">
</form>

<h2>Commentaires (Point de Réflexion/Exécution)</h2>
{% for comment in comments %}
    <div class="comment">
        {{ comment|safe }} 
    </div>
{% else %}
    <p>Aucun commentaire.</p>
{% endfor %}

<h3>Instructions pour l'Attaque</h3>
<p><strong>Cible :</strong> Exécuter <code>alert(1)</code> ou <code>prompt(document.domain)</code>.</p>
<p>1. Le WAF bloque les chaînes courantes. Vous devez trouver une balise ou un événement non listé, ou utiliser un encodage qui est décodé par le navigateur mais pas par le WAF (par exemple, entités HTML, ou une variation de casse/formatage).</p>
<p>2. Un exemple d'évasion peut être l'utilisation d'une balise moins courante comme <code>&lt;img src=x onXXX=...&gt;</code> ou <code>&lt;svg/onload=...&gt;</code>, en injectant des sauts de ligne ou des caractères non standard pour briser l'analyse du filtre.</p>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE, comments=COMMENTS)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    raw_comment = request.form.get('comment', '')
    
    # 1. Le commentaire passe par le WAF
    sanitized_comment = waf_filter(raw_comment)
    
    # 2. Le commentaire est stocké et sera affiché tel quel
    COMMENTS.append(sanitized_comment)
    
    # Nous stockons également le commentaire brut pour voir ce qui est bloqué
    COMMENTS.append(f"<p>*** Log WAF : ' {raw_comment} ' devient : {sanitized_comment} </p>")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
