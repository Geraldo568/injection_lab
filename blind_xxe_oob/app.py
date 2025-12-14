from flask import Flask, request, render_template_string
from lxml import etree
import os

app = Flask(__name__)

# Créez le secret à exfiltrer (simule /etc/passwd ou une clé privée)
SECRET_FILE_PATH = "/tmp/secret_key_8116.txt"

try:
    if not os.path.exists(SECRET_FILE_PATH):
        with open(SECRET_FILE_PATH, "w") as f:
            f.write("BLIND-XXE-OOB-SECRET:eCfil3r4ti0nSucC3sS!")
except Exception as e:
    print(f"Erreur lors de la création du fichier secret: {e}")

# IMPORTANT: Les accolades doubles ({{ et }}) dans le CSS empêchent 
# Python d'interpréter les styles comme des clés de formatage.
HTML_TEMPLATE = """
<style>
    body {{ font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }}
    h1 {{ color: #8e44ad; border-bottom: 2px solid #9b59b6; padding-bottom: 10px; }}
    .vulnerability-note {{ background-color: #8e44ad; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }}
    form {{ background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }}
    textarea {{ width: 100%; height: 200px; padding: 10px; border: 1px solid #ccc; }}
    input[type="submit"] {{ background-color: #9b59b6; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; }}
</style>

<div class="vulnerability-note">VULNÉRABILITÉ CRITIQUE : Blind XXE Out-of-Band (OOB) - Port 8116</div>
<h1>Lab 37 - Générateur de Rapport XML</h1>

<p>
    Ce service prend un rapport XML, mais est configuré en mode "aveugle". 
    Il ne renvoie pas la valeur de l'entité externe, vous obligeant à utiliser une technique OOB (Out-of-Band) via une DTD externe pour exfiltrer le secret à l'adresse <code>{secret_path}</code>.
</p>
<form method="POST">
    <textarea name="xml_data" placeholder="Entrez le XML ici...">&lt;?xml version="1.0"?&gt;
&lt;report&gt;
  &lt;title&gt;Blind XXE Test&lt;/title&gt;
  &lt;content&gt;Hello World&lt;/content&gt;
&lt;/report&gt;</textarea>
    <input type="submit" value="Soumettre le XML">
</form>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    # Le .format() n'a lieu qu'au niveau de la route
    context = {'secret_path': SECRET_FILE_PATH}
    
    if request.method == 'POST':
        xml_data = request.form.get('xml_data')
        if xml_data:
            try:
                parser = etree.XMLParser(resolve_entities=False, no_network=False)
                etree.fromstring(xml_data.encode('utf-8'), parser)
                
                return render_template_string(HTML_TEMPLATE.format(**context) + "<p style='color:#2ecc71;'>Rapport traité. Aucune erreur.</p>")
            except etree.XMLSyntaxError as e:
                return render_template_string(HTML_TEMPLATE.format(**context) + "<p style='color:#e74c3c;'>Erreur de syntaxe XML.</p>")
            except Exception as e:
                return render_template_string(HTML_TEMPLATE.format(**context) + f"<p style='color:#e74c3c;'>Une erreur s'est produite: {type(e).__name__}.</p>")
                
    return render_template_string(HTML_TEMPLATE.format(**context))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
