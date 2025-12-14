from flask import Flask, request, render_template_string
from lxml import etree # L'analyseur XML
import json

app = Flask(__name__)

# La page de base avec le formulaire
HTML_FORM = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    textarea { width: 100%; height: 150px; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    input[type="submit"] { background-color: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .info { color: #3498db; margin-top: 15px; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: XXE Injection Avancée (Out-of-Band) - Port 8103</div>
<h1>Lab 24 - Analyseur de Configuration XML</h1>

<p>Le serveur analyse le XML sans désactiver la résolution d'entités externes. La sortie n'est pas reflétée, donc une technique OOB est requise.</p>

<form method="POST">
    <label for="xml_data">Configuration XML :</label>
    <textarea name="xml_data" id="xml_data"><config><user>alice</user><param>test</param></config></textarea>
    <input type="submit" value="Analyser la Configuration">
</form>

<h2>Résultat de l'Analyse</h2>
<pre>{{ result }}</pre>

<h3>Instructions pour l'Attaque OOB</h3>
<p><strong>Cible :</strong> Exfiltrer le contenu du fichier <code>/etc/passwd</code> vers un serveur contrôlé par l'attaquant (non inclus dans ce lab, mais nécessaire pour l'exploit).</p>
<p>1. Vous devez utiliser une charge utile qui définit une entité externe, puis une entité paramètre pour charger une DTD externe malveillante (par exemple, hébergée sur votre serveur d'écoute `http://ATTAQUANT.COM:8080/evil.dtd`).</p>
<p>2. Cette DTD doit forcer l'analyseur à lire le contenu du fichier et à l'envoyer à votre serveur d'écoute via une requête HTTP ou FTP, en utilisant une entité paramètre pour la concaténation de chaînes (par exemple, pour exfiltrer <code>/etc/passwd</code> dans la requête GET).</p>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = "En attente de l'envoi du XML..."
    
    if request.method == 'POST':
        xml_data = request.form.get('xml_data', '')
        
        # ⚠️ VULNÉRABILITÉ XXE ⚠️: etree.fromstring est vulnérable par défaut à l'XXE
        # etree.parse(source, parser)
        try:
            # Pour lxml, DTD et la résolution d'entités externes sont activées par défaut
            root = etree.fromstring(xml_data.encode('utf-8'))
            
            # Traitement simulé des données
            processed_data = {child.tag: child.text for child in root}
            result = f"Analyse XML réussie (Données traitées) : \n{json.dumps(processed_data, indent=2)}\n\n"
            result += "Si une requête Out-of-Band a été déclenchée, vous la verrez sur votre serveur d'écoute."
            
        except etree.XMLSyntaxError as e:
            result = f"Erreur de syntaxe XML: {e}"
        except Exception as e:
            result = f"Erreur inattendue: {e}"

    return render_template_string(HTML_FORM, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
