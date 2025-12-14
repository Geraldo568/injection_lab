from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .info { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; white-space: pre-wrap; }
    .backend-note { background-color: #3498db; color: white; padding: 8px; border-radius: 4px; }
</style>
<div class="backend-note">BACK-END SERVER (Lis Content-Length)</div>
<h1>Lab 16 - Back-end: Interprétation de Requête</h1>

<p>Le back-end reçoit la requête du Front-end.</p>
<div class="info">
    <strong>Méthode:</strong> {{ method }}<br>
    <strong>URL:</strong> {{ path }}<br>
    <strong>Headers (CL):</strong> {{ cl_header }}<br>
    <strong>Body (CL):</strong> {{ body_cl }}<br>
</div>
<hr>
<p>
    <strong>Statut de l'Application:</strong>
    {% if smuggled_request %}
        <span style="color: red; font-weight: bold;">[SMUGGLING DETECTÉ]</span> Requête illicite (SMUGGLED) reçue !
    {% else %}
        <span style="color: green; font-weight: bold;">[OK]</span> Requête normale traitée.
    {% endif %}
</p>
"""

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handler(path):
    method = request.method
    
    # Simuler la lecture par le Back-end (qui lit CL)
    cl_header = request.headers.get('Content-Length')
    body_cl = request.data.decode('latin-1').replace('\n', '\\n').replace('\r', '\\r')

    smuggled_request = 'SMUGGLED-REQUEST-MAGIC' in body_cl or 'GET /admin' in body_cl

    return render_template_string(HTML_TEMPLATE, 
                                  method=method, 
                                  path=f'/{path}',
                                  cl_header=cl_header,
                                  body_cl=body_cl[:200] + ('...' if len(body_cl) > 200 else ''),
                                  smuggled_request=smuggled_request)

if __name__ == '__main__':
    # Le back-end est exposé sur un port interne uniquement
    app.run(host='0.0.0.0', port=80)
