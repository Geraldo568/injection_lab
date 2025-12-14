# back_server.py (Simule le Back-End, préfère Transfer-Encoding)
from http.server import BaseHTTPRequestHandler, HTTPServer

class BackHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Simuler le Back-End (TE) : Il lit le corps basé sur Transfer-Encoding s'il est présent.
        # Pour une simple démo, nous lisons tout ce qui est reçu pour montrer la partie "smuggled".
        request_body = self.rfile.read(int(self.headers.get('content-length', 0))).decode('utf-8', errors='ignore')
        
        # NOTE : Dans un vrai lab, la bibliothèque TE lirait la partie smuggled après le CL.
        # Ici, nous nous concentrons sur la démo où l'attaquant envoie une requête valide pour le CL, 
        # mais le TE est là pour que le Back-End lise la partie suivante comme une nouvelle requête.

        # Vérification si une requête supplémentaire est présente
        smuggled_part = ""
        if '0\r\n\r\n' in request_body:
            smuggled_part = request_body.split('0\r\n\r\n', 1)[1]

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        if smuggled_part:
            self.wfile.write(bytes(f"Back-End Received (TE) and found SMUGGLED REQUEST:\n---> {smuggled_part.strip()}", "utf-8"))
        else:
            self.wfile.write(bytes(f"Back-End Received (TE): {request_body.strip()}", "utf-8"))

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Back-End HRS is alive.", "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer(("0.0.0.0", 80), BackHandler)
    print("HRS Back-End Server (TE) started on port 80...")
    webServer.serve_forever()
