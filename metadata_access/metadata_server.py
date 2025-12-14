from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

# JSON typique d'une réponse de credentials AWS
CREDENTIALS_RESPONSE = {
    "Code": "Success",
    "LastUpdated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "Type": "AWS-HMAC",
    "AccessKeyId": "ASIAVULNERABLEKEY",
    "SecretAccessKey": "vUlnEr4bL3SecrEtK3Y",
    "Token": "AWSTokenLongStringExample",
    "Expiration": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 3600))
}

HTML_RESPONSE = f"""
    <html>
    <body style="font-family: Arial; background-color: #e6f7ff; padding: 20px;">
        <h1 style="color: #2c3e50;">Cloud Metadata Endpoint Simulator</h1>
        <p>Ce service simule l'endpoint de métadonnées interne. Il est conçu pour être accessible uniquement via une adresse IP spécifique (ex: 169.254.169.254).</p>
        <p>L'application vulnérable s'y connecte si l'attaquant fournit l'URL interne correcte.</p>
        <h2>Clés d'Accès Volées (JSON) :</h2>
        <pre style="background: #fff; padding: 15px; border: 1px solid #3498db;">{json.dumps(CREDENTIALS_RESPONSE, indent=4)}</pre>
    </body>
    </html>
"""

class MetadataHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(HTML_RESPONSE, "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer(("0.0.0.0", 80), MetadataHandler)
    print("Metadata Endpoint Simulator started on port 80...")
    webServer.serve_forever()
