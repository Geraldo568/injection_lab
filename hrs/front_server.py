# front_server.py (Simule le Load Balancer / Front-End, préfère Content-Length)
from http.server import BaseHTTPRequestHandler, HTTPServer
# import requests  <-- Cette ligne est supprimée

# CSS intégré pour le rendu esthétique
PAGE_STYLE = """
<style>
body{font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px;} 
.vulnerability-note{background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px;}
pre{background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto;}
</style>
"""

class FrontHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(f"""
            <html><head><title>HRS Lab - Proxy/Front (Port 8090)</title>{PAGE_STYLE}</head>
            <body>
            <div class="vulnerability-note">VULNÉRABILITÉ: HTTP Request Smuggling (HRS) - Port 8090</div>
            <h1>Lab HRS - Front-End (Type CL.TE)</h1>
            <p><strong>Cible:</strong> Exploiter l'incohérence entre les serveurs. Le Front-End (vous) lit l'en-tête <code>Content-Length</code>. Le Back-End (interne) lit l'en-tête <code>Transfer-Encoding: chunked</code>.</p>
            <h3>Instructions (Attaque CL.TE)</h3>
            <p>Envoyez une requête POST où :</p>
            <ul>
                <li><code>Content-Length</code> (CL) est le plus petit (ex: taille de la première ligne de données).</li>
                <li><code>Transfer-Encoding: chunked</code> (TE) est présent.</li>
            </ul>
            <p>Le Back-End lira l'en-tête <code>TE</code> et traitera la requête suivante comme faisant partie du corps de la requête précédente, contaminant la requête d'un autre utilisateur.</p>
            
            <h3>Testez avec cURL :</h3>
            <pre>
curl -i -X POST http://localhost:8090/ -H "Host: localhost" \\
-H "Content-Length: 6" -H "Transfer-Encoding: chunked" \\
--data-binary $'0\\r\\n\\r\\nGET /admin HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n'
            </pre>
            <p>Le Back-End devrait voir "GET /admin...".</p>
            </body></html>
        """, "utf-8"))

    def do_POST(self):
        # Simuler l'analyse du corps par le Front-End (privilégie Content-Length)
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            # Le Front-End ne lit que CL octets.
            request_body_front = self.rfile.read(content_length) 
        except Exception:
            request_body_front = b''
        
        # Afficher le résultat pour le debug.
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(f"Front-End (CL) Processed. CL Length Read: {len(request_body_front)}. \nEnvoyez une requête POST pour vérifier le log du Back-End.", "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer(("0.0.0.0", 80), FrontHandler)
    print("HRS Front-End Server (CL) started on port 80...")
    webServer.serve_forever()
